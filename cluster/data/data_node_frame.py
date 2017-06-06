from blaze.interactive import data

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
from sklearn.preprocessing import LabelEncoder
import logging
from common.utils import *
import shutil
from master.workflow.data.workflow_data_frame import WorkFlowDataFrame as wf_data_frame

class DataNodeFrame(DataNode):
    """
        DataNode Configuration
        NULL처리가 중요한데 Category "" Continuous 0.0
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
            self.src_local_handler(conf_data)
        if (self.data_src_type == 'rdb'):
            raise Exception ("on development now")
        if (self.data_src_type == 's3'):
            raise Exception("on development now")
        if (self.data_src_type == 'hbase'):
            raise Exception("on development now")

    def get_eval_node_file_list(self, conf_data):
        #evalnode 찾고
        #만들고, 경로 가져옴

        eval_data_node = [_i  for _i, _k in conf_data.get('cls_pool').items() if 'evaldata' in _i]
        data_conf_node_id = [_i for _i, _k in conf_data.get('cls_pool').items() if 'dataconf' in _i]
        eval_data_cls = wf_data_frame(eval_data_node[0])
        eval_source_path = eval_data_cls.source_path
        fp_list = utils.get_filepaths(eval_source_path, file_type='csv')
        for file_path in fp_list:
            df_csv_read = self.load_csv_by_pandas(file_path)
            self.data_conf = self.make_column_types(df_csv_read, eval_data_node[0],
                                                    data_conf_node_id[0])  # make columns type of csv


        #eval_data_cls.src_local_handler


    def src_local_handler(self, conf_data):
        """
        Make h5 & tfrecord for multi treading

        Arguments:
            conf_data : data_source_path. etc
        """
        try:

            fp_list = utils.get_filepaths(self.data_src_path, file_type='csv')
            _multi_node_flag = self.multi_node_flag

            eval_data = dict((_i, _k) for _i, _k in self.cls_list.items() if 'evaldata' in _i)

            try:
                #data conf node id 찾기
                data_conf_node_id = ''
                for _i, _k in self.cls_list.items():
                    if 'dataconf' in _i:
                        data_conf_node_id = _i
                        #eval 카테고리 데이터를 가져 오기 위해서 필요 Evalnode가 실행할때는 필요 없음
                        if 'data_node' not in conf_data['node_id']:
                            self.get_eval_node_file_list(conf_data)

                data_dfconf_list = data_conf_node_id

                for file_path in fp_list:
                    df_csv_read = self.load_csv_by_pandas(file_path)

                    if 'dataconf' in data_dfconf_list:
                        self.data_conf = self.make_column_types(df_csv_read, conf_data['node_id'], data_conf_node_id) # make columns type of csv
                        #eval 것도 같이 가져와서 unique value를 구해야함

                    #self.make_unique_value_each_column(df_csv_read,conf_data['node_id'])
                    self.create_hdf5(self.data_store_path, df_csv_read)
                    #Todo 뽑아서 함수화 시킬것
                    #for wdnn
                    #Wdnn인경우 data_dfconf가 무조껀 한개만 존재 하므로 아래와 같은 로직이 가능
                    if len(data_dfconf_list) > 0:
                        #Todo 정리가능

                        _key =data_dfconf_list
                        _nnid = _key.split('_')[0]
                        _ver = _key.split('_')[1]
                        _node  = 'dataconf_node'
                        _wf_data_conf = wf_data_conf(_key)
                        if hasattr(_wf_data_conf,'label') == True:
                            # label check
                            _label = _wf_data_conf.label
                            _labe_type = _wf_data_conf.label_type
                            origin_labels_list = _wf_data_conf.label_values if hasattr(_wf_data_conf,'label_values') else list() #처음 입려할때 라벨벨류가 없으면 빈 리스트 넘김
                            compare_labels_list = self.set_dataconf_for_labels(df_csv_read,_label)
                            self.combined_label_list = utils.get_combine_label_list(origin_labels_list,compare_labels_list )
                            #리스트를 합친다음 DB에 업데이트 한다.
                            _data_conf = dict()
                            _data_conf['label_values'] = self.combined_label_list
                            if _labe_type == 'CONTINUOUS':
                                _data_conf['label_values'] = list()
                            _wf_data_conf.put_step_source(_nnid, _ver,_node, _data_conf )

                            # make tfrecord for multi Threading
                            if _multi_node_flag == True:
                                skip_header = False
                                # Todo Have to remove if production
                                self.save_tfrecord(file_path, self.data_store_path, skip_header, df_csv_read,_label, _labe_type)

                    dir = self.data_src_path+"/backup"
                    if not os.path.exists(dir):
                        os.makedirs(dir)
                        #os.mkdir(self.data_src_path+"/backup")

                    file_name_bk = strftime("%Y-%m-%d-%H:%M:%S", gmtime()) + ".csvbk"
                    shutil.copy(file_path,self.data_src_path+"/backup/"+file_name_bk )
                    os.remove(file_path) #승우씨것
            except Exception as e:
                logging.error("Datanode making h5 or tfrecord error".format(e))
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

    def save_tfrecord(self, csv_data_file, store_path, skip_header, df_csv_read, label, label_type):
        """
        Creates a TFRecords file for the given input data and
        example transofmration function
        """

        filename = strftime("%Y-%m-%d-%H:%M:%S", gmtime())
        output_file = store_path +"/"+ filename + ".tfrecords"
        self.create_tfrecords_file( output_file, skip_header, df_csv_read, label,label_type)

    def create_tfrecords_file(self, output_file, skip_header, df_csv_read, label,label_type):
        """
        Creates a TFRecords file for the given input data and
        example transofmration function
        """
        try:
            writer = tf.python_io.TFRecordWriter(output_file)
            logging.info("Creating TFRecords file at", output_file, "...")

            CONTINUOUS_COLUMNS, CATEGORICAL_COLUMNS  = self.make_continuous_category_list(self.data_conf["cell_feature"])
            print_row_count = 10000
            csv_dataframe = df_csv_read
            for count, row in csv_dataframe.iterrows():
                x = self.create_example_pandas(row, CONTINUOUS_COLUMNS, CATEGORICAL_COLUMNS, label,label_type)
                if (count % print_row_count == 0):
                    logging.info("###### TFRecording row count : {0}".format(count))
                writer.write(x.SerializeToString())
            writer.close()
            print("Wrote to", output_file)
        except Exception as e:
            raise e

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

    def create_example_pandas(self, row, CONTINUOUS_COLUMNS, CATEGORICAL_COLUMNS, label, label_type):
        """
        Make TFRecord Extend row (Example)
        TFRecord를 만들기 위한 Example을 만든다.

        """
        try:
            example = tf.train.Example()
            _CONTINUOUS_COLUMNS = CONTINUOUS_COLUMNS[:]
            _CATEGORICAL_COLUMNS = CATEGORICAL_COLUMNS[:]
            #_CONTINUOUS_COLUMNS.remove("fnlwgt")
            try:
                if label in _CATEGORICAL_COLUMNS:
                    _CATEGORICAL_COLUMNS.remove(label)
                if label in _CONTINUOUS_COLUMNS:
                    _CONTINUOUS_COLUMNS.remove(label)
            except Exception as e:
                raise Exception(e)

            #TODO: extende cell feature를 여기서 체크할 필요가 있을듯 함
            # tfrecord는 여기서 Label을 변경한다. 나중에 꺼낼때 답이 없음 Tensor 객체로 추출되기 때문에 그러나 H5는 feeder에서 변환해주자
            le = LabelEncoder()
            le.fit(self.combined_label_list)

            for col, value in row.items():
                #print(col)
                #print(value)
                if col in _CATEGORICAL_COLUMNS:
                    if isnan(value):
                        value = ""
                    example.features.feature[col].bytes_list.value.extend([str.encode(value)])
                elif col in _CONTINUOUS_COLUMNS:
                    if isnan(value):
                        value = 0.0
                    #example.features.feature[col].int64_list.value.extend([int(value)])
                    example.features.feature[col].float_list.value.extend([float(value)])

                    #example.features.feature[col].flo
                #'income_bracket'
                #'fnlwgt'
                if col == label:
                    #example.features.feature['label'].int64_list.value.extend([int(">50K" in value)])

                    #Todo Category? Continuous?

                    #ori = int(">50K" in value)
                    #print("original label convert" + str(ori))
                    if label_type == "CONTINUOUS":
                        example.features.feature['label'].int64_list.value.extend([int(value)])
                    else:
                        trans = le.transform([value])[0] # 무조껀 0번째임
                        example.features.feature['label'].int64_list.value.extend([int(trans)])
                        #inverse_label = le.inverse_transform([trans])

                    #print(value + " ori : " + str(ori) + "    convert label convert :" + str(trans) + "    inverse label :" + str(inverse_label))

                    #print("inverse label convert" + str(inverse_label))

            return example
        except Exception as e:
            logging.error("make tfrecord column {0} value {0}".format(col,value))
            logging.error("make tfrecord rows {0}".format(row))
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
                file_path = utils.get_filepaths(self.data_store_path, 'tfrecords')
            else:
                file_path = utils.get_filepaths(self.data_store_path, 'h5')
            return file_path
        except Exception as e:
            raise Exception(e)

    def load_csv_by_pandas(self, data_path):
        """
        read csv
        :param data_path:
        :return:data_path
        """
        try :
            df_csv_read = pd.read_csv(tf.gfile.Open(data_path),
                                      skipinitialspace=True,
                                      engine="python",
                                      encoding='utf-8-sig')
            return df_csv_read
        except Exception as e :
            raise Exception (e)

    def make_column_types (self, df, node_id, data_dfconf_list):
        """
        csv를 읽고 column type을 계산하여 data_conf에 저장(data_conf가 비어있을때 )
        :param df:
        :param conf_data:
        """
        try:

            data_conf, data_conf_unique_json =self.set_dataconf_for_checktype(df, node_id, data_dfconf_list )
            #self.data_conf = self.set_dataconf_for_checktype(df, node_id )
            data_conf_unique_cnt = self.make_unique_value_each_column(df,node_id)
            data_conf.update(data_conf_unique_cnt)
            dataconf_nodes = self._get_forward_node_with_type(node_id, 'dataconf')
            #if(len(dataconf_nodes) > 0 or ('evaldata' in self.node_name)) :
            wf_data_conf_node = wf_data_conf(data_dfconf_list)
            #처음일때 Cell_feature update Eval일때는 Unique Value 업데이트
            if self.dataconf_first_time_check(wf_data_conf_node, node_id):
                self.set_default_dataconf_from_csv(wf_data_conf_node, node_id, data_conf)
                self.set_default_dataconf_from_csv(wf_data_conf_node, node_id, data_conf_unique_cnt)
                self.set_default_dataconf_from_csv(wf_data_conf_node, node_id, data_conf_unique_json)
            if self.dataconf_eval_time_check(wf_data_conf_node, node_id):
                self.set_default_dataconf_from_csv(wf_data_conf_node, node_id, data_conf_unique_json)
            #    self.set_default_dataconf_from_csv(wf_data_conf_node, node_id, data_conf)
            return data_conf
        except Exception as e:
            logging.info("make column type Error {0}  line no({1})".format(e, e.__traceback__.tb_lineno))
            raise Exception(e)


    def dataconf_first_time_check(self, _wf_data_conf_node, _node_name):
        """
        data_conf가 비어있거나, DataNode일때만 업데이트 하도록 한다.
        :param data_dfconf_list (nn00001_1_dataconf_node)
        :return True:
        """
        _value = False
        #wf_data_conf_node = wf_data_conf(data_dfconf_list)
        if (len(_wf_data_conf_node.cell_feature) == 0 or 'conf' not in _wf_data_conf_node.__dict__) and ('data_node' in _node_name):
            _value = True
        return _value

    def dataconf_eval_time_check(self, _wf_data_conf_node, _node_name):
        """
        data conf가 있어도, eval이면 unique값만 추가한다.
        :param data_dfconf_list (nn00001_1_dataconf_node)
        :return True:
        """
        _value = False
        #wf_data_conf_node = wf_data_conf(data_dfconf_list)
        # if hasattr(_wf_data_conf_node, 'cell_feature'):
        #     if (len(_wf_data_conf_node.cell_feature) > 0 and ('evaldata' in _node_name)):
        #         _value = True\
        if ('evaldata' in _node_name):
             _value = True
        return _value


    def make_unique_value_each_column (self, df, node_id):
        """ Dataframe중 범주형 데이터를 찾아서 유일한 값의 갯수를 반환한다 
            Unique Value return in Dataframe

        Args:
          params:
            * df : dataframe
            * node_id: nnid

        Returns:
            json

        Raises:
        """
        try:
            data_conf = dict()
            column_cate_unique = dict()
            numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
            for i, v in df.dtypes.iteritems():
                if (str(v) not in numerics):  # maybe need float
                    column_cate_unique[i] = df[i].unique().size
            data_conf['unique_cell_feature'] = column_cate_unique
            data_conf_json_str = json.dumps(data_conf)
            data_conf_json = json.loads(data_conf_json_str)
            return data_conf_json
        except Exception as e:
            logging.error("make_unique_value_each_column error : {0}, {1}".format(i,v))
            raise e


    def set_default_dataconf_from_csv(self,wf_data_config, node_id, data_conf):
        """

        :param wf_data_config, df, nnid, ver, node:
        :param conf_data:
        tfrecord 때문에 항상 타입을 체크하고 필요할때만 저장
        """
        # #TODO : set_default_dataconf_from_csv 파라미터 정리 필요
        nnid = node_id.split('_')[0]
        ver = node_id.split('_')[1]
        data_node = "dataconf_node"
        wf_data_config.put_step_source(nnid, ver, data_node, data_conf)

    def set_dataconf_for_checktype(self, df, node_id, data_dfconf_list):
        """
        csv를 읽고 column type을 계산하여 data_conf에 저장(data_conf가 비어있을때 )
        카테고리 컬럼은 Unique 한 값을 구해서 cell_feature_unique에 넣어줌(Keras용)
        
        :param wf_data_config, df, nnid, ver, node:
        :param conf_data:
        """
        try:
            #TODO : set_default_dataconf_from_csv 파라미터 정리 필요
            data_conf = dict()
            data_conf_unique_v = dict()
            data_conf_col_unique_v = dict()
            data_conf_col_type = dict()

            numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']

            # Wdnn인경우 data_dfconf가 무조껀 한개만 존재 하므로 아래와 같은 로직이 가능
            if len(data_dfconf_list) > 0:
                _wf_data_conf = wf_data_conf(data_dfconf_list)
                #_cell_feature = _wf_data_conf.cell_feature if hasattr(_wf_data_conf,'cell_feature') else list() #처음 입려할때 라벨벨류가 없으면 빈 리스트 넘김
                _cell_feature_unique = _wf_data_conf.cell_feature_unique if hasattr(_wf_data_conf,
                                                                      'cell_feature_unique') else list()  # 처음 입려할때 라벨벨류가 없으면 빈 리스트 넘김
            for i, v in df.dtypes.iteritems():
                # label
                column_dtypes = dict()
                column_unique_value = dict()
                col_type = ''
                if (str(v) in numerics):  # maybe need float
                    col_type = 'CONTINUOUS'
                    columns_unique_value = list()
                else:
                    col_type = 'CATEGORICAL'
                    #columns_unique_value = pd.unique(df[i].values.ravel()).tolist()  # null처리 해야함
                    columns_unique_value = pd.unique(df[i].fillna('').values.ravel()).tolist()  # null처리 해야함
                column_dtypes['column_type'] = col_type

                #원래 가지고 있던 카테고리 컬럼별 유일한 값
                origin_feature_unique = _cell_feature_unique[i].get('column_u_values') if (i in _cell_feature_unique) else list()
                combined_col_u_list = utils.get_combine_label_list(origin_feature_unique, columns_unique_value)
                #읽어와서 추가되면 뒤에 붙여준다.
                column_unique_value['column_u_values'] = combined_col_u_list

                data_conf_col_type[i] = column_dtypes
                data_conf_col_unique_v[i] = column_unique_value
            data_conf['cell_feature'] = data_conf_col_type
            data_conf_unique_v['cell_feature_unique'] = data_conf_col_unique_v

            #json으로 바꿔줌
            data_conf_json_str = json.dumps(data_conf)
            data_conf_json = json.loads(data_conf_json_str)
            data_conf_unique_json_str = json.dumps(data_conf_unique_v)
            data_conf_unique_json = json.loads(data_conf_unique_json_str)

            return data_conf_json, data_conf_unique_json
        except Exception as e:
            logging.error("set_dataconf_for_checktype {0} {1}".format(e, e.__traceback__.tb_lineno))


    def set_dataconf_for_labels(self, df, label):
        """
        csv를 읽고 label의 distict 값을 가져옴
        Extract distinct label values
        :param wf_data_config, df, nnid, ver, node:
        :param conf_data:
        """
        #TODO : set_default_dataconf_from_csv 파라미터 정리 필요

        label_values = dict()

        label_values = pd.unique(df[label].values.ravel().astype('str')).tolist()
        # DATACONF_FRAME_CALL
        #wf_data_config.put_step_source(node_id, label_values)
        return label_values

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
            self.combine_label_list = list()
        except Exception as e :
            raise Exception ("WorkFlowDataFrame parms are not set " + str(e))

