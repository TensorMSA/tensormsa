from master.workflow.data.workflow_data import WorkFlowData
from master import models
from common import utils


class WorkFlowDataFrame(WorkFlowData) :
    """
    1. Definition
    handle preview and settings for frame data
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


    @property
    def object_type(self):
        """
        getter for object type
        """
        return self.get_step_source(self.key)['type']

    @property
    def sql_stmt(self):
        """
        getter for sql_statement
        """
        return self.get_step_source(self.key)['source_sql']

    @property
    def source_path(self):
        """
        getter for source_path
        """
        return self.get_step_source(self.key)['source_path']

    @property
    def src_type(self):
        """
        getter for source type
        """
        return self.get_step_source(self.key)['source_type']

    @property
    def src_server(self):
        """
        getter for source_server
        """
        return self.get_step_source(self.key)['source_server']

    @property
    def step_preprocess(self):
        """
        getter for preprocess
        """
        return self.get_step_source(self.key)['preprocess']

    @property
    def step_store(self):
        """
        getter for store
        """
        return self.get_step_source(self.key)['store_path']

    def get_preview_data(self):
        """

        :param self:
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

    def put_step_source(self, src, form, prg, nnid, wfver, node,input_data):
        """
        putter for source step
        :param obj: config data from view
        :return:boolean
        """

        try:
            #obj = models.NN_WF_NODE_INFO.objects.get(wf_state_id=str(nnid) + "_" + str(wfver), nn_wf_node_name='data_node')


            obj = models.NN_WF_NODE_INFO.objects.get(nn_wf_node_id=str(nnid) + "_" + str(wfver) + "_" + str(node))
            config_data = getattr(obj, 'node_config_data')
            config_data['type'] = input_data['type']
            config_data['source_type'] = src
            config_data['source_parse_type'] = form
            config_data['source_server'] = input_data['source_server']
            config_data['source_sql'] = input_data['source_sql']
            config_data['source_path'] = utils.get_source_path(nnid, wfver, input_data['source_path'])
            setattr(obj, 'node_config_data', config_data)
            obj.save()

            setattr(obj, 'node_config_data', config_data)
            obj.save()
            return config_data

        except Exception as e:
            raise Exception(e)


    def put_step_preprocess(self, src, form, prg, nnid, wfver, node,input_data):
        """
        putter for preprocess
        :param obj: config data from view
        :return:boolean
        """
        try:
            obj = models.NN_WF_NODE_INFO.objects.get(nn_wf_node_id=str(nnid) + "_" + str(wfver) + "_" + str(node))
            config_data = getattr(obj, 'node_config_data')
            config_data['preprocess'] = input_data['preprocess']
            setattr(obj, 'node_config_data', config_data)
            obj.save()
            return input_data['preprocess']

        except Exception as e:
            raise Exception(e)


    def put_step_store(self, src, form, prg, nnid, wfver, node,input_data):
        """
        putter for store
        :param obj: config data from view
        :return:boolean
        """
        try:
            obj = models.NN_WF_NODE_INFO.objects.get(nn_wf_node_id=str(nnid) + "_" + str(wfver) + "_" + str(node))
            config_data = getattr(obj, 'node_config_data')
            config_data['store_path'] = utils.get_store_path(nnid, input_data['store_path'])
            setattr(obj, 'node_config_data', config_data)
            obj.save()
            return input_data['store_path']

        except Exception as e:
            raise Exception(e)

    def _load_local_frame(self, conn):

        return None

    def _load_s3_frame(self, conn):

        return None

    def _load_rdb_frame(self, conn):

        return None

    def _load_hbase_frame(self, conn):

        return None

    def _set_default_column_type(self):

        return None