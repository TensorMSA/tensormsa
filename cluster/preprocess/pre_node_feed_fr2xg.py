from cluster.preprocess.pre_node_feed import PreNodeFeed
import tensorflow as tf
import pandas as pd
from master.workflow.dataconf.workflow_dataconf_frame import WorkflowDataConfFrame as wf_data_conf
from master.workflow.data.workflow_data_frame import WorkFlowDataFrame as wf_data_frame
from common import utils
from sklearn.preprocessing import LabelEncoder
import logging
from master.network.nn_common_manager import NNCommonManager

class PreNodeFeedFr2xg(PreNodeFeed):
    # @property
    # def input_paths(self):
    #     return self.input_paths

    # @input_paths.setter
    # def input_paths(self, value):
    #     self.input_paths = value
    def set_for_predict(self, nnid=None):
        self.pointer = 0
        if nnid != None:
            self._init_node_parm(nnid)



    def run(self, conf_data):
        """
        override init class
        """
        #전 노드중 dataconf를 찾아 온다 wdnn만 가능
        #전체 노드중 data_conf를 넣어서 만든다. 1개 밖에 없음

        try:
            logging.info("PreNodeFeedFr2xg Xgboost Run called")
            # init data setup
            self._init_train_parm(conf_data)
            #self._init_value()


            #data_conf_node_name = self.node_name.split('_')[0] + "_" + self.node_name.split('_')[1] +"_dataconf_node"
            #self._init_node_parm(data_conf_node_name)
            super(PreNodeFeedFr2xg, self).run(conf_data)
            #input_features = self.create_feature_columns()

            #testself.node_name.split('_')[1]
            #self.multi_queue_and_h5_print(self.input_paths[0])
        except Exception as e:
            logging.error("PreNodeFeedFr2xg Xgboost Run {0}".format(e))
            raise e


    def input_fn2(self, mode, data_file, df, dataconf):
        """Wide & Deep Network input tensor maker
            V1.0    16.11.04    Initial
                :param df : dataframe from hbase
                :param df, nnid
                :return: tensor sparse, constraint """
        try:
            #self.df_validation(df, dataconf)

            # remove NaN elements
            _label = self.label
            _label_calues = self.label_values

            #df = df.dropna(how='any', axis=0)
            df_test = df.dropna(how='any', axis=0)

            ##Make List for Continuous, Categorical Columns
            CONTINUOUS_COLUMNS = []
            CATEGORICAL_COLUMNS = []
            ##Get datadesc Continuous and Categorical infomation from Postgres nninfo
            # json_string = self.get_json_by_nnid(nnid) # DATACONF
            # json_object = json_string

            le = LabelEncoder()
            le.fit(_label_calues)

            #Todo 트레이닝 하기 위해서 바꿔야함

            j_feature = dataconf['cell_feature']
            for cn, c_value in j_feature.items():
                if c_value["column_type"] == "CATEGORICAL":
                    CATEGORICAL_COLUMNS.append(cn)
                elif c_value["column_type"] == "CONTINUOUS":
                    CONTINUOUS_COLUMNS.append(cn)
                elif c_value["column_type"] == "CATEGORICAL_KEY":
                    CATEGORICAL_COLUMNS.append(cn)

                    # {"data_conf": {"label": {"income_bracket": "LABEL"}, "cross_cell": {"col1": ["occupation", "education"], "col2": ["native_country", "occupation"]}, "cell_feature": {"age": {"column_type": "CONTINUOUS"}, "race": {"column_type": "CATEGORICAL"}, "gender": {"keys": ["female", "male"], "column_type": "CATEGORICAL_KEY"}, "education": {"column_type": "CATEGORICAL"}, "workclass": {"column_type": "CATEGORICAL"}, "occupation": {"column_type": "CATEGORICAL"}, "capital_gain": {"column_type": "CONTINUOUS"}, "capital_loss": {"column_type": "CONTINUOUS"}, "relationship": {"column_type": "CATEGORICAL"}, "education_num": {"column_type": "CONTINUOUS"}, "hours_per_week": {"column_type": "CONTINUOUS"}, "marital_status": {"column_type": "CATEGORICAL"}, "native_country": {"column_type": "CATEGORICAL"}}, "Transformations": {"col1": {"boundaries": [18, 25, 30, 35, 40, 45, 50, 55, 60, 65], "column_name": "age"}}}}
            # Check Continuous Column is exsist?
            if len(CONTINUOUS_COLUMNS) > 0:
                # print(CONTINUOUS_COLUMNS)
                #null 값 처리를 위해서 fillna사용
                continuous_cols = {k: tf.constant(df[k].fillna(0).values) for k in CONTINUOUS_COLUMNS}
                #continuous_cols = {k: tf.float32(df[k].fillna(0.).values) for k in CONTINUOUS_COLUMNS}
            # Check Categorical Column is exsist?
            if len(CATEGORICAL_COLUMNS) > 0:

                for k in CATEGORICAL_COLUMNS:
                    df[k] = df[k].astype('str')

                categorical_cols = {k: tf.SparseTensor(
                    indices=[[i, 0] for i in range(df[k].size)],
                    values=df[k].fillna('').replace(['nan','Nan'],'').values,
                    dense_shape=[df[k].size, 1])
                                    for k in CATEGORICAL_COLUMNS}

            # Merges the two dictionaries into one.
            feature_cols = {}
            if (len(CONTINUOUS_COLUMNS) > 0):
                feature_cols.update(continuous_cols)
            if len(CATEGORICAL_COLUMNS) > 0:
                feature_cols.update(categorical_cols)

            feature_cols.pop(_label)
            # dataconf
            #LABEL_COLUMN = 'label'
            #df[LABEL_COLUMN] = (df['income_bracket'].apply(lambda x: '>50K' in x)).astype(int)
            if self.label_type == "CONTINUOUS":
                df["label"] = df[_label].astype(int)
            else:
                #trans = le.transform([value])[0]  # 무조껀 0번째임
                #example.features.feature['label'].int64_list.value.extend([int(trans)])
                lable_encoder_func = lambda x: le.transform([x])
                df["label"] = df[_label].map(lable_encoder_func).astype(int)
                #label_encode = le.transform(label_list)
            label = tf.constant(df["label"].values)

            return feature_cols, label
        except Exception as e:
            print("Error Message : {0} cause by {1} ".format(e), e.__traceback__.tb_lineno)
            raise Exception(e)

    def _convert_data_format(self, file_path, index):
        """
        just pass hdf5 file chunk
        :param file_path:
        :param index:
        :return:
        """
        # try:
        #     h5file = h5py.File(file_path, mode='r')
        #     raw_data = h5file['rawdata']
        #     return raw_data[index.start : index.stop]
        # except Exception as e:
        #     raise Exception(e)
        # finally:
        #     h5file.close()
        # type4 partial read
        #Todo 할때마다 계속 파일을 읽는게 올바른 것인가?
        try:
            store = pd.HDFStore(file_path)
            nrows = store.get_storer('table1').nrows
            chunksize = 100

            #for i in range(nrows // chunksize + 1):
            chunk = store.select('table1',
                                 start=index.start,
                                 stop=index.stop)
        except Exception as e:
             raise Exception(e)
        finally:
            store.close()
        return chunk

    def data_size(self):
        try:
            store = pd.HDFStore(self.input_paths[self.pointer])
            return store.get_storer('table1').nrows
        except Exception as e:
            raise Exception(e)
        finally:
            store.close()


    def _init_node_parm(self, key):
        """
        Init parameter from workflow_data_frame
        :return:
        """
        try :
            _wf_data_conf = wf_data_conf(key)
            self.label = _wf_data_conf.label
            self.cell_feature= _wf_data_conf.cell_feature
            self.cross_cell = _wf_data_conf.cross_cell
            self.extend_cell_feature = _wf_data_conf.extend_cell_feature
            self.label_values = _wf_data_conf.label_values
            self.label_type = _wf_data_conf.label_type
            if hasattr(self, "node_name"): #bugfix node_name이 없는 경우 에러 안나게 처리
                if 'test' in self.__dict__.get("node_name"):
                    _wf_data_conf = wf_data_frame(key.split('_')[0] + '_' + key.split('_')[1] + '_' + 'evaldata')
                    self.multi_node_flag = _wf_data_conf.multi_node_flag
                else :
                    _wf_data_conf = wf_data_frame(key.split('_')[0] + '_' + key.split('_')[1] + '_' + 'data_node')
                    self.multi_node_flag = _wf_data_conf.multi_node_flag

        except Exception as e :
            raise Exception ("WorkFlowDataFrame parms are not set " + str(e))

    def _init_train_parm(self, conf_data):
        # get initial value
        self.conf_data = conf_data
        self.cls_pool = conf_data["cls_pool"]
        self.nn_id = conf_data["nn_id"]
        self.wf_ver = conf_data["wf_ver"]
        self.node_id = conf_data["node_id"]
        graph = NNCommonManager().get_nn_node_name(conf_data["nn_id"])
        for net in graph:
            if net['fields']['graph_node'] == 'netconf_node':
                self.netconf_node = net['fields']['graph_node_name']
            if net['fields']['graph_node'] == 'netconf_feed':
                self.train_feed_name = self.nn_id + "_" + self.wf_ver + "_" + net['fields']['graph_node_name']
            if net['fields']['graph_node'] == 'eval_feed':
                self.eval_feed_name = self.nn_id + "_" + self.wf_ver + "_" + net['fields']['graph_node_name']
        self.feed_node = self.get_prev_node()
