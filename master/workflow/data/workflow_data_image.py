from master.workflow.data.workflow_data import WorkFlowData
from master import models
from common.utils import *

class WorkFlowDataImage(WorkFlowData) :
    """
    1. Definition
    handle preview and settings for image data
    2. Tables
    NN_WF_NODE_INFO (NODE_CONFIG_DATA : Json Field) 
    """

    def get_preview_data(self):
        """

        :param type:
        :param conn:
        :return:
        """
        return None


    def set_preview_data(self):
        """

        :param type:
        :param conn:
        :return:
        """
        return None

    def get_data(self):
        """

        :param type:
        :param conn:
        :return:
        """
        return None


    def put_step_source_ori(self, node_id, config_data):
        """

        :param type:
        :param conn:
        :return:
        """
        try:
            obj = models.NN_WF_NODE_INFO.objects.get(nn_wf_node_id=node_id)
            setattr(obj, 'node_config_data', config_data)
            obj.save()
            return config_data

        except Exception as e:
            raise Exception(e)
        return None


    def get_step_source(self, node_id):
        """
        getter for source step
        :return:obj(json) to make view
        """
        try:
            obj = models.NN_WF_NODE_INFO.objects.get(nn_wf_node_id=node_id)
            config_data = getattr(obj, 'node_config_data')

        except Exception as e:
            raise Exception(e)
        return config_data

    def put_step_source(self, nnid, wfver, node, config_data):
        """
        putter for source step
        :param obj: config data from view
        :return:boolean
        """

        try:
            obj = models.NN_WF_NODE_INFO.objects.get(wf_state_id=str(nnid) + "_" + str(wfver), nn_wf_node_name=node)
            # old_config_data = getattr(obj, 'node_config_data')
            # if('labels' in old_config_data) :
            #     config_data["labels"] = old_config_data["labels"]
            config_data["source_path"] = get_source_path(nnid, wfver, node)
            config_data["store_path"] = get_store_path(nnid, wfver, node)
            setattr(obj, 'node_config_data', config_data)
            obj.save()
            return config_data

        except Exception as e:
            raise Exception(e)

    def get_data_node_info(self, nnid, wfver, submenu_id):
        """
        getter for source step
        :return:obj(json) to make view
        """
        try:
            obj = models.NN_WF_NODE_INFO.objects.filter(wf_state_id_id=str(nnid) + "_" + str(wfver), wf_task_submenu_id_id=submenu_id)
            return_data = {}
            i = 0
            for config in obj:
                return_data_sub = {}
                return_data_sub['nn_wf_node_id'] = getattr(config, 'nn_wf_node_id')
                return_data_sub['nn_wf_node_name'] = getattr(config, 'nn_wf_node_name')
                return_data_sub['nn_wf_node_desc'] = getattr(config, 'nn_wf_node_desc')
                return_data["data"+str(i)] = return_data_sub
                i += 1
        except Exception as e:
            raise Exception(e)

        return return_data

    def get_step_preprocess(self):
        """
        getter for preprocess
        :return:obj(json) to make view
        """
        return None

    def put_step_preprocess(self, obj):
        """
        putter for preprocess
        :param obj: config data from view
        :return:boolean
        """
        return None

    def get_step_store(self):
        """
        getter for store
        :return:obj(json) to make view
        """
        return None

    def put_step_store(self, obj):
        """
        putter for store
        :param obj: config data from view
        :return:boolean
        """
        return None

    def _get_lable_list(self):
        """

        :return:
        """
        return []

    def _get_preview_urls(self):
        """

        :return:
        """
        return []


    def _insert_preview_images(self):
        """

        :return:
        """
        return None

    def _set_preivew_paths(self, preview_path_list):
        """

        :param preview_path_list:
        :return:
        """
        return None

    def _set_lable_list(self, lable_list):
        """

        :param lable_list:
        :return:
        """
        return None
