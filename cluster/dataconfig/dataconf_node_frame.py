from cluster.dataconfig.dataconf_node import DataConfNode
from master.workflow.dataconf.workflow_dataconf_frame import WorkflowDataConfFrame

class DataConfNodeFrame(DataConfNode):
    """

    """

    def run(self, conf_data):
        try:
            self._init_node_parm(conf_data['node_id'])
            print("data_conf : " + str(self.data_conf))
            return None
        except Exception as e:
            raise Exception(e)

    def _init_node_parm(self):
        return None

    def _set_progress_state(self):
        return None

    def _init_node_parm(self, key):
        """
        Init parameter from workflow_data_frame
        :return:
        """
        wf_data_conf = WorkflowDataConfFrame(key)
        self.data_conf = wf_data_conf.data_conf
