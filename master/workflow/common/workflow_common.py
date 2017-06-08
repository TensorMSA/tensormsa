from common.utils import *
from master import models


class WorkFlowCommon:
    """
    parent class for all workflow classes
    """
    def get_view_obj(self, node_id):
        """
        get view data for net config
        :return:
        """
        # node_id = input_data["key"]["node_id"]

        try:
            obj = models.NN_WF_NODE_INFO.objects.get(nn_wf_node_id=node_id)
            data_set = getattr(obj, "node_config_data")
            return data_set
        except Exception as e:
            raise Exception(e)

    def set_view_obj(self, node_id, input_data):
        """
        set net config data edited on view
        :param obj:
        :return:
        """
        try:
            #TODO : remove after lunching runtime
            #self.validation_check(input_data)
            #self.restriction_check(node_id, input_data)
            obj = models.NN_WF_NODE_INFO.objects.get(nn_wf_node_id=node_id)
            setattr(obj, "node_config_data", input_data)
            obj.save()
            return input_data
        except Exception as e:
            raise Exception(e)
        return None

    def update_view_obj(self, node_id, input_data):
        """
        set net config data edited on view
        :param obj:
        :return:
        """
        try:
            obj = models.NN_WF_NODE_INFO.objects.get(nn_wf_node_id=node_id)
            data_set = getattr(obj, "node_config_data")
            data_set.update(input_data)
            setattr(obj, "node_config_data", data_set)
            obj.save()
            return input_data
        except Exception as e:
            raise Exception(e)
        return None

    def get_state_id(self, node_id):
        try:
            obj = models.NN_WF_NODE_INFO.objects.get(nn_wf_node_id=node_id)
            return obj.wf_state_id
        except Exception as e:
            raise Exception(e)

    def validation_check(self, json_data):
        """
        check if necessray parms are all set
        :param json_data:
        :return:
        """
        if('type' in json_data):
            filter_list = self._get_key_parms(type=json_data.get('type'))
        else :
            filter_list = self._get_key_parms()

        if(filter_list is not None):
            match_list = list(set(json_data.keys()).intersection(filter_list))
            req_list = list(set(filter_list) - set(match_list))
            error_msg = ""
            for key in req_list :
                error_msg = ''.join([error_msg, key , 'not defined\n'])
            if(len(error_msg) > 0) :
                raise Exception (error_msg)
        else:
            raise Exception('JSON Validation ERROR')

    def _get_key_parms(self, type='default'):
        """
        return update black list
        :return:
        """
        if(type in self.essence_parms) :
            return self.essence_parms.get(type)
        else :
            return None

    def _set_key_parms(self, lists, type='default'):
        """
        set update black list
        :param lists:
        :return:
        """
        self.essence_parms = {}
        self.essence_parms[type] = lists

    def restriction_check(self, node_id, json_data):
        """
        restirct user to modify cirical values may can occur problems on flow
        :param json_data:
        :return:
        """
        db_parm = self.get_view_obj(node_id)
        exists_list = list(set(json_data).intersection(db_parm))
        black_list = self._get_prhb_parms()

        if(len(list(set(black_list).intersection(exists_list))) > 0) :
            raise Exception("you cannot change critical values, create new version for diffrent model")

    def _get_prhb_parms(self):
        """
        return update black list
        :return:
        """
        if(self.update_black_list) :
            return self.update_black_list
        else :
            return []

    def _set_prhb_parms(self, lists):
        """
        set update black list
        :param lists:
        :return:
        """
        self.update_black_list = lists


