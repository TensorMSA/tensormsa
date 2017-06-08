from cluster.data.data_node import DataNode
from master.workflow.data.workflow_data_text import WorkFlowDataText
from common import utils
import os,h5py
from time import gmtime, strftime
from shutil import copyfile
import numpy as np

class DataNodeRaw(DataNode):


    def run(self, conf_data):
        """

        :param conf_data:
        :return:
        """
        self._init_node_parm(conf_data['node_id'])
        if(self.data_src_type == 'local') :
            self.src_local_handler(conf_data)
        if (self.data_src_type == 'rdb'):
            raise Exception ("on development now")
        if (self.data_src_type == 's3'):
            raise Exception("on development now")
        if (self.data_src_type == 'hbase'):
            raise Exception("on development now")

    def src_local_handler(self, conf_data):
        """

        :param conf_data:
        :return:
        """
        try:
            fp_list = utils.get_filepaths(self.data_src_path)
            for file_path in fp_list :
                str_buf = self._load_local_files(file_path)
                self._save_raw_file(str_buf)
        except Exception as e:
            raise Exception(e)

    def _save_raw_file(self,buffer_list):
        file_name = strftime("%Y-%m-%d-%H:%M:%S", gmtime())
        output_path = os.path.join(self.data_store_path, file_name)
        with open(output_path, 'w+') as f:
            for line in buffer_list:
                f.write("%s " % line)
            f.flush()
            f.close()

    def _load_local_files(self, file_path):
        """
        load local source file
        :return:
        """
        with open(file_path, 'r') as myfile:
            os.remove(file_path)
            return myfile.readlines()

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

    def load_data(self, node_id = "", parm = 'all'):
        """
        load train data
        :param node_id:
        :param parm:
        :return:
        """
        return utils.get_filepaths(self.data_store_path)


