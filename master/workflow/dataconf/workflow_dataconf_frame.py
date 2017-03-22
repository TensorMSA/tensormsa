from master.workflow.dataconf.workflow_dataconf import WorkFlowDataConf
from common import utils
from master import models

class WorkflowDataConfFrame(WorkFlowDataConf):
    """
    Data Columns의 속성을 정의 해주는 Class
    # properties
        data_conf
    """
    def __init__(self, key = None):
        """
        init key variable
        :param key:
        :return:
        """
        if (key is not None):
            self.key = key
            self.conf = self.get_step_source(key)

    #data_conf
    def get_view_obj(self):
        """
        get column type info for view
        :return:
        """
        self._get_default_type()
        self._get_modified_type()

        return None

    def set_view_obj(self, obj):
        """
        set column type info on db json filed
        :param obj:
        :return:
        """
        return None

    def _get_default_type(self):
        """

        :return:
        """
        return None

    def _get_modified_type(self):
        """

        :return:
        """
        return None

    def _set_default_type(self):
        """

        :return:
        """
        return None

    def _set_modified_type(self):
        """

        :return:
        """
        return None

    def put_step_source(self,nnid, ver, node, input_data):
        """
        putter for source step
        :param obj: config data from view
        :return:boolean
        """

        try:
            #obj = models.NN_WF_NODE_INFO.objects.get(wf_state_id=str(nnid) + "_" + str(wfver), nn_wf_node_name='data_node')

            config_data = input_data
            obj = models.NN_WF_NODE_INFO.objects.get(nn_wf_node_id=str(nnid) + "_" + str(ver) + "_" + str(node))
            config_data = getattr(obj, 'node_config_data')
            config_data['data_conf'] = input_data
            #config_data['source_parse_type'] = form
            #config_data['source_server'] = input_data['source_server']
            #config_data['source_sql'] = input_data['source_sql']
            #config_data['source_path'] = utils.get_source_path(nnid, ver, input_data['source_path'])
            setattr(obj, 'node_config_data', config_data)
            obj.save()

            #setattr(obj, 'node_config_data', config_data)
            #obj.save()
            return config_data

        except Exception as e:
            raise Exception(e)
