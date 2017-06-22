from master.automl.automl import AutoMlCommon
import random

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
        self.auto_ml_info = AutoMlCommon(nn_id)
        self.conf_info = self.auto_ml_info.conf_info
        self.train_info = self.auto_ml_info.train_info
        self.stat_info = self.auto_ml_info.stat_info

    def run(self):
        """
        run automl
        :return:
        """
        # Net Version create
        # TODO : Net Version check and create new
        # generate conf format for new train
        node_confs = self._generate_random_case(self.conf_info)
        # copy train data to new ver
        # TODO : copy train data to new ver
        # Find all nodes and set Data
        # TODO : find all nodes and set Data
        # run train with early termination
        # TODO : run train with early termination
        return node_confs

    def save_result(self):
        """
        save each train result
        :return:
        """
        pass

    def _generate_all_cases(self):
        """
        generate all cases on list
        :return: list + json form for neural network
        """
        pass

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
                if(type(auto_form.get('option')) == list and len(auto_form.get('option')) > 0) :
                    return auto_form.get('option')[0]
                elif(type(auto_form.get('option')) == str) :
                    return auto_form.get('option')
            else :
                if(auto_form.get('option') == None) :
                    st, en, ir = auto_form.get('auto')
                    if(type(st) == float or type(en) == float or type(ir) == float) :
                        return random.uniform(st, en) % ir
                    else :
                        if(en > st) :
                            return random.randrange(st, en)%ir
                        else :
                            return random.randrange(en, st) % ir
                elif(type(auto_form.get('option')) == list) :
                    st, en, ir = auto_form.get('auto')
                    num =  random.randrange(st, en)%ir
                    return auto_form.get('option')[num]
        except Exception as e :
            raise Exception ("error on automl format conv : {0}".format(e))
