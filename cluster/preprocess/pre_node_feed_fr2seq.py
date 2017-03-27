from cluster.preprocess.pre_node_feed import PreNodeFeed
from master.workflow.preprocess.workflow_feed_fr2seq import WorkflowFeedFr2Seq
import pandas as pd

class PreNodeFeedFr2Seq(PreNodeFeed):
    """

    """

    def _init_node_parm(self, node_id):
        """

        :param node_id:
        :return:
        """
        try:
            wf_conf = WorkflowFeedFr2Seq(node_id)
            self.encode_col = wf_conf.get_encode_column()
            self.decode_col = wf_conf.get_decode_column()
        except Exception as e:
            raise Exception(e)

    def _convert_data_format(self, file_path, index):
        """

        :param obj:
        :param index:
        :return:
        """
        store = pd.HDFStore(file_path)
        chunk = store.select('table1',
                           start=index.start,
                           stop=index.stop)
        store.close()
        return chunk[self.encode_col], chunk[self.decode_col]

