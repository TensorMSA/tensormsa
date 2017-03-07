from cluster.data.data_node import DataNode
from master.workflow.data.workflow_data_text import WorkFlowDataText
from konlpy.tag import Kkma
import konlpy, jpype
from konlpy.tag import Mecab
from common.utils import common_util
import h5py, os
from cluster.data.hdf5 import H5PYDataset
from time import gmtime, strftime

class DataNodeText(DataNode):
    """

    """

    def run(self, conf_data):
        """

        :param conf_data:
        :return:
        """
        try:
            self._init_node_parm(conf_data)

            file_name = strftime("%Y-%m-%d-%H:%M:%S", gmtime())
            output_path = os.path.join(self.data_store_path, file_name)
            os.makedirs(self.data_store_path, exist_ok=True)
            h5file = h5py.File(output_path, mode = 'w')

            mecab = Mecab('/usr/local/lib/mecab/dic/mecab-ko-dic')
            fp_list = common_util.get_filepaths(self.data_src_path)
            for file_path in fp_list :
                with open(file_path, 'r') as myfile:
                    data = myfile.read()
                    pos = mecab.pos(data)
                    dt = h5py.special_dtype(vlen=str)
                    hdf_rawdata = h5file.create_dataset("rawdata", (len(pos),2), dtype=dt)
                    hdf_rawdata[...] = pos

            temp = h5py.File(output_path, mode='r')
            print(temp['/rawdata'])

            # kkma = Kkma()
            # pos = kkma.pos(u'원칙이나 기체 설계와 엔진·레이더·항법장비 등')
            # print(pos)

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