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

class DataNodeFrame(DataNode):
    """

    """

    def run(self, conf_data):
        """
        Run Data Node
        :param data_path:
        :return:dataframe
        """

        self._init_node_parm(conf_data['node_id'])
        node_id = conf_data['node_id']
        source_directory = self.data_src_path
        data_source_type = self.data_src_type
        data_store_path = self.data_store_path
        object_type = self.type
        data_server_type = self.data_server_type
        data_preprocess_type = self.data_preprocess_type
        data_sql_stmt = self.data_sql_stmt

        if object_type == "csv":
            #source_filepath_name = source_directory + "/" + "adult.data"
            try:
                df_csv_read = self.load_csv_by_pandas(source_directory)
                self.make_column_types(df_csv_read, conf_data)
            except Exception as e:
                raise Exception(e)
            try:
                self.create_hdf5(data_store_path, df_csv_read)
            except Exception as e:
                raise Exception(e)

            # try:
            #     # filename = data_store_path + "/" + "adult.h5"
            #     #
            #     # #type4 partial read
            #     # store = pd.HDFStore(filename)
            #     # nrows = store.get_storer('table1').nrows
            #     # chunksize = 100
            #     #
            #     # for i in range(nrows // chunksize + 1):
            #     #     chunk = store.select('table1',
            #     #                          start=i * chunksize,
            #     #                          stop=(i + 1) * chunksize)
            #     # store.close()
            # except Exception as e:
            #     raise Exception(e)
        return None

    def create_hdf5(self, data_path, dataframe):
        """
        Create hdf5
        :param data_path:
        :return:dataframe
        """
        store_filepath_name = data_path + "/" + "adult.h5"
        # 파일이 있으면 지우기
        try:
            os.remove(store_filepath_name)
        except OSError:
            pass

        hdf = pd.HDFStore(store_filepath_name)
        hdf.put('table1', dataframe, format='table', data_columns=True, encoding='UTF-8')
        hdf.close()

    def load_hdf5(data_path, dataframe):
        """
        Load_hdf5
        :param data_path:
        :return:data_path
        """
        store_filepath_name = data_path + "/" + "adult.h5"
        hdf = pd.HDFStore(store_filepath_name)
        hdf.put('table1', dataframe, format='table', data_columns=True)
        hdf.close()

    def load_csv_by_pandas(self, data_path):
        """
        read csv
        :param data_path:
        :return:data_path
        """
        source_filepath_name = data_path + "/" + "adult.data"
        df_csv_read = pd.read_csv(tf.gfile.Open(source_filepath_name),
                                  skipinitialspace=True,
                                  engine="python")
        return df_csv_read

    def make_column_types (self, df, conf_data):
        """
        csv를 읽고 column type을 계산하여 data_conf에 저장(data_conf가 비어있을때 )
        :param df:
        :param conf_data:
        """
        try:
            node_id = conf_data['node_id'].split("_")
            nnid = node_id[0]
            ver = node_id[1]
            node = "dataconf_node"  # node_id[2] + "_" + node_id[3]
            nn_wf_node_id = nnid+"_"+ver+"_"+node
            wf_data_config = wf_data_conf(nn_wf_node_id)

            try:
                check = wf_data_config.data_conf
            except KeyError:
                #TODO : set_default_dataconf_from_csv parameter shoud modify It is many
                self.set_default_dataconf_from_csv(wf_data_config, df, nnid, ver, node)
        except Exception as e:
            raise Exception(e)

    def set_default_dataconf_from_csv(self,wf_data_config, df, nnid, ver, node):
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
        print(data_conf_json)
        # DATACONF_FRAME_CALL
        wf_data_config.put_step_source(nnid, ver, node, data_conf_json)

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
        wf_data_frame = WorkFlowDataFrame(key)
        self.type = wf_data_frame.object_type
        self.data_sql_stmt = wf_data_frame.sql_stmt
        self.data_src_path = wf_data_frame.source_path
        self.data_src_type = wf_data_frame.src_type
        self.data_server_type = wf_data_frame.src_server
        self.data_preprocess_type = wf_data_frame.step_preprocess
        self.data_store_path = wf_data_frame.step_store

