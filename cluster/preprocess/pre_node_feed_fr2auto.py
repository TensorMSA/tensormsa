from cluster.preprocess.pre_node_feed import PreNodeFeed
from master.workflow.preprocess.workflow_feed_fr2auto import WorkflowFeedFr2Auto
import pandas as pd
import warnings
import numpy as np

class PreNodeFeedFr2Auto(PreNodeFeed):
    """

    """

    def run(self, conf_data):
        """
        override init class
        """
        super(PreNodeFeedFr2Auto, self).run(conf_data)
        self._init_node_parm(conf_data['node_id'])

    def _init_node_parm(self, node_id):
        """

        :param node_id:
        :return:
        """
        try:
            wf_conf = WorkflowFeedFr2Auto(node_id)
            self.encode_col = wf_conf.get_encode_column()
            self.encode_len = wf_conf.get_encode_len()
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
            count = index.stop - index.start
            if(self.encode_col in chunk) :
                encode = self.encode_pad(self._preprocess(chunk[self.encode_col].values)[0:count], max_len=self.encode_len)
                return encode
            else :
                warnings.warn("not exists column names requested !!")
                return [['#'] * self.encode_len], [['#'] * self.decode_len]
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
