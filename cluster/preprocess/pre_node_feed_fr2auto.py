from cluster.preprocess.pre_node_feed import PreNodeFeed
from master.workflow.preprocess.workflow_feed_fr2auto import WorkflowFeedFr2Auto
import pandas as pd
import warnings
import numpy as np
from functools import reduce
from konlpy.tag import Mecab
from common.utils import *

class PreNodeFeedFr2Auto(PreNodeFeed):
    """

    """

    def run(self, conf_data):
        """
        override init class
        """
        super(PreNodeFeedFr2Auto, self).run(conf_data)
        self._init_node_parm(conf_data['node_id'])

    def _get_node_parm(self, node_id):
        """
        return conf master class
        :return:
        """
        return WorkflowFeedFr2Auto(node_id)

    def _init_node_parm(self, node_id):
        """

        :param node_id:
        :return:
        """
        try:
            wf_conf = WorkflowFeedFr2Auto(node_id)
            self.wf_conf = wf_conf
            self.preprocess_type = wf_conf.get_preprocess_type()
            if (self.preprocess_type in ['frame']):
                self._init_frame_node_parm(wf_conf)
            elif (self.preprocess_type in ['mecab', 'kkma', 'twitter']):
                self._init_nlp_node_parm(wf_conf)

            insert_dict = {}
            for key in list(self.__dict__.keys()) :
                if key in ['preprocess_type','encode_col', 'encode_len', 'embed_type',
                           'word_vector_size', 'input_size','encode_dtype'] :
                    insert_dict[key] = self.__dict__[key]
            wf_conf.update_view_obj(node_id, insert_dict)
        except Exception as e:
            raise Exception(e)

    def _init_frame_node_parm(self, wf_conf):
        """
        init parms when data type is frame
        :param wf_conf:
        :return:
        """
        self.encode_col = wf_conf.get_encode_column()
        self.encode_len = {}
        self.encode_dtype = {}
        self.encode_onehot = {}
        self.embed_type = wf_conf.get_embed_type()
        self.word_vector_size = wf_conf.get_vocab_size() + 4
        self.input_size = 0
        if (self.embed_type == 'onehot'):
            if(wf_conf.get_vocab_list()) :
                encoder_value_list =  wf_conf.get_vocab_list()
                for col_name in list(encoder_value_list.keys()):
                    self.encode_onehot[col_name] = OneHotEncoder(self.word_vector_size)
                    self.encode_onehot[col_name].restore(encoder_value_list.get(col_name))
            self._init_frame_node_parm_with_data()

    def _init_frame_node_parm_with_data(self):
        """
        init pamr s need to be calculated
        :return:s
        """
        try :
            store = pd.HDFStore(self.input_paths[0])
            chunk = store.select('table1',
                                 start=0,
                                 stop=100)

            for col_name in self.encode_col:
                if (self.encode_len.get(col_name) == None):
                    if (chunk[col_name].dtype in ['int', 'float']):
                        self.encode_len[col_name] = 1
                        self.input_size = self.input_size + 1
                    else:
                        self.encode_len[col_name] = self.word_vector_size
                        self.input_size = self.input_size + self.word_vector_size
                    self.encode_onehot[col_name] = OneHotEncoder(self.word_vector_size)
                    self.encode_dtype[col_name] = str(chunk[col_name].dtype)
        except Exception as e :
            raise Exception ("error on wcnn feed parm prepare : {0}".format(e))

    def _init_nlp_node_parm(self, wf_conf):
        """
        init parms when data type is nlp
        :param wf_conf:
        :return:
        """
        self.encode_col = wf_conf.get_encode_column()
        self.encode_len = wf_conf.get_encode_len()
        self.embed_type = wf_conf.get_embed_type()
        self.word_vector_size = wf_conf.get_vocab_size() + 4
        self.input_size = int(self.encode_len) * int(self.word_vector_size)
        if (self.embed_type == 'onehot'):
            self.onehot_encoder = OneHotEncoder(self.word_vector_size)
            if (wf_conf.get_vocab_list()):
                self.onehot_encoder.restore(wf_conf.get_vocab_list())

    def _convert_data_format(self, file_path, index):
        """
        convert variois data to matrix fit to autoencoder
        :param obj:
        :param index:
        :return:
        """
        if(self.preprocess_type in ['frame']) :
            return self._frame_parser(file_path, index)
        elif(self.preprocess_type in ['mecab', 'kkma', 'twitter']) :
            return self._nlp_parser(file_path, index)

    def _frame_parser(self, file_path, index):
        """
        parse nlp data
        :return:
        """
        try :
            store = pd.HDFStore(file_path)
            chunk = store.select('table1',
                                 start=index.start,
                                 stop=index.stop)
            input_vector = []
            count = index.stop - index.start

            for col_name in self.encode_col:
                if (chunk[col_name].dtype == 'O'):
                    input_vector.append(list(map(lambda x: self.encode_onehot[col_name].get_vector(x),
                                             chunk[col_name][0:count].tolist())))
                else :
                    input_vector.append(np.array(list(map(lambda x: [self._filter_nan(x)], chunk[col_name][0:count].tolist()))))
            return self._flat_data(input_vector, len(chunk[col_name][0:count].tolist()))
        except Exception as e :
            raise Exception (e)
        finally:
            store.close()

    def _filter_nan(self, x):
        """
        map nan to 0
        :param x:
        :return:
        """
        import math
        if(math.isnan(x)) :
            return 0.0
        else :
            return x

    def _flat_data(self, input_vector, count):
        """

        :param input_vector:
        :return:
        """
        try :
            result = []
            for i in range(count) :
                row = []
                for col in input_vector :
                    row = row + col[i].tolist()
                result.append(row)
            return np.array(result, dtype='f')
        except Exception as e :
            raise Exception ("wcnn data prepare flat_data error : {0}".format(e))

    def _nlp_parser(self, file_path, index):
        """
        parse nlp data
        :return:
        """
        try :
            store = pd.HDFStore(file_path)
            chunk = store.select('table1',
                                 start=index.start,
                                 stop=index.stop)
            count = index.stop - index.start
            if (self.encode_col in chunk):
                encode = self.encode_pad(self._preprocess(chunk[self.encode_col].values)[0:count],
                                         max_len=self.encode_len)
                return self._word_embed_data(self.embed_type, encode)
            else:
                warnings.warn("not exists column names requested !!")
                return [['#'] * self.encode_len]
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

    def has_next(self):
        """
        check if hdf5 file pointer has next
        :return:
        """
        if(len(self.input_paths) > self.pointer) :
            return True
        else :
            if (self.preprocess_type in ['frame']):
                if (self.embed_type == 'onehot'):
                    save_dic = {}
                    for col_name in self.encode_col:
                        save_dic[col_name] = self.encode_onehot[col_name].dics()
                    self.wf_conf.set_vocab_list(save_dic)
                return False
            elif (self.preprocess_type in ['mecab', 'kkma', 'twitter']):
                if (self.embed_type == 'onehot'):
                    self.wf_conf.set_vocab_list(self.onehot_encoder.dics())
                return False


