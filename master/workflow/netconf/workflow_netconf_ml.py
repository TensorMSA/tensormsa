from master.workflow.netconf.workflow_netconf import WorkFlowNetConf
from master import models
from common.utils import *

class WorkFlowNetConfML(WorkFlowNetConf):
    """

    """

    @property
    def model_path(self):
        """
        getter for preprocess
        """
        return self.conf['model_path']

    @property
    def ml_class(self):
        """
        getter for preprocess
        """
        return self.conf['ml_class']

    @property
    def config(self):
        """
        getter for preprocess
        """
        return self.conf['config']

    @property
    def model_type(self):
        """
        getter for preprocess
        """
        return self.conf['model_type']


    def __init__(self, key = None):
        """
        init key variable
        :param key:
        :return:
        """
        if key is not None :
            self.key = key
            self.conf = self.get_step_source(key)

        self._set_prhb_parms(['model_path', 'encoder_len', 'decoder_len','encoder_depth', 'cell_type'])

    def validation_check(self, json_data):
        error_msg = ""
        if ('model_path' not in json_data):
            error_msg = ''.join([error_msg, 'model_path (str) not defined'])
        if ('ml_class' not in json_data):
            error_msg = ''.join([error_msg, 'ml_class (str) not defined'])
        if ('config' not in json_data):
            error_msg = ''.join([error_msg, 'config (dic) not defined'])
        if (error_msg == ""):
            return True
        else:
            return error_msg

    def get_step_source(self, nnid):
        """
        getter for source step
        :return:obj(json) to make view
        """
        try:
            obj = models.NN_WF_NODE_INFO.objects.get(nn_wf_node_id=self.key)
            config_data = getattr(obj, 'node_config_data')
            return config_data
        except Exception as e:
            raise Exception(e)

    def set_view_obj(self, nnid, ver, node, input_data):
        """
        set net config data edited on view
        :param nnid, ver, node, input_data:
        :return:
        """
        try:
            if (self.validation_check(input_data)):
                obj = models.NN_WF_NODE_INFO.objects.get(nn_wf_node_id=str(nnid) + "_" + str(ver) + "_" + str(node))
                config_data = getattr(obj, 'node_config_data')
                config_data['model_path'] = get_model_path(nnid, ver, node)
                config_data['ml_class'] = input_data['ml_class']
                config_data['config'] = input_data['config']
                config_data['model_type'] = input_data['model_type']
                setattr(obj, "node_config_data", config_data)
                obj.save()
            return input_data
        except Exception as e:
            raise Exception(e)

    def config_data_nvl_bool(self, config_data, attribute_name):

        if attribute_name in config_data:
            _value = config_data[attribute_name]
        else:
            _value = False
        return _value


    def get_drop_out(self):
        """

        :param node_id:
        :return:
        """
        if ('conf' not in self.__dict__):
            self.conf = self.get_view_obj(self.key)
        return self.conf['drop_out']


