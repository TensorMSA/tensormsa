from master.automl.automl import AutoMlCommon
from master.network.nn_common_manager import NNCommonManager
from master.workflow.init.workflow_init_simple import WorkFlowSimpleManager
from master.workflow.common.workflow_common import WorkFlowCommon
import random, logging, copy
from django.db import connection
from common.utils import *
from cluster.service.service_train_task import train
from celery import group
from celery.task.control import inspect

def automl_run(nnid) :
    AutoMlRunManager(nnid).run()

class AutoMlRunManager :
    """
    automl runmanager with handles
    from create net ver, batch ver
    """
    def __init__(self, nn_id):
        """
        initialize parms need to run auto mode
        :return:
        """
        self.nn_id = nn_id
        self.auto_ml_info = AutoMlCommon(nn_id)
        self.conf_info = self.auto_ml_info.conf_info
        self.parm_info = self.auto_ml_info.parm_info
        self.stat_info = self.auto_ml_info.stat_info
        self.net_type = self.auto_ml_info.net_type
        self.summary = {}
        self.summary['bygen'] = []
        self.summary['best'] = []
        self.debug_mode = False

    def run(self):
        """
        run automl
        :return:
        """
        try :
            # get genetic algorithm hyper parameters
            generation = self.parm_info.get('generation')
            population = self.parm_info.get('population')
            survive = self.parm_info.get('survive')

            # define gene list
            networks = []

            # iterate generation
            for idx in range(generation) :
                # create new generations
                if(idx == 0) :
                    gen_nets, ver_data_sets = self.create_networks(idx, population)
                    networks = networks + gen_nets
                    AutoMlCommon().reset_stat_obj(self.nn_id)
                else :
                    gen_nets, ver_data_sets = self.create_networks(idx, population - survive)
                    networks = networks + gen_nets

                # train & evaluate networks
                networks = self.train_networks(networks)
                # set each train set flag to fin
                self.set_train_finish(ver_data_sets)
                # update traing progress
                self.update_summary(networks, survive)
                # sort & discard
                networks = self.discard_inferior(networks, survive)
            return networks
        except Exception as e :
            logging.error("Error on running AutoML alogorithm : {0}".format(e))

    def update_summary(self, networks, survive):
        """
        update summary info of processing genetic algorithm
        arranged by generation (sequece of list means number of generation
        each node contains extra info like survive or not 
        :param networks: networks for one generations
        :param survive: number of gene to survive 
        :return: dict type result info with extra flag 
        """
        networks = sorted(networks, key=lambda x: x.get('acc'), reverse=True)
        result = list(map(lambda x : self.set_value(x, 'survive', True) , networks[0:survive]))
        self.summary['best'] = result
        result = result + list(map(lambda x : self.set_value(x, 'survive', False) , networks[survive:]))
        self.summary['bygen'].append(result)
        AutoMlCommon().update_stat_obj(self.nn_id, self.summary)

    def set_value(self, data_set, key, value):
        data_set[key] = value
        return data_set

    def save_summary(self, info):
        """
        save best survived results
        :return:
        """
        self.summary['best'] = info
        AutoMlCommon().update_stat_obj(self.nn_id, self.summary)

    def discard_inferior(self, networks, survive):
        """
        discard inferior genes combinations
        :param networks: network lists
        :return: networks
        """
        networks = sorted(networks, key=lambda x : x.get('acc'), reverse=True)
        return networks[0:survive]

    def train_networks(self, networks):
        """
        train each networks on cluster server
        :param networks: network lists
        :return: networks
        """
        try :
            tasks = []
            #i = inspect()
            #if (i.active() == None):
            if (self.debug_mode):
                # for debug you can run all tasks on django process
                for network in networks:
                    if(network['flag'] == True ) :
                        continue
                    result = train(network.get('nn_id'), str(network.get('nn_wf_ver_id')))
                    key = '_'.join([network['nn_id'], str(network['nn_wf_ver_id'])])
                    network['acc'] = result[key].get('accuracy')
                    network['flag'] = True
            else :
                # You can use cluster servers for faster hyper parameter searching
                # using cluster server with celery for genetic algorithm
                for network in networks :
                    if (network['flag'] == True):
                        continue
                    tasks.append(train.subtask((network.get('nn_id'), str(network.get('nn_wf_ver_id')))))
                results = group(tasks).apply_async()
                results = results.join()
                for result in results :
                    for network in networks :
                        key = '_'.join([network['nn_id'], str(network['nn_wf_ver_id'])])
                        if(key in list(result.keys()) and result[key] is not None and result[key].get('accuracy') is not None) :
                            network['acc'] = result[key].get('accuracy')
                            network['flag'] = True
            return networks
        except Exception as e :
            logging.error("Error on training : {0} ".format(e))

    def create_networks(self, generation, number):
        """
        We need to create new network for evluate our hyperparameter
        :param generation:number of generation
        :param population:number of population for each generation
        :return:return list of network (nn_id and version)
        """
        try :
            networks = []
            ver_data_sets = []
            for idx in range(number) :
                # (1) create version
                nn_wf_ver_id, ver_data_set = self.create_version(str(generation))
                ver_data_sets.append(ver_data_set)

                # (2) create state & graph flow
                WorkFlowSimpleManager().create_workflow(self.nn_id, nn_wf_ver_id, self.net_type)
                all_node_list = self.get_all_nodes_list(self.nn_id, nn_wf_ver_id)

                # (3) generate conf format for new train & set netconf node
                node_confs = self._generate_random_case(copy.deepcopy(self.conf_info))

                # (4) set node params
                for node in all_node_list:
                    node_name = node.get('nn_wf_node_name')
                    if(node_name in node_confs) :
                        WorkFlowCommon().set_view_obj('_'.join([str(self.nn_id), str(nn_wf_ver_id), node_name]),
                                                      node_confs[node_name])

                        if (node.get('wf_task_menu_id_id') == "data") :
                            update_data = {}
                            update_data['source_path'] = get_source_path(str(self.nn_id), "common", node_name)
                            update_data['store_path'] = get_store_path(str(self.nn_id), "common", node_name)
                            WorkFlowCommon().update_view_obj('_'.join([str(self.nn_id), str(nn_wf_ver_id), node_name]),
                                                             update_data)

                        if (node.get('wf_task_menu_id_id') == "eval") :
                            update_data = {}
                            update_data['source_path'] = get_source_path(str(self.nn_id), "common", node_name)
                            update_data['store_path'] = get_store_path(str(self.nn_id), "common", node_name)
                            WorkFlowCommon().update_view_obj('_'.join([str(self.nn_id), str(nn_wf_ver_id), node_name]),
                                                             update_data)

                        if (node.get('wf_task_menu_id_id') == "netconf") :
                            update_data = {}
                            update_data['model_path'] = get_model_path(str(self.nn_id), str(nn_wf_ver_id), node_name)
                            update_data['modelpath'] = get_model_path(str(self.nn_id), str(nn_wf_ver_id), node_name)
                            WorkFlowCommon().update_view_obj('_'.join([str(self.nn_id), str(nn_wf_ver_id), node_name]),
                                                             update_data)

                # (5) return summary result
                netdata = {}
                netdata['nn_id'] = self.nn_id
                netdata['generation'] = generation
                netdata['nn_wf_ver_id'] = nn_wf_ver_id
                netdata['acc'] = 0.0
                netdata['flag'] = False
                netdata['survive'] = True
                networks.append(netdata)
            return networks, ver_data_sets
        except Exception as e :
            logging.error("Error AutoML create network : {0}".format(e))

    def mutation(self, networks, number):
        """
        mutate gene with survived ones
        :param networks: networks info
        :param number: number of genes to generate
        :return: networks
        """
        pass

    def create_version(self, generation):
        """
        create version on database
        :param generation:
        :return:
        """
        # Create Version
        nnCommonManager = NNCommonManager()
        nn_wf_ver_id = nnCommonManager.get_nn_max_ver(self.nn_id) + 1
        input_data = {}
        input_data['nn_wf_ver_id'] = nn_wf_ver_id
        input_data['nn_def_list_info_nn_id'] = generation
        input_data['automl_gen'] = generation
        input_data['condition'] = "2"  # 1 Pending, 2 Progress, 3 Finish, 4 Error
        input_data['active_flag'] = "N"
        input_data['nn_wf_ver_desc'] = " ".join(["id:",self.nn_id, "gen:", generation, "ver:", str(nn_wf_ver_id)])
        input_data['nn_id'] = self.nn_id

        # Net Version create
        nnCommonManager.insert_nn_wf_info(input_data)
        return nn_wf_ver_id, input_data

    def set_train_finish(self, ver_data_sets):
        """
        update state flag for version level info on database
        :param input_data : raw info we had on database 
        :return:version info 
        """
        try :
            for input_data in ver_data_sets :
                # Create Version
                nnCommonManager = NNCommonManager()
                del input_data['nn_id']
                input_data['condition'] = "3" # 1 Pending, 2 Progress, 3 Finish, 4 Error
                # Net Version create
                nnCommonManager.update_nn_wf_info(self.nn_id, input_data)
            return True
        except Exception as e :
            return False

    def _generate_random_case(self, conf_info):
        """
        generate random case for train
        :param auto_ml_info: auto ml conf json format
        :return: json form for neural network
        """
        try :
            if (type(conf_info) == dict) :
                row = self._find_leaf(conf_info)
                if(row is None):
                    return conf_info
                if(self._check_format(conf_info[row])) :
                    conf_info[row] = self._format_conv(conf_info[row])
                    return conf_info
                else :
                    val = self._generate_random_case(conf_info[row])
                    conf_info[row] = val
                    return self._generate_random_case(conf_info)
            elif (type(conf_info) == list) :
                i, row = self._find_leaf(conf_info)
                if (row is None):
                    return conf_info
                if (self._check_format(row)):
                    conf_info[i] = self._format_conv(row)
                    return conf_info
                else:
                    val = self._generate_random_case(row)
                    conf_info[i] = val
                    return self._generate_random_case(conf_info)
            else :
                return conf_info

        except Exception as e :
            raise Exception ("error on automl generate random case : {0}".format(e))

    def _find_leaf(self, conf_info):
        """

        :param conf_info:
        :return:
        """
        if (type(conf_info) == dict):
            for row in list(conf_info.keys()):
                if (str(conf_info[row]).find("auto") < 0) :
                    continue
                if (type(conf_info[row]) in [list]):
                    return row
                if(conf_info[row] is None or type(conf_info[row]) not in [dict]):
                    continue
                if (type(conf_info[row]) in [dict] or conf_info[row].get("auto") is not None):
                    return row
            return None
        elif (type(conf_info) == list):
            for i, row in enumerate(conf_info):
                if (str(row).find("auto") < 0) :
                    continue
                if (row is None):
                    continue
                if (type(row) in [dict] or row.get("auto") is not None):
                    return i, row
            return None, None
        else :
            raise Exception ("_find_leaf error")

    def _check_format(self, auto_form):
        """
        convert auto format which include automl flag and ranges
        to real conf data
        :param auto_form:
        :return:
        """
        if (type(auto_form) is not dict or auto_form.get("auto") == None) :
            return False
        else :
            return True

    def _format_conv(self, auto_form):
        """
        convert auto format which include automl flag and ranges
        to real conf data
        :param auto_form:
        :return:
        """
        try :
            if(auto_form.get('auto') == False) :
                if(type(auto_form.get('option')) == list) :
                    return auto_form.get('option')
                elif(type(auto_form.get('option')) == str) :
                    return auto_form.get('option')
                elif (type(auto_form.get('option')) == int):
                    return auto_form.get('option')
            else :
                if(auto_form.get('option') == None) :
                    st, en, ir = auto_form.get('auto')
                    if(type(st) == float or type(en) == float or type(ir) == float) :
                        return random.uniform(st, en)
                    else :
                        if(en > st) :
                            return random.randrange(st, en, ir)
                        else :
                            return random.randrange(en, st, ir)
                elif(type(auto_form.get('option')) == list) :
                    st, en, ir = auto_form.get('auto')
                    num =  random.randrange(st, en, ir)
                    return auto_form.get('option')[num]
                else :
                    return auto_form.get('option')
        except Exception as e :
            raise Exception ("error on automl format conv : {0}".format(e))

    def get_all_nodes_list(self, nn_id, wf_ver):
        """
        get execute class path
        :param node_id:
        :return:
        """
        # make query string (use raw query only when cate is too complicated)
        try:
            query_list = []
            query_list.append("SELECT ND.nn_wf_node_id, ND.wf_task_submenu_id_id, SB.wf_task_menu_id_id, ND.nn_wf_node_name   ")
            query_list.append("FROM  master_NN_WF_NODE_INFO ND JOIN master_WF_TASK_SUBMENU_RULE SB   ")
            query_list.append("      ON ND.wf_task_submenu_id_id =  SB.wf_task_submenu_id   ")
            query_list.append("WHERE ND.wf_state_id_id = %s")

            # parm_list : set parm value as list
            parm_list = []
            parm_list.append(str(nn_id) + "_" + str(wf_ver))

            with connection.cursor() as cursor:
                cursor.execute(''.join(query_list), parm_list)
                row = dictfetchall(cursor)
            return row
        except Exception as e:
            raise Exception(e)
