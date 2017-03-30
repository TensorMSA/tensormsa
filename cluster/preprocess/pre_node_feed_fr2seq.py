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
            store = pd.HDFStore(file_path)
            chunk = store.select('table1',
                               start=index.start,
                               stop=index.stop)
            encode = self._preprocess(chunk[self.encode_col])
            decode = self._preprocess(chunk[self.decode_col])

            return encode, decode
        except Exception as e :
            raise Exception (e)
        finally:
            store.close()

    def _preprocess(self, input_data):
        """

        :param input_data:
        :return:
        """
        if(self.preprocess_type == 'mecab') :
            return self._mecab_parse(input_data)
        elif (self.preprocess_type == 'kkma'):
            return self._mecab_parse(input_data)
        elif (self.preprocess_type == 'twitter'):
            return self._mecab_parse(input_data)
        else :
            return input_data

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