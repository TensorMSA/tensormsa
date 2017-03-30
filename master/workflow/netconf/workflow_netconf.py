from common.utils import *
from master import models

class WorkFlowNetConf :

    def get_node_status(self):
        """
        return node status info (nn_id, nn_ver, node_type, node_prg, etc)
        :return:
        """
        return None

    def get_related_node_status(self):
        """
        get related node info (especially data node)
        :return:object (related node's data info)
        """
        return None

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
            self.validation_check(input_data)
            obj = models.NN_WF_NODE_INFO.objects.get(nn_wf_node_id=node_id)
            nn_id = input_data["key"]["nn_id"]
            wfver = input_data["key"]["wf_ver_id"]
            node = input_data["key"]["node"]
            input_data["modelpath"] = get_model_path(nn_id, wfver, node)
            input_data["modelname"] = "model_"+nn_id+"_"+wfver
            setattr(obj, "node_config_data", input_data)
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
        pass

