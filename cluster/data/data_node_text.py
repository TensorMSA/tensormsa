from cluster.data.data_node import DataNode
from master.workflow.data.workflow_data_text import WorkFlowDataText
from konlpy.tag import Kkma
import konlpy, jpype

class DataNodeText(DataNode):
    """

    """

    def run(self, conf_data):
        """

        :param conf_data:
        :return:
        """
        self._init_node_parm(conf_data)
        kkma = Kkma()
        pos = kkma.pos(u'원칙이나 기체 설계와 엔진·레이더·항법장비 등')
        print(pos)
        return pos

    def _init_node_parm(self, key):
        """

        :return:
        """
        wf_conf = WorkFlowDataText(key)
        self.data_sql_stmt = wf_conf.get_sql_stmt()
        self.data_src_type = wf_conf.get_src_type()
        self.data_server_type = wf_conf.get_src_server()
        self.data_parse_type = wf_conf.get_parse_type()
        self.data_preprocess_info = wf_conf.get_step_preprocess()
        self.data_store_path = wf_conf.get_step_store()

    def _set_progress_state(self):
        return None