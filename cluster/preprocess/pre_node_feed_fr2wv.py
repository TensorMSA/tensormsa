from cluster.preprocess.pre_node_feed import PreNodeFeed
from master.workflow.preprocess.workflow_feed_fr2wv import WorkflowFeedFr2Wv
import pandas as pd
import numpy as np

class PreNodeFeedFr2Wv(PreNodeFeed):
    """

    """

    def run(self, conf_data):
        """
        override init class
        """
        super(PreNodeFeedFr2Wv, self).run(conf_data)
        self._init_node_parm(conf_data['node_id'])

    def _init_node_parm(self, node_id):
        """

        :param node_id:
        :return:
        """
        try:
            wf_conf = WorkflowFeedFr2Wv(node_id)
            self.column_list = wf_conf.get_column_list()
            self.sent_max_len = wf_conf.get_sent_max_len()
            self.preprocess_type = wf_conf.get_preprocess_type()
        except Exception as e:
            raise Exception(e)

    def _convert_data_format(self, file_path, index):
        """

        :param obj:
        :param index:
        :return:
        """
        try :
            return_data = []
            store = pd.HDFStore(file_path)
            chunk = store.select('table1',
                               start=index.start,
                               stop=index.stop)

            for column in self.column_list :
                for line in self._preprocess(chunk[column].values)[index.start:index.stop] :
                    return_data = return_data + line
            return [return_data]
        except Exception as e :
            raise Exception (e)
        finally:
            store.close()

    def data_size(self):
        """
        get data array size of this calss
        :return:
        """
        try :
            store = pd.HDFStore(self.input_paths[self.pointer])
            table_data = store.select('table1')
            return table_data[table_data.columns.values[0]].count()
        except Exception as e :
            raise Exception (e)
        finally:
            store.close()