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
        self._init_node_parm(conf_data['node_id'])
        #TRAIN = 'cat_vs_dog.zip'
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
            source_filepath_name = source_directory + "/" + "adult.data"
            try:
                df_csv_read = self.load_csv_by_pandas(source_directory)
                self.make_column_types(df_csv_read, conf_data)
                #df_csv_read = pd.read_csv(tf.gfile.Open(source_filepath_name),
                #     skipinitialspace=True,
                #     engine="python")
                #filtered_df = df_csv_read[(df_csv_read.fnlwgt==121772)]
                #print(filtered_df)

                #dtype
                #for i,v in df_csv_read.dtypes.iteritems():
                #    print(i,v)


            except Exception as e:
                raise Exception(e)
            #test convert to hdf5
            try:
                #store_filepath_name = data_store_path + "/" + "adult.h5"
                #df_csv_read.to_hdf(store_filepath_name, 'df', format='fixed', mode='w')
                #hdf = pd.HDFStore(store_filepath_name)
                #hdf.put('d1', df_csv_read, format='table', data_columns=True)
                #hdf.close()
                self.create_hdf5(data_store_path, df_csv_read)
            except Exception as e:
                raise Exception(e)

            try:
                filename = data_store_path + "/" + "adult.h5"
                #type4 partial read
                store = pd.HDFStore(filename)
                nrows = store.get_storer('table1').nrows
                chunksize = 100

                for i in range(nrows // chunksize + 1):
                    chunk = store.select('table1',
                                         start=i * chunksize,
                                         stop=(i + 1) * chunksize)
                    #print(chunk)
                    # work on the chunk
                store.close()

                #type 3 read_hdf
           #     hdf_load = pd.read_hdf(filename, 'table1')
             #   print(type(hdf_load))

                #type2 read pandas

                #hdf_load = pd.HDFStore(filename, mode='r')

            #    print(type(hdf_load))

                #type 1 h5py
                #f = h5py.File(filename, 'r')
                #data = f['table1'][...]
                #print(type(data))

            except Exception as e:
                raise Exception(e)





            #print(df_csv_read)

        return None
        #return None

    def create_hdf5(self, data_path, dataframe):
        store_filepath_name = data_path + "/" + "adult.h5"
        # df_csv_read.to_hdf(store_filepath_name, 'df', format='fixed', mode='w')
        hdf = pd.HDFStore(store_filepath_name)
        hdf.put('table1', dataframe, format='table', data_columns=True, encoding='UTF-8')
        hdf.close()

    def load_hdf5(data_path, dataframe):
        store_filepath_name = data_path + "/" + "adult.h5"
        # df_csv_read.to_hdf(store_filepath_name, 'df', format='fixed', mode='w')
        hdf = pd.HDFStore(store_filepath_name)
        hdf.put('table1', dataframe, format='table', data_columns=True)
        hdf.close()

    def load_csv_by_pandas(self, data_path):
        source_filepath_name = data_path + "/" + "adult.data"
        df_csv_read = pd.read_csv(tf.gfile.Open(source_filepath_name),
                                  skipinitialspace=True,
                                  engine="python")
        return df_csv_read
        # filtered_df = df_csv_read[(df_csv_read.fnlwgt==121772)]
        # print(filtered_df)
    def make_column_types (self, df, conf_data):
        try:
            data_conf = dict()
            data_conf_col_type = dict()
            data_conf_label = dict()
            for i, v in df.dtypes.iteritems():
                #label
                column_dtypes = dict()
                col_type = ''
                if (str(v) == "int64"): #maybe need float
                    col_type =  'CONTINUOUS'
                else:
                    col_type = 'CATEGORICAL'
                column_dtypes['column_type'] = col_type
                data_conf_col_type[i] = column_dtypes
               # print(data_conf_col_type)
            data_conf['cell_feature'] = data_conf_col_type
            #data_conf_label["label"] ="LABEL"
            #data_conf["label"] = data_conf_label

            data_conf_json_str = json.dumps(data_conf)
            data_conf_json = json.loads(data_conf_json_str)
            print(data_conf_json)
            #'nn00004_2_data_node'
            node_id = conf_data['node_id'].split("_")
            nnid = node_id[0]
            ver = node_id[1]
            node = "dataconf_node"#node_id[2] + "_" + node_id[3]
            #DATACONF_FRAME_CALL
            wf_data_conf().put_step_source(nnid, ver, node, data_conf_json)

        except Exception as e:
            raise Exception(e)



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

