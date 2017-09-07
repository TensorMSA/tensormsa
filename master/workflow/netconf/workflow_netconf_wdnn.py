from master.workflow.netconf.workflow_netconf import WorkFlowNetConf
from master import models
from common.utils import *


class WorkFlowNetConfWdnn(WorkFlowNetConf):
    """

    """

    @property
    def model_path(self):
        """
        getter for preprocess
        """
        return self.conf['model_path']

    @property
    def hidden_layers(self):
        """
        getter for preprocess
        """
        return self.conf['hidden_layers']

    @property
    def activation_function(self):
        """
        getter for preprocess
        """
        return self.conf['activation_function']

    @property
    def batch_size(self):
        """
        getter for preprocess
        """
        return self.conf['batch_size']

    @property
    def epoch(self):
        """
        getter for preprocess
        """
        return self.conf['epoch']


    @property
    def model_type(self):
        """
        getter for preprocess
        """
        return self.conf['model_type']
    @property
    def train(self):
        """
        getter for preprocess
        """
        return self.conf['train'] if hasattr(self.conf,'train') else True

    @property
    def auto_demension(self):
        """
        getter for preprocess
        """
        return self.conf['auto_demension'] if hasattr(self.conf,'auto_demension') else True


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
        # if ('encoder_len' not in json_data):
        #     error_msg = ''.join([error_msg, 'encoder_len (int) not defined'])
        # if ('decoder_len' not in json_data):
        #     error_msg = ''.join([error_msg, 'decoder_len (int) not defined'])
        # if ('encoder_depth' not in json_data):
        #     error_msg = ''.join([error_msg, 'encoder_depth (int) not defined'])
        # if ('decoder_depth' not in json_data):
        #     error_msg = ''.join([error_msg, 'decoder_depth (int) not defined'])
        # if ('cell_type' not in json_data):
        #     error_msg = ''.join([error_msg, 'cell_type (str) (vanila, lstm, gru) not defined'])
        # if ('drop_out' not in json_data):
        #     error_msg = ''.join([error_msg, 'drop_out (float) not defined'])
        # if ('word_embed_type' not in json_data):
        #     error_msg = ''.join([error_msg, 'word_embed_type (str) (w2v, onehot)not defined'])
        # if ('word_embed_id' not in json_data):
        #     error_msg = ''.join([error_msg, 'word_embed_id (str) (net id) not defined'])
        if ('hidden_layers' not in json_data):
            error_msg = ''.join([error_msg, 'hidden_layers (list) (net id) not defined'])
        if ('activation_function' not in json_data):
            error_msg = ''.join([error_msg, 'activation_function (str) (net id) not defined'])
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
                config_data['hidden_layers'] = input_data['hidden_layers']
                config_data['activation_function'] = input_data['activation_function']
                config_data['batch_size'] = input_data['batch_size']
                config_data['epoch'] = input_data['epoch']
                config_data['model_type'] = input_data['model_type']
                config_data['train'] = input_data['train']
                config_data['auto_demension'] = input_data['auto_demension']  if 'auto_demension' in input_data else self.config_data_nvl_bool(config_data,
                                                                                                       'auto_demension')
                # config_data['source_parse_type'] = form
                # config_data['source_server'] = input_data['source_server']
                # config_data['source_sql'] = input_data['source_sql']
                # config_data['source_path'] = utils.get_source_path(nnid, wfver, input_data['source_path'])
                # setattr(obj, 'node_config_data', config_data)
                setattr(obj, "node_config_data", config_data)
                obj.save()
            return input_data
        except Exception as e:
            #print(e)
            raise Exception(e)
        #return None

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


