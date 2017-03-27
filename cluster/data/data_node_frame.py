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
import h5py as h5
import json
from master.workflow.dataconf.workflow_dataconf_frame import WorkflowDataConfFrame as wf_data_conf
from common import utils

class DataNodeFrame(DataNode):
    """

    """

    def run(self, conf_data):
        """
        Run Data Node
        :param data_path:
        :return:dataframe
        """
        self.cls_list = conf_data['cls_pool']
        self._init_node_parm(conf_data['node_id'])

        if self.type == "csv":
            fp_list = utils.get_filepaths(self.data_src_path)
            try:
                for file_path in fp_list:
                    df_csv_read = self.load_csv_by_pandas(file_path)
                    self.make_column_types(df_csv_read, conf_data['node_id'])
                    self.create_hdf5(self.data_store_path, df_csv_read)
                    os.remove(file_path)
            except Exception as e:
                raise Exception(e)
        return None

    def create_hdf5(self, data_path, dataframe):
        """
        Create hdf5
        :param data_path:
        :return:dataframe
        """
        file_name = strftime("%Y-%m-%d-%H:%M:%S", gmtime())
        output_path = os.path.join(data_path, file_name)
        hdf = pd.HDFStore(output_path)
        hdf.put('table1', dataframe, format='table', data_columns=True, encoding='UTF-8')
        hdf.close()

    def load_data(self, node_id, parm = 'all'):
        """
        load train data
        :param node_id:
        :param parm:
        :return:
        """
        try:
            return utils.get_filepaths(self.data_store_path)
        except Exception as e:
            raise Exception(e)

    def load_csv_by_pandas(self, data_path):
        """
        read csv
        :param data_path:
        :return:data_path
        """
        df_csv_read = pd.read_csv(tf.gfile.Open(data_path),
                                  skipinitialspace=True,
                                  engine="python")
        return df_csv_read

    def make_column_types (self, df, node_id):
        """
        csv를 읽고 column type을 계산하여 data_conf에 저장(data_conf가 비어있을때 )
        :param df:
        :param conf_data:
        """
        try:
            dataconf_nodes = self._get_forward_node_with_type(node_id, 'dataconf')
            if(len(dataconf_nodes) > 0 ) :
                wf_data_conf_node = wf_data_conf(dataconf_nodes[0])
                if ('conf' not in wf_data_conf_node.__dict__):
                    self.set_default_dataconf_from_csv(wf_data_conf_node, df, node_id)
        except Exception as e:
            raise Exception(e)

    def set_default_dataconf_from_csv(self,wf_data_config, df, node_id):
        """
        csv를 읽고 column type을 계산하여 data_conf에 저장(data_conf가 비어있을때 )
        :param wf_data_config, df, nnid, ver, node:
        :param conf_data:
        """
        #TODO : set_default_dataconf_from_csv 파라미터 정리 필요
        data_conf = dict()
        data_conf_col_type = dict()
        #data_conf_label = dict()
        for i, v in df.dtypes.iteritems():
            # label
            column_dtypes = dict()
            col_type = ''
            if (str(v) == "int64"):  # maybe need float
                col_type = 'CONTINUOUS'
            else:
                col_type = 'CATEGORICAL'
            column_dtypes['column_type'] = col_type
            data_conf_col_type[i] = column_dtypes
        data_conf['cell_feature'] = data_conf_col_type
        data_conf_json_str = json.dumps(data_conf)
        data_conf_json = json.loads(data_conf_json_str)

        # DATACONF_FRAME_CALL
        wf_data_config.put_step_source(node_id, data_conf_json)

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
        try :
            wf_data_frame = WorkFlowDataFrame(key)
            self.type = wf_data_frame.object_type
            self.data_sql_stmt = wf_data_frame.sql_stmt
            self.data_src_path = wf_data_frame.source_path
            self.data_src_type = wf_data_frame.src_type
            self.data_server_type = wf_data_frame.src_server
            self.data_preprocess_type = wf_data_frame.step_preprocess
            self.data_store_path = wf_data_frame.step_store
        except Exception as e :
            raise Exception ("WorkFlowDataFrame parms are not set ")

