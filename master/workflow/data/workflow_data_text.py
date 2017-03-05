from master.workflow.data.workflow_data import WorkFlowData
from common import utils
from master import models

class WorkFlowDataText(WorkFlowData) :
    """
    1. Definition
    Reuse already saved as HDF5 format
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


    def get_step_source(self, nnid, wfver, node):
        """
        getter for source step
        :return:obj(json) to make view
        """
        try:
            obj = models.NN_WF_NODE_INFO.objects.get(nn_wf_node_id=str(nnid) + "_" + str(wfver) + "_" + str(node))
            config_data = getattr(obj, 'node_config_data')
            return config_data
        except Exception as e:
            raise Exception(e)


    def put_step_source(self, src, form, nnid, wfver, node, input_data):
        """
        putter for source step
        :param obj: config data from view
        :return:boolean
        """
        try:
            obj = models.NN_WF_NODE_INFO.objects.get(nn_wf_node_id=str(nnid) + "_" + str(wfver) + "_" + str(node))
            config_data = getattr(obj, 'node_config_data')
            config_data['source_type'] = src
            config_data['source_parse_type'] = form
            config_data['source_server'] = input_data['source_server']
            config_data['source_sql'] = input_data['source_sql']
            config_data['source_path'] = utils.get_source_path(nnid, wfver, input_data['source_path'])
            setattr(obj, 'node_config_data', config_data)
            obj.save()
            return input_data['source_path']

        except Exception as e:
            raise Exception(e)


    def get_step_preprocess(self, nnid, wfver, node):
        """
        getter for preprocess
        :return:obj(json) to make view
        """

        try:
            obj = models.NN_WF_NODE_INFO.objects.get(nn_wf_node_id=str(nnid) + "_" + str(wfver) + "_" + str(node))
            config_data = getattr(obj, 'node_config_data')
            return config_data['preprocess']
        except Exception as e:
            raise Exception(e)


    def put_step_preprocess(self, src, form, nnid, wfver, node, input_data):
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


    def get_step_store(self, nnid, wfver, node):
        """
        getter for store
        :return:obj(json) to make view
        """
        try:
            obj = models.NN_WF_NODE_INFO.objects.get(nn_wf_node_id=str(nnid) + "_" + str(wfver) + "_" + str(node))
            config_data = getattr(obj, 'node_config_data')
            return config_data['store_path']
        except Exception as e:
            raise Exception(e)


    def put_step_store(self, src, form, nnid, wfver, node, input_data):
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