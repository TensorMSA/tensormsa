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
import csv

class DataNodeFrame(DataNode):
    """

    """


    def run(self, conf_data):
        """
        Run Data Node
        한번에 HDF5랑  TFRECORD를 만든다.
        :param data_path:
        :return:dataframe
        """
        self.cls_list = conf_data['cls_pool']
        self._init_node_parm(conf_data['node_id'])

        if(self.data_src_type == 'local' and self.type == "csv") :
            #self.src_local_handler(conf_data)
            self.src_local_handler(conf_data, tfrecode_flag=True)
        if (self.data_src_type == 'rdb'):
            raise Exception ("on development now")
        if (self.data_src_type == 's3'):
            raise Exception("on development now")
        if (self.data_src_type == 'hbase'):
            raise Exception("on development now")



    def src_local_handler(self, conf_data, tfrecode_flag = False):
        """
        :param conf_data:
        :return:
        """
        try:

            fp_list = utils.get_filepaths(self.data_src_path)

            _multi_node_flag = self.multi_node_flag

            try:
                for file_path in fp_list:
                    df_csv_read = self.load_csv_by_pandas(file_path)
                    self.data_conf = self.make_column_types(df_csv_read, conf_data['node_id'])
                    self.create_hdf5(self.data_store_path, df_csv_read)
                    #os.remove(file_path)

                #make tfrecord for multi Threading
                    if _multi_node_flag == True:
                        skip_header = False
                        #Todo Have to remove if production
                        #self.save_tfrecord(file_path, self.data_store_path, skip_header, df_csv_read)
            except Exception as e:
                raise Exception(e)
            return None
        except Exception as e:
            raise Exception(e)

    def multi_load_data(self, node_id, parm = 'all'):
        pass




    def preprocess_data(self, input_data):
        """

        :param input_data:
        :return:
        """
        if(self.data_preprocess_type == 'mecab'):
            for key in input_data.keys() :
                input_data[key] = self._mecab_parse(input_data[key])
            return input_data

    def save_tfrecord(self, csv_data_file, store_path, skip_header, df_csv_read):
        #_, ext = os.path.basename(csv_data_file)
        #filename = os.path.basename(csv_data_file)
        filename = strftime("%Y-%m-%d-%H:%M:%S", gmtime())
        output_file = store_path +"/"+ filename + ".tfrecords"
        self.create_tfrecords_file( output_file, skip_header, df_csv_read)

    def create_tfrecords_file(self, output_file, skip_header, df_csv_read):
        """
        Creates a TFRecords file for the given input data and
        example transofmration function
        """
        writer = tf.python_io.TFRecordWriter(output_file)
        print("Creating TFRecords file at", output_file, "...")

        CONTINUOUS_COLUMNS, CATEGORICAL_COLUMNS  = self.make_continuous_category_list(self.data_conf["cell_feature"])

        csv_dataframe = df_csv_read
        for _, row in csv_dataframe.iterrows():
            x = self.create_example_pandas(row, CONTINUOUS_COLUMNS, CATEGORICAL_COLUMNS )
            writer.write(x.SerializeToString())
        writer.close()
        print("Wrote to", output_file)

    def make_continuous_category_list(self,cell_feature ):
        """
        Example 을 위한  Continuous 랑 Categorical을 구분하기 위한 list

        """
        CONTINUOUS_COLUMNS = list()
        CATEGORICAL_COLUMNS = list()
        for type_columne, type_value in cell_feature.items():
            if type_value["column_type"] == 'CONTINUOUS':
                CONTINUOUS_COLUMNS.append(type_columne)
            else:
                CATEGORICAL_COLUMNS.append(type_columne)
        return CONTINUOUS_COLUMNS, CATEGORICAL_COLUMNS

    def create_example_pandas(self, row, CONTINUOUS_COLUMNS, CATEGORICAL_COLUMNS):
        """
        Make TFRecord Extend row (Example)
        TFRecord를 만들기 위한 Example을 만든다.

        """
        try:
            example = tf.train.Example()
            _CONTINUOUS_COLUMNS = CONTINUOUS_COLUMNS[:]
            _CATEGORICAL_COLUMNS = CATEGORICAL_COLUMNS[:]
            _CONTINUOUS_COLUMNS.remove("fnlwgt")
            _CATEGORICAL_COLUMNS.remove("income_bracket")

            for col, value in row.items():
                #print(col)
                #print(value)
                if col in _CATEGORICAL_COLUMNS:
                    example.features.feature[col].bytes_list.value.extend([str.encode(value)])
                elif col in _CONTINUOUS_COLUMNS:
                    example.features.feature[col].int64_list.value.extend([int(value)])
                #'income_bracket'
                #'fnlwgt'
                if col == "income_bracket":
                    example.features.feature['label'].int64_list.value.extend([int(">50K" in value)])

            return example
        except Exception as e:
            raise Exception(e)


    def create_hdf5(self, data_path, dataframe):
        """
        Create hdf5
        :param data_path:
        :return:dataframe
        """
        file_name = strftime("%Y-%m-%d-%H:%M:%S", gmtime()) + ".h5"
        output_path = os.path.join(data_path, file_name)
        hdf = pd.HDFStore(output_path)
        hdf.put('table1', dataframe, format='table', data_columns=True, encoding='UTF-8')
        hdf.close()

    def load_data(self, node_id = "", parm = 'all'):
        """
        load train data
        :param node_id:
        :param parm:
        :return:
        """
        try:
            _multi_node_flag = self.multi_node_flag
            if _multi_node_flag == True:
                file_path = utils.get_filepaths(self.data_store_path,'h5')
            else:
                file_path = utils.get_filepaths(self.data_store_path,'tfrecords')
            return file_path
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
            data_conf=self.set_dataconf_for_checktype(df, node_id )
            #self.data_conf = self.set_dataconf_for_checktype(df, node_id )
            dataconf_nodes = self._get_forward_node_with_type(node_id, 'dataconf')
            if(len(dataconf_nodes) > 0 ) :
                wf_data_conf_node = wf_data_conf(dataconf_nodes[0])
                if ('conf' not in wf_data_conf_node.__dict__):
                    self.set_default_dataconf_from_csv(wf_data_conf_node, node_id, self.data_conf)
            return data_conf
        except Exception as e:
            raise Exception(e)

    def set_default_dataconf_from_csv(self,wf_data_config, node_id, data_conf):
        """
        csv를 읽고 column type을 계산하여 data_conf에 저장(data_conf가 비어있을때 )
        :param wf_data_config, df, nnid, ver, node:
        :param conf_data:
        tfrecord 때문에 항상 타입을 체크하고 필요할때만 저장
        """
        # #TODO : set_default_dataconf_from_csv 파라미터 정리 필요
        # data_conf = dict()
        # data_conf_col_type = dict()
        # #data_conf_label = dict()
        # for i, v in df.dtypes.iteritems():
        #     # label
        #     column_dtypes = dict()
        #     col_type = ''
        #     if (str(v) == "int64"):  # maybe need float
        #         col_type = 'CONTINUOUS'
        #     else:
        #         col_type = 'CATEGORICAL'
        #     column_dtypes['column_type'] = col_type
        #     data_conf_col_type[i] = column_dtypes
        # data_conf['cell_feature'] = data_conf_col_type
        # data_conf_json_str = json.dumps(data_conf)
        # data_conf_json = json.loads(data_conf_json_str)

        # DATACONF_FRAME_CALL
        wf_data_config.put_step_source(node_id, data_conf)

    def set_dataconf_for_checktype(self, df, node_id):
        """
        csv를 읽고 column type을 계산하여 data_conf에 저장(data_conf가 비어있을때 )
        :param wf_data_config, df, nnid, ver, node:
        :param conf_data:
        """
        #TODO : set_default_dataconf_from_csv 파라미터 정리 필요
        data_conf = dict()
        data_conf_col_type = dict()
        #data_conf_label = dict()
        numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
        for i, v in df.dtypes.iteritems():
            # label
            column_dtypes = dict()
            col_type = ''
            if (str(v) in numerics):  # maybe need float
                col_type = 'CONTINUOUS'
            else:
                col_type = 'CATEGORICAL'
            column_dtypes['column_type'] = col_type
            data_conf_col_type[i] = column_dtypes
        data_conf['cell_feature'] = data_conf_col_type
        data_conf_json_str = json.dumps(data_conf)
        data_conf_json = json.loads(data_conf_json_str)

        # DATACONF_FRAME_CALL
        #wf_data_config.put_step_source(node_id, data_conf_json)
        return data_conf_json

    def _set_progress_state(self):
        return None

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
            self.sent_max_len = wf_data_frame.max_sentence_len
            self.multi_node_flag = wf_data_frame.multi_node_flag
        except Exception as e :
            raise Exception ("WorkFlowDataFrame parms are not set " + str(e))

