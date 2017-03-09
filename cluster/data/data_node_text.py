from cluster.data.data_node import DataNode
from master.workflow.data.workflow_data_text import WorkFlowDataText
from konlpy.tag import Kkma
from konlpy.tag import Mecab
from common import utils
import os
from time import gmtime, strftime
from shutil import copyfile

class DataNodeText(DataNode):
    """

    """

    def run(self, conf_data):
        """

        :param conf_data:
        :return:
        """
        try:
            self._init_node_parm(conf_data['node_id'])
            os.makedirs(self.data_store_path, exist_ok=True)
            fp_list = utils.get_filepaths(self.data_src_path)
            for file_path in fp_list:
                file_name = strftime("%Y-%m-%d-%H:%M:%S", gmtime())
                output_path = os.path.join(self.data_store_path, file_name)
                copyfile(file_path, output_path)
                os.remove(file_path)
        except Exception as e:
            print("exception : {0}".format(e))
            raise Exception(e)


    def _init_node_parm(self, key):
        """

        :return:
        """
        wf_conf = WorkFlowDataText(key)
        self.data_sql_stmt = wf_conf.get_sql_stmt()
        self.data_src_path = wf_conf.get_source_path()
        self.data_src_type = wf_conf.get_src_type()
        self.data_server_type = wf_conf.get_src_server()
        self.data_parse_type = wf_conf.get_parse_type()
        self.data_preprocess_type = wf_conf.get_step_preprocess()
        self.data_store_path = wf_conf.get_step_store()

    def _set_progress_state(self):
        return None


    def load_train_data(self, node_id, parm = 'all'):
        """
        load train data
        :param node_id:
        :param parm:
        :return:
        """
        try :
            self._init_node_parm(node_id)
            if (self.data_preprocess_type == 'mecab'):
                return self._mecab_parse()
            elif(self.data_preprocess_type == 'kkma'):
                return self._kkma_parse()
        except Exception as e :
            raise Exception (e)

    def load_test_data(self, node_id, parm = 'all'):
        """
        load test data
        :param node_id:
        :param parm:
        :return:
        """
        return []

    def _mecab_parse(self):
        """

        :param h5file:
        :return:
        """
        mecab = Mecab('/usr/local/lib/mecab/dic/mecab-ko-dic')
        fp_list = utils.get_filepaths(self.data_store_path)
        return_arr = []
        for file_path in fp_list:
            with open(file_path, 'r') as myfile:
                data = myfile.read()
                return_arr = return_arr + self._flat(mecab.pos(data))
        return return_arr

    def _kkma_parse(self):
        """

        :param h5file:
        :return:
        """
        kkma = Kkma()
        return_arr = []
        fp_list = utils.get_filepaths(self.data_store_path)
        for file_path in fp_list:
            with open(file_path, 'r') as myfile:
                data = myfile.read()
                return_arr = return_arr + self._flat(kkma.pos(data))
        return return_arr

    def _twitter_parse(self, h5file):
        """

        :param h5file:
        :return:
        """
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
            if(tag == 'SF') :
                line_list.append('\n')
                doc_list.append(line_list)
                line_list = []
        return doc_list