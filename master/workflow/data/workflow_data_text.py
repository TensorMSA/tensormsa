from master.workflow.data.workflow_data import WorkFlowData
from common import utils
from master import models
import os

class WorkFlowDataText(WorkFlowData) :
    """
    1. Definition
    Reuse already saved as HDF5 format
    2. Tables
    NN_WF_NODE_INFO (NODE_CONFIG_DATA : Json Field)
    """

    def __init__(self, key = None):
        """
        init key variable
        :param key:
        :return:
        """
        self.key = key


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

    def get_step_source(self):
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

    def get_sql_stmt(self):
        """

        :param nnid:
        :param wfver:
        :param node:
        :return:
        """
        if('conf' not in self.__dict__) :
            self.conf = self.get_step_source()
        return self.conf.get('source_sql')

    def get_src_type(self):
        """

        :param nnid:
        :param wfver:
        :param node:
        :return:
        """
        if ('conf' in self.__dict__):
            self.conf = self.get_step_source()
        return self.conf.get('source_type')

    def get_src_server(self):
        """

        :param nnid:
        :param wfver:
        :param node:
        :return:
        """
        if ('conf' in self.__dict__):
            self.conf = self.get_step_source()
        return self.conf.get('source_server')

    def get_parse_type(self):
        """

        :param nnid:
        :param wfver:
        :param node:
        :return:
        """
        if ('conf' in self.__dict__):
            self.conf = self.get_step_source()
        return self.conf.get('source_parse_type')

    def get_source_path(self):
        """

        :param nnid:
        :param wfver:
        :param node:
        :return:
        """
        if ('conf' in self.__dict__):
            self.conf = self.get_step_source()
        return self.conf.get('source_path')

    def check_step_source(self, obj):
        """
        check step_source process fit to requirement
        :param obj: config data from view
        :return:boolean
        """
        error_msg = ""

        if ('source_type' not in obj):
            error_msg = ''.join([error_msg, 'source_type (local, hadoop, s3, rdb) not defined'])

        if(obj['source_type'] == 'local') :
            if ('max_sentence_len' not in obj):
                error_msg = ''.join([error_msg, 'max_sentence_len (inteager length of sent) not defined'])
            if ('source_parse_type' not in obj):
                error_msg = ''.join([error_msg, 'source_parse_type (raw, excel) not defined'])

        if (obj['source_type'] in ['rdb', 'hbase', 's3']):
            if ('source_parse_type' not in obj):
                error_msg = ''.join([error_msg, 'source_parse_type (raw, excel) not defined'])
            if ('source_server' not in obj):
                error_msg = ''.join([error_msg, 'source_server (local or server management id) not defined'])
            if ('source_sql' not in obj):
                error_msg = ''.join([error_msg, 'source_sql (query string) not defined'])
            if ('source_path' not in obj):
                error_msg = ''.join([error_msg, 'source_path (source path string) not defined'])
            if ('max_sentence_len' not in obj):
                error_msg = ''.join([error_msg, 'max_sentence_len (inteager length of sent) not defined'])

        if (error_msg == ""):
            return True
        else:
            raise Exception(error_msg)

    def put_step_source(self, src, form, nnid, wfver, node, input_data):
        """
        putter for source step
        :param obj: config data from view
        :return:boolean
        """
        try:
            if(src == 'local') :
                source_path = utils.get_source_path(nnid, wfver, node)
                return self.update_wf_node_info(src, form, nnid, wfver, node, input_data, source_path)

        except Exception as e:
            raise Exception(e)

    def update_wf_node_info(self, src, form, nnid, wfver, node, input_data, source_path):
        """

        :param src:
        :param form:
        :param nnid:
        :param wfver:
        :param node:
        :param input_data:
        :return:
        """
        obj = models.NN_WF_NODE_INFO.objects.get(nn_wf_node_id=str(nnid) + "_" + str(wfver) + "_" + str(node))
        config_data = getattr(obj, 'node_config_data')
        config_data['source_type'] = src
        config_data['source_parse_type'] = form
        config_data['source_server'] = input_data['source_server']
        config_data['source_sql'] = input_data['source_sql']
        config_data['source_path'] = source_path
        config_data['max_sentence_len'] = input_data['max_sentence_len']
        setattr(obj, 'node_config_data', config_data)
        obj.save()

        if (os.path.exists(source_path) == False):
            os.makedirs(source_path, exist_ok=True)

        return config_data

    def get_step_preprocess(self):
        """
        getter for preprocess
        :return:obj(json) to make view
        """

        try:
            if ('conf' in self.__dict__):
                self.conf = self.get_step_source()
            return self.conf['preprocess']
        except Exception as e:
            raise Exception(e)

    def check_step_preprocess(self, obj):
        """

        :param obj:
        :return:
        """
        error_msg = ""

        if ('preprocess' not in obj):
            error_msg = ''.join([error_msg, 'preprocess type (mecab, kkma) not defined'])

        if (error_msg == ""):
            return True
        else:
            raise Exception(error_msg)


    def put_step_preprocess(self, src, form, nnid, wfver, node, input_data):
        """
        putter for preprocess
        :param obj: config data from view
        :return:boolean
        """
        try:
            self.check_step_preprocess(input_data)
            obj = models.NN_WF_NODE_INFO.objects.get(nn_wf_node_id=str(nnid) + "_" + str(wfver) + "_" + str(node))
            config_data = getattr(obj, 'node_config_data')
            config_data['preprocess'] = input_data['preprocess']
            setattr(obj, 'node_config_data', config_data)
            obj.save()
            return input_data['preprocess']
        except Exception as e:
            raise Exception(e)

    def get_step_store(self):
        """
        getter for store
        :return:obj(json) to make view
        """
        try:
            if ('conf' in self.__dict__):
                self.conf = self.get_step_source()
            return self.conf['store_path']
        except Exception as e:
            raise Exception(e)

    def check_step_store(self, obj):
        """

        :param obj:
        :return:
        """
        return True

    def put_step_store(self, src, form, nnid, wfver, node, input_data):
        """
        putter for store
        :param obj: config data from view
        :return:boolean
        """
        try:
            self.check_step_store(input_data)
            store_path = utils.get_store_path(nnid, wfver, node)
            obj = models.NN_WF_NODE_INFO.objects.get(nn_wf_node_id=str(nnid) + "_" + str(wfver) + "_" + str(node))
            config_data = getattr(obj, 'node_config_data')
            config_data['store_path'] = utils.get_store_path(nnid, wfver, node)
            setattr(obj, 'node_config_data', config_data)
            obj.save()

            if (os.path.exists(store_path) == False):
                os.makedirs(store_path, exist_ok=True)

            return config_data['store_path']

        except Exception as e:
            raise Exception(e)

    def get_max_sent_len(self):
        """
        getter for store
        :return:obj(json) to make view
        """
        try:
            if ('conf' in self.__dict__):
                self.conf = self.get_step_source()
            return self.conf['max_sentence_len']
        except Exception as e:
            raise Exception(e)