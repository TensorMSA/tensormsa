from cluster.data.data_node import DataNode
import os
import zipfile
import h5py
import numpy
from master.workflow.data.workflow_data_frame import WorkFlowDataFrame
from time import gmtime, strftime
from cluster.common.common_node import WorkFlowCommonNode
import pandas as pd
import tensorflow as tf

class DataNodeFrame(DataNode):
    """

    """

    def run(self, conf_data):
        self._init_node_parm(conf_data['node_id'])
        TRAIN = 'cat_vs_dog.zip'
        node_id = conf_data['node_id']
        #config_data = WorkFlowDataFrame().get_step_source(node_id)
        source_directory = self.data_src_path
        data_source_type = self.data_src_type
        data_store_path = self.data_store_path
        object_type = self.type
        data_server_type = self.data_server_type
        data_preprocess_type = self.data_preprocess_type
        data_sql_stmt = self.data_sql_stmt

        if object_type == "csv":
            filepath_name = source_directory + "/" + "adult.data"
            try:
                df_csv_read = pd.read_csv(tf.gfile.Open(filepath_name),
                     skipinitialspace=True,
                     engine="python")
            except Exception as e:
                raise Exception(e)
            print(df_csv_read)





        return None
        #return None

    def _init_node_parm(self, node_id):
        return None

    def _set_progress_state(self):
        return None

    def load_train_data(self, node_id, parm = 'all'):
        return []

    def load_test_data(self, node_id, parm = 'all'):
        return []

    def _init_node_parm(self, key):
        """
        Init parameter from workflow_data_frame
        :return:
        """
        wf_df_conf = WorkFlowDataFrame(key)
        self.type = wf_df_conf.object_type
        self.data_sql_stmt = wf_df_conf.sql_stmt
        self.data_src_path = wf_df_conf.source_path
        self.data_src_type = wf_df_conf.src_type
        self.data_server_type = wf_df_conf.src_server
        self.data_preprocess_type = wf_df_conf.step_preprocess
        self.data_store_path = wf_df_conf.step_store

