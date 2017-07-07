from cluster.preprocess.pre_node_feed import PreNodeFeed
import tensorflow as tf
import pandas as pd
from master.workflow.dataconf.workflow_dataconf_frame import WorkflowDataConfFrame as wf_data_conf
from master.workflow.data.workflow_data_frame import WorkFlowDataFrame as wf_data_frame
from common import utils
from sklearn.preprocessing import LabelEncoder
import logging

class PreNodeFeedFr2Wdnn(PreNodeFeed):
    """

    """

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
            data_conf_node_name = self.node_name.split('_')[0] + "_" + self.node_name.split('_')[1] +"_dataconf_node"
            self._init_node_parm(data_conf_node_name)
            super(PreNodeFeedFr2Wdnn, self).run(conf_data)
            #input_features = self.create_feature_columns()

            #testself.node_name.split('_')[1]
            self.multi_queue_and_h5_print(self.input_paths[0])
        except Exception as e:
            logging.error("fidder error {0}".format(e))
            raise e

    def _convert_data_format(self, obj, index):
        pass

    def create_feature_columns(self, dataconf = None):
        """
        Get feature columns for tfrecord reader
        TFRecord에서 feature를 추출
        """


        _cell_feature = self.cell_feature
        _extend_cell_feature = self.extend_cell_feature
        _label = self.label
        _label_calues = self.label_values

        CONTINUOUS_COLUMNS, CATEGORICAL_COLUMNS = self.make_continuous_category_list(_cell_feature)
        CALCULATED_CONTINUOUS_COLUMNS, CALCULATED_CATEGORICAL_COLUMNS = self.add_none_keys_cate_conti_list(CONTINUOUS_COLUMNS,CATEGORICAL_COLUMNS )

        # cate를 가지고 formon을 돌리는데 카테로 만들고 extend에 key 있으면 key도 추가 하고
        #conti도 for문 돌리고
        #마지막에 set을 어떻게 할지도 중요하고

        category_tensor = dict()
        continuous_tensor = dict()
        for cate_item in CALCULATED_CATEGORICAL_COLUMNS:
            category_tensor[cate_item] = tf.contrib.layers.sparse_column_with_hash_bucket(cate_item, hash_bucket_size=1000)
        for conti_item in CALCULATED_CONTINUOUS_COLUMNS:
            continuous_tensor[conti_item] = tf.contrib.layers.real_valued_column(conti_item, dtype=tf.float32)
        #NONE은 다 처리 되었고
        #KEY를 처리 할려면
        for key_item, value in _extend_cell_feature.items():
            if value.get("column_type") == "CATEGORICAL_KEY":
                category_tensor[key_item] = tf.contrib.layers.sparse_column_with_keys(column_name=key_item, keys=value.get("keys"))

        category_tensor.update(continuous_tensor)
        modi_set = {_v for _v in category_tensor.values()}
        label_modi = tf.contrib.layers.real_valued_column("label", dtype=tf.int64)
        modi_set.add(label_modi)

        #
        # gender = tf.contrib.layers.sparse_column_with_keys(
        #     column_name="sex", keys=["female", "male"])
        # race = tf.contrib.layers.sparse_column_with_keys(
        #     column_name="race", keys=[
        #         "Amer-Indian-Eskimo",
        #         "Asian-Pac-Islander",
        #         "Black",
        #         "Other",
        #         "White"
        #     ])
        #
        #
        #
        # education = tf.contrib.layers.sparse_column_with_hash_bucket(
        #     "education", hash_bucket_size=1000)
        # marital_status = tf.contrib.layers.sparse_column_with_hash_bucket(
        #     "marital_status", hash_bucket_size=100)
        # relationship = tf.contrib.layers.sparse_column_with_hash_bucket(
        #     "relationship", hash_bucket_size=100)
        # workclass = tf.contrib.layers.sparse_column_with_hash_bucket(
        #     "workclass", hash_bucket_size=100)
        # occupation = tf.contrib.layers.sparse_column_with_hash_bucket(
        #     "occupation", hash_bucket_size=1000)
        # native_country = tf.contrib.layers.sparse_column_with_hash_bucket(
        #     "native_country", hash_bucket_size=1000)
        #
        # # Continuous base columns.
        # age = tf.contrib.layers.real_valued_column("age", dtype=tf.int64)
        # education_num = tf.contrib.layers.real_valued_column("education_num", dtype=tf.int64)
        # capital_gain = tf.contrib.layers.real_valued_column("capital_gain", dtype=tf.int64)
        # capital_loss = tf.contrib.layers.real_valued_column("capital_loss", dtype=tf.int64)
        # hours_per_week = tf.contrib.layers.real_valued_column("hours_per_week", dtype=tf.int64)
        #
        # label = tf.contrib.layers.real_valued_column("label", dtype=tf.int64)
        #
        # ori_set =  set([
        #     workclass,
        #     education,
        #     marital_status,
        #     occupation,
        #     relationship,
        #     race,
        #     gender,
        #     native_country,
        #     age,
        #     education_num,
        #     capital_gain,
        #     capital_loss,
        #     hours_per_week,
        #     label,
        # ])

        return modi_set #ori_set



    def input_fn(self, mode, data_file, batch_size, dataconf = None):
        try:


            input_features = self.create_feature_columns()
            features = tf.contrib.layers.create_feature_spec_for_parsing(input_features)

            feature_map = tf.contrib.learn.io.read_batch_record_features(
                file_pattern=[data_file],
                #file_pattern=data_file,
                batch_size=batch_size,
                features=features,
                queue_capacity = 20000,
                name="read_batch_features_{}".format(mode))

            target = feature_map.pop("label")

            #num_epoch =
            print(str(batch_size))
        except Exception as e:
            raise e

        return feature_map, target

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

    def add_none_keys_cate_conti_list(self,conti_list, cate_list ):
        """
        Example 을 위한  Continuous 랑 Categorical을 구분하기 위한 list

        """
        CALCULATED_CONTINUOUS_COLUMNS = list()
        CALCULATED_CATEGORICAL_COLUMNS = list()

        # , "extend_cell_feature":
        # {
        #     "sex": {"keys": ["female", "male"], "column_type": "CATEGORICAL_KEY"}
        #     , "race": {"column_type": "NONE"}
        #     , "marital_status": {"column_type": "NONE"}
        # }

        _extend_cell_feature = self.extend_cell_feature
        _extend_cell_feature_list = list()
        _label = self.label
        for _k, _v in _extend_cell_feature.items():
            if _v.get("column_type") == "CATEGORICAL_KEY":
                _extend_cell_feature_list.append(_k)

        #_extend_cell_feature_list = list(_extend_cell_feature.keys())
        _extend_cell_feature_list.append(_label)
        label_extend_list = list(_extend_cell_feature_list)


        for _,_key in enumerate(label_extend_list):
            if _key in conti_list:
                conti_list.remove(_key)
            if _key in cate_list:
                cate_list.remove(_key)

        # for type_columne, type_value in cell_feature.items():
        #     if type_value["column_type"] == 'CONTINUOUS':
        #         CONTINUOUS_COLUMNS.append(type_columne)
        #     else:
        #         CATEGORICAL_COLUMNS.append(type_columne)
        return conti_list, cate_list

    def multi_queue_and_h5_print(self, file_name):
        #filename = 'adult_data.tfrecords'

        # Queue 는 이런식으로 설정 여기서는 쓰지 않음
        #filename_queue = tf.train.string_input_producer(
        #    [filename], num_epochs=1)

        # 꼭 local variable initial  해야함
        try:
            if self.multi_node_flag == True:
                init_op = tf.local_variables_initializer()

                # Multi Thread로 들고옴
                feature_map, target = self.input_fn(tf.contrib.learn.ModeKeys.EVAL, file_name, 128)

                with tf.Session() as sess:
                    # Start populating the filename queue.
                    sess.run(init_op)
                    coord = tf.train.Coordinator()
                    threads = tf.train.start_queue_runners(coord=coord)

                    tfrecord_list_row = list()  # 출력을 위한 List
                    print_column = True

                    for i in range(3):
                        # Multi Thread에서 넣을것을 Session으로 실행
                        example, label = sess.run([feature_map, target])

                        _row = ""
                        if print_column == True:  # Header를 위한 Column Key 설정 첫줄만
                            tfrecord_list_key = [col for col in example.keys()]
                            tfrecord_list_key.append('label')
                            print_column = False
                            tfrecord_list_row.append(tfrecord_list_key)

                        for i in range(len(example[list(example.keys())[0]])):  # Row를 들고 오기 뭔가 지저분함

                            tfrecord_list_col = list()
                            for _k in example.keys():
                                if str(type(example[_k])).find('Sparse') > -1:  # Sparse는 Bytes로 나와서 Bytes를 String 으로 처리
                                    tfrecord_list_col.append(str(example[_k].values[i].decode()))
                                else:
                                    # numpy도 ndarray로 나와서 [0]을 붙여 정리함
                                    tfrecord_list_col.append(str(example[_k][i][0]))
                            tfrecord_list_col.append(str(label[i][0]))
                            columns_value = tfrecord_list_col
                            tfrecord_list_row.append(columns_value)

                        # 이쁘게 출력하기 위해 Print 함수 설정
                        for item in tfrecord_list_row:
                            print(str(item[0:])[1:-1])

                    coord.request_stop()
                    coord.join(threads)
            else:
                # Todo 할때마다 계속 파일을 읽는게 올바른 것인가?
                try:
                    store = pd.HDFStore(file_name)
                    nrows = store.get_storer('table1').nrows
                    chunksize = 100

                    # for i in range(nrows // chunksize + 1):
                    chunk = store.select('table1')
                    logging.info(chunk)
                except Exception as e:
                    raise Exception(e)
                finally:
                    store.close()
        except Exception as e:
            logging.error("feed just show data {0}".format(e))

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
