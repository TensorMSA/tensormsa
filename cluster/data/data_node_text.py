from cluster.data.data_node import DataNode
from master.workflow.data.workflow_data_text import WorkFlowDataText
from konlpy.tag import Kkma
from konlpy.tag import Mecab
from konlpy.tag import Twitter
from common import utils
import os,h5py
from time import gmtime, strftime
from shutil import copyfile
import numpy as np

class DataNodeText(DataNode):

    def get_tag_package(self, type):
        buffer_list = []
        if (type == 'mecab'):
            buffer_list = self._mecab_parse()
        elif (type == 'kkma'):
            buffer_list = self._kkma_parse()
        elif (type == 'twitter'):
            buffer_list = self._twitter_parse()
        return buffer_list

    def run(self, conf_data):
        """

        :param conf_data:
        :return:
        """
        try:
            self._init_node_parm(conf_data['node_id'])
            buffer_list = self.get_tag_package(self.data_preprocess_type)

            if(len(buffer_list) > 0 ) :
                file_name = strftime("%Y-%m-%d-%H:%M:%S", gmtime())
                output_path = os.path.join(self.data_store_path, file_name)
                h5file = h5py.File(output_path, 'w', chunk=True)
                dt_vlen = h5py.special_dtype(vlen=str)
                dt_arr = np.dtype((dt_vlen, (self.sent_max_len, )))
                h5raw = h5file.create_dataset('rawdata', (len(buffer_list),), dtype=dt_arr)
                for i in range(len(buffer_list)):
                    h5raw[i] = np.array(buffer_list[i], dtype=object)
                h5file.flush()
                h5file.close()

        except Exception as e:
            print("exception : {0}".format(e))
            raise Exception(e)

    def _init_node_parm(self, key):
        """
        init parms by using master classes (handling params)
        :return:
        """
        wf_conf = WorkFlowDataText(key)
        self.data_sql_stmt = wf_conf.get_sql_stmt()
        self.data_src_path = wf_conf.get_source_path()
        self.data_src_type = wf_conf.get_src_type()
        self.data_store_path = wf_conf.get_step_store()
        self.data_server_type = wf_conf.get_src_server()
        self.data_parse_type = wf_conf.get_parse_type()
        self.sent_max_len = wf_conf.get_max_sent_len()
        self.data_preprocess_type = wf_conf.get_step_preprocess()

    def _set_progress_state(self):
        return None

    def load_data(self, node_id, parm = 'all'):
        """
        load train data
        :param node_id:
        :param parm:
        :return:
        """
        self._init_node_parm(node_id)
        fp_list = utils.get_filepaths(self.data_store_path)
        return_arr = []
        try :
            for file_path in fp_list:
                self._init_node_parm(node_id)
                h5file = h5py.File(file_path, mode='r')
                return_arr.append(h5file)
            return return_arr
        except Exception as e :
            raise Exception (e)

    def _mecab_parse(self):
        """

        :param h5file:
        :return:
        """
        mecab = Mecab('/usr/local/lib/mecab/dic/mecab-ko-dic')
        fp_list = utils.get_filepaths(self.data_src_path)
        return_arr = []
        for file_path in fp_list:
            with open(file_path, 'r') as myfile:
                data = myfile.read()
                return_arr = return_arr + self._flat(mecab.pos(data))
                os.remove(file_path)
        return return_arr

    def _kkma_parse(self):
        """

        :param h5file:
        :return:
        """
        kkma = Kkma()
        return_arr = []
        fp_list = utils.get_filepaths(self.data_src_path)
        for file_path in fp_list:
            with open(file_path, 'r') as myfile:
                data = myfile.read()
                return_arr = return_arr + self._flat(kkma.pos(data))
                os.remove(file_path)
        return return_arr

    def _twitter_parse(self):
        """

        :param h5file:
        :return:
        """
        twitter = Twitter(jvmpath=None)
        return_arr = []
        fp_list = utils.get_filepaths(self.data_src_path)
        for file_path in fp_list:
            with open(file_path, 'r') as myfile:
                data = myfile.read()
                return_arr = return_arr + self._flat(twitter.pos(data))
                os.remove(file_path)
        return return_arr

    def _default_parse(self):
        pass

    def _flat(self, pos):
        """
        flat corpus for gensim
        :param pos:
        :return:
        """
        doc_list = []
        line_list = []
        for word, tag in pos :
            line_list.append("{0}/{1}".format(word, tag))
            #Add POS Tagging for divide (kkma and twitter)
            if(tag == 'SF' or tag == 'Punctuation') :
                if(len(line_list) > self.sent_max_len - 1) :
                    line_list = line_list[0:self.sent_max_len-1]
                else :
                    pad_len = (self.sent_max_len - (len(line_list)+1))
                    line_list = line_list + ['#'] * pad_len
                line_list.append('\n')
                doc_list.append(line_list)
                line_list = []
        return doc_list