from cluster.preprocess.pre_node_feed import PreNodeFeed
from master.workflow.preprocess.workflow_feed_fr2wcnn import WorkflowFeedFr2Wcnn
import pandas as pd
import warnings
import numpy as np
from konlpy.tag import Mecab
from common.utils import *

class PreNodeFeedFr2Wcnn(PreNodeFeed):
    """

    """

    def run(self, conf_data):
        """
        override init class
        """
        super(PreNodeFeedFr2Wcnn, self).run(conf_data)
        self._init_node_parm(conf_data['node_id'])

    def _get_node_parm(self, node_id):
        """
        return conf master class
        :return:
        """
        return WorkflowFeedFr2Wcnn(node_id)

    def _init_node_parm(self, node_id):
        """

        :param node_id:
        :return:
        """
        try:
            wf_conf = WorkflowFeedFr2Wcnn(node_id)
            self.wf_conf = wf_conf
            self.encode_channel = wf_conf.get_encode_channel
            self.encode_col = wf_conf.get_encode_column
            self.encode_len = wf_conf.get_encode_len
            self.decode_col = wf_conf.get_decode_column
            self.lable_size = wf_conf.get_lable_size
            self.char_embed = wf_conf.char_encode
            self.char_max_len = wf_conf.char_max_len
            self.lable_onehot = OneHotEncoder(self.lable_size)
            if (wf_conf.get_lable_list):
                self.lable_onehot.restore(wf_conf.get_lable_list)
            self.preprocess_type = wf_conf.get_preprocess_type
            self.embed_type = wf_conf.get_embed_type
            self.vocab_size = wf_conf.get_vocab_size + 4
            self.char_embed_size = 160
            if (self.char_embed == True) :
                self.word_vector_size = self.vocab_size + (self.char_embed_size * self.char_max_len)
            else :
                self.word_vector_size = self.vocab_size
            if(self.embed_type == 'onehot') :
                self.input_onehot = OneHotEncoder(self.vocab_size)
                if (wf_conf.get_vocab_list):
                    self.input_onehot.restore(wf_conf.get_vocab_list)
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
            if(self.encode_col in chunk and self.decode_col in chunk) :
                words = self.encode_pad(self._preprocess(chunk[self.encode_col].values)[0:count], max_len=self.encode_len)
                if(self.char_embed) :
                    encode = self._word_embed_data(self.embed_type, words, cls=self.input_onehot, char_embed=True )
                else :
                    encode = self._word_embed_data(self.embed_type, words, cls=self.input_onehot, char_embed=False)
                    encode = np.array(encode).reshape([-1, self.encode_len, self.word_vector_size, self.encode_channel])
                decode = np.array(chunk[self.decode_col].values).reshape([-1,1]).tolist()
                return encode, self._word_embed_data(self.embed_type, decode, cls=self.lable_onehot)
            else :
                raise Exception ("WCNN Data convert error : no column name exists")
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
            return list(map(lambda x : x.split(' '), input_data.tolist()))

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

    def has_next(self):
        """
        check if hdf5 file pointer has next
        :return:
        """
        if(len(self.input_paths) > self.pointer) :
            return True
        else :
            self.wf_conf.set_lable_list(self.lable_onehot.dics())
            self.wf_conf.set_word_vector_size(self.word_vector_size)
            self.wf_conf.set_char_embed(self.char_embed)
            self.wf_conf.set_char_max_len(self.char_max_len)
            self.wf_conf.set_encode_len(self.encode_len)
            self.wf_conf.set_encode_channel(self.encode_channel)
            self.wf_conf.set_char_embed_size(self.char_embed_size)
            if (self.embed_type == 'onehot'):
                self.wf_conf.set_vocab_list(self.input_onehot.dics())
            return False
