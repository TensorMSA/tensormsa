from cluster.data.data_node import DataNode
from master.workflow.data.workflow_data_text import WorkFlowDataText
from konlpy.tag import Kkma
import konlpy, jpype
from konlpy.tag import Mecab
from common import utils
import h5py, os
from cluster.data.hdf5 import H5PYDataset
from time import gmtime, strftime

class DataNodeText(DataNode):
    """
            # kkma = Kkma()
            # pos = kkma.pos(u'원칙이나 기체 설계와 엔진·레이더·항법장비 등')
            # print(pos)
    """

    def run(self, conf_data):
        """

        :param conf_data:
        :return:
        """
        try:
            self._init_node_parm(conf_data['node_id'])

            file_name = strftime("%Y-%m-%d-%H:%M:%S", gmtime())
            output_path = os.path.join(self.data_store_path, file_name)
            os.makedirs(self.data_store_path, exist_ok=True)
            h5file = h5py.File(output_path, mode = 'w')

            mecab = Mecab('/usr/local/lib/mecab/dic/mecab-ko-dic')
            fp_list = utils.get_filepaths(self.data_src_path)
            for file_path in fp_list :
                with open(file_path, 'r') as myfile:
                    data = myfile.read()
                    pos = mecab.pos(data)
                    dt = h5py.special_dtype(vlen=str)
                    hdf_rawdata = h5file.create_dataset("rawdata", (len(pos),2), dtype=dt)
                    hdf_rawdata[...] = pos
            return pos
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
        self.data_preprocess_info = wf_conf.get_step_preprocess()
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
        self._init_node_parm(node_id)
        return_data_arr = []
        fp_list = utils.get_filepaths(self.data_store_path)
        for file_path in fp_list:
            with h5py.File(file_path, mode='r') as myfile:
                return_data_arr.append(myfile['/rawdata'][...])
        return return_data_arr

    def load_test_data(self, node_id, parm = 'all'):
        """
        load test data
        :param node_id:
        :param parm:
        :return:
        """
        return []