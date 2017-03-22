from cluster.dataconfig.dataconf_node import DataConfNode
from master.workflow.dataconf.workflow_dataconf_frame import WorkflowDataConfFrame

class DataConfNodeFrame(DataConfNode):
    """
        Data Columns을 설정 하고 Validation Check가 필요함
        그러나 매번 Training을 할때는 필요 없음

        Validation check
            Category는 몇개냐
            Continuous에 문자값이 있으면 안됨

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
