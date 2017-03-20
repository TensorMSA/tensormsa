
import tensorflow as tf
import json
import tempfile
from django.conf import settings
from sklearn.preprocessing import LabelEncoder
import numpy as np


flags = tf.app.flags
FLAGS = flags.FLAGS
flags.DEFINE_string("model_type", "wide_n_deep",
                    "Valid model types: {'wide', 'deep', 'wide_n_deep'}.")
flags.DEFINE_integer("train_steps", 10000, "Number of training steps.")

"""
WDNN NETWORK COMMON CLASS
    WDNN Network needs input_fn, wdnn_build function.
"""

class NeuralCommonWdnn():


    # def input_fn(self, df, nnid):
    #     """Wide & Deep Network input tensor maker
    #         V1.0    16.11.04    Initial
    #             :param df : dataframe from hbase
    #             :param df, nnid
    #             :return: tensor sparse, constraint """
    #     try:
    #
    #         ##Make List for Continuous, Categorical Columns
    #         CONTINUOUS_COLUMNS = []
    #         CATEGORICAL_COLUMNS = []
    #         ##Get datadesc Continuous and Categorical infomation from Postgres nninfo
    #         json_string = self.get_json_by_nnid(nnid) # DATACONF
    #         json_object = json_string
    #
    #         j_feature = json_object['cell_feature']
    #         for cn, c_value in j_feature.items():
    #           if c_value["column_type"] == "CATEGORICAL":
    #               CATEGORICAL_COLUMNS.append(cn)
    #           elif c_value["column_type"] == "CONTINUOUS":
    #               CONTINUOUS_COLUMNS.append(cn)
    #           elif c_value["column_type"] =="CATEGORICAL_KEY":
    #               CATEGORICAL_COLUMNS.append(cn)
    #
    #         # Check Continuous Column is exsist?
    #         if len(CONTINUOUS_COLUMNS)>0 :
    #             #print(CONTINUOUS_COLUMNS)
    #
    #             continuous_cols = {k: tf.constant(df[k].values) for k in CONTINUOUS_COLUMNS}
    #         # Check Categorical Column is exsist?
    #         if len(CATEGORICAL_COLUMNS) > 0 :
    #
    #             for k in CATEGORICAL_COLUMNS:
    #                 df[k] = df[k].astype('str')
    #             categorical_cols = {k: tf.SparseTensor(
    #               indices=[[i, 0] for i in range(df[k].size)],
    #               values=df[k].values,
    #               shape=[df[k].size, 1])
    #                               for k in CATEGORICAL_COLUMNS}
    #
    #         # Merges the two dictionaries into one.
    #         feature_cols = {}
    #         if(len(CONTINUOUS_COLUMNS)>0):
    #
    #             feature_cols.update(continuous_cols)
    #         if len(CATEGORICAL_COLUMNS) > 0:
    #
    #             feature_cols.update(categorical_cols)
    #
    #         #Get label distinct list from postgres 16.12.04
    #         json_string = WdnnCommonManager.get_all_info_json_by_nnid(self, nnid=nnid)
    #         _label_list = json_string['datasets']
    #
    #         label_list = eval(_label_list)
    #         le = LabelEncoder()
    #         le.fit(label_list)
    #         lable_encoder_func = lambda x: le.transform([x])
    #         df['label'] = df['label'].map(lable_encoder_func).astype(int)
    #         label_encode = le.transform(label_list)
    #
    #         label = tf.constant(df["label"].values)
    #
    #         return feature_cols, label
    #     except Exception as e:
    #         print("Error Message : {0}".format(e))
    #         raise Exception(e)

    # def get_json_by_nnid(self,nnid):
    #     """get network configuration info json
    #     :param nnid
    #     :return: json string """
    #
    #     datadesc = netconf.load_ori_format(nnid)
    #     result = json.loads(datadesc)
    #
    #     return result
    # def get_all_info_json_by_nnid(self,nnid):
    #     """get network configuration info json
    #     :param nnid
    #     :return: json string """
    #     result = netconf.get_network_config(nnid)
    #
    #     return result

    def wdnn_build(self, model_type, nodeid, hidden_layers, activation_fn, dataconf, model_dir,  train=True):
        """ wide & deep netowork builder
            :param nnid
            :param model_dir : directory of chkpoint of wdnn model
            :param train : train or predict
            :return: tensorflow network model """
        try:


            hidden_layers_value = hidden_layers
            json_object = dataconf #json.load(dataconf)
            data_conf_json = dataconf #json.loads(dataconf)

            label_object  = dataconf

            #Check Train or Predict
            #if(train):
                #model_dir = settings.HDFS_MODEL_ROOT + "/"+nnid + "/"+tempfile.mkdtemp().split("/")[2]
            #    model_dir = settings.HDFS_MODEL_ROOT + "/" + nnid
            #else:
            #    if(model_dir != "No"):
            #        model_dir = model_dir

            #label_cnt = len(list(label_object))

            # continuous, categorical and embeddingforCategorical(deep) list
            #featureColumnCategorical = {}
            featureColumnContinuous = {}
            featureDeepEmbedding={}
            j_feature = data_conf_json["cell_feature"]


            # one line expression change
            # Categorial columns을 Sparse Layer로 만듬 python처럼 한줄로 표시
            featureColumnCategorical = {cn:tf.contrib.layers.sparse_column_with_hash_bucket(cn, hash_bucket_size=1000)
                                        for cn, c_value in j_feature.items()  if c_value["column_type"] == "CATEGORICAL" }
            # 범주형 Categorial columns을 추가 업데이트를 통해 두 딕셔너리를 합침 세련되게
            featureColumnCategorical.update({ cn:tf.contrib.layers.sparse_column_with_keys(column_name=cn,keys=c_value["keys"])
                                        for cn, c_value in j_feature.items() if c_value["column_type"] == "CATEGORICAL_KEY" })

            # Categorucal layer를 emdedding 해서 차원을 줄임
            featureDeepEmbedding = {key:tf.contrib.layers.embedding_column(value, dimension=8) for key, value in featureColumnCategorical.items()}

            # Json에서 Continuous Colums 가져옴
            featureColumnContinuous = {cn:tf.contrib.layers.real_valued_column(cn)
                                    for cn, c_value in j_feature.items() if c_value["column_type"] == "CONTINUOUS"}

            #make wide columns
            #Todo shoud be check is it right? wide colummns is featureColumnCategorical
            wide_columns= [sparseTensor for key, sparseTensor in featureColumnCategorical.items()]

            #Cross cell make
            if data_conf_json.get('cross_cell'):
                cross_column_list = [[featureColumnCategorical[entry_cross] for entry_cross in cross_col] for
                                     key, cross_col in data_conf_json["cross_cell"].items()]
                wide_columns.extend(
                    [tf.contrib.layers.crossed_column(cross_col, hash_bucket_size=int(1e4)) for cross_col in
                     cross_column_list])
                #print("pass")
            #j_cross = data_conf_json["cross_cell"]

            # try one liner but failed but finally success
            #cross_col1 = [featureColumnCategorical[c_value] for jc, values in j_cross.items() for c_key, c_value in values.items()]


            # complete wide colums

            #wide_columns.extend([tf.contrib.layers.crossed_column(cross_col,hash_bucket_size=int(1e4)) for key, cross_col in j_cross.items()])



            if data_conf_json.get('Transformations'):
                #transfomation_col = [ featureColumnContinuous[values['column_name']]  for jc, values in  data_conf_json['Transformations'].items()]
                #trans_boundaries = [ values['boundaries']  for jc, values in  data_conf_json['Transformations'].items()]
                wide_columns.extend([tf.contrib.layers.bucketized_column(featureColumnContinuous[values['column_name']],values['boundaries'])
                                     for key, values in data_conf_json['Transformations'].items()])

            #make deep Columns
            deep_columns = [realTensor for key, realTensor in featureColumnContinuous.items()]

            deep_columns.extend([embedTensor for key, embedTensor in featureDeepEmbedding.items()])
            #wide_columns = []
            if model_type == "wdnn":

                m = tf.contrib.learn.DNNLinearCombinedClassifier(
                    model_dir=model_dir,
                    linear_feature_columns=wide_columns,
                    dnn_feature_columns=deep_columns,
                    #n_classes=2,  # 0.11 bug
                    dnn_hidden_units=hidden_layers_value)


            elif model_type == "wide":

                m = tf.contrib.learn.LinearClassifier(model_dir=model_dir,
                                                      feature_columns=wide_columns
                                                      ,enable_centered_bias = True)
            elif model_type =="deep":

                m = tf.contrib.learn.DNNClassifier(model_dir=model_dir,
                                                       feature_columns=deep_columns,
                                                       #n_classes = label_cnt, #0.11 bug
                                                       hidden_units=hidden_layers_value)




                # deep_columns = []
                # for realTensor in featureColumnContinuous:
                #     deep_columns.append(featureColumnContinuous[realTensor])
                #
                # for embeddingTensor in featureDeepEmbedding:
                #     deep_columns.append(featureDeepEmbedding[embeddingTensor])
                #
                # if FLAGS.model_type == "wide_n_deep":
                #
                #     m = tf.contrib.learn.DNNLinearCombinedClassifier(
                #         model_dir=model_dir,
                #         linear_feature_columns=wide_columns,
                #         dnn_feature_columns=deep_columns,
                #         n_classes=label_cnt,  # 0.11 bug
                #         dnn_hidden_units=hidden_layers_value)
                # elif FLAGS.model_type == "wide":
                #
                #     m = tf.contrib.learn.LinearClassifier(model_dir=model_dir,
                #                                           feature_columns=wide_columns
                #                                           ,enable_centered_bias = True)
                # elif FLAGS.model_type =="deep":
                #
                #     m = tf.contrib.learn.DNNClassifier(model_dir=model_dir,
                #                                            feature_columns=deep_columns,
                #                                            n_classes = label_cnt, #0.11 bug
                #                                            hidden_units=hidden_layers_value)
                #
                # rv = self.network_update(nnid,model_dir)

              #   , "Transformations":
              #   {"col1": {"boundaries": [18, 25, 30, 35, 40, 45, 50, 55, 60, 65], "column_name": "age"}}

            #_BucketizedColumn(source_column=_RealValuedColumn(column_name='age', dimension=1, default_value=None, dtype=tf.float32, normalizer=None), boundaries=(18, 25, 30, 35, 40, 45, 50, 55, 60, 65))
            # ##Transformations column for wide
            # transfomation_col= {}
            # if 'Transformations' in json_object: #json_object.has_key('Transformations'):
            #     j_boundaries = json_object["Transformations"]
            #     for jc, values in j_boundaries.items(): #3.5python
            #
            #         trans_col_name = values["column_name"]
            #         trans_boundaries = values["boundaries"]
            #
            #         rvc = featureColumnContinuous[trans_col_name]
            #
            #         transfomation_col[jc] = tf.contrib.layers.bucketized_column(featureColumnContinuous[trans_col_name],trans_boundaries)
            #         wide_columns.append(tf.contrib.layers.bucketized_column(featureColumnContinuous[trans_col_name],trans_boundaries))
            #
            # deep_columns = []
            # for realTensor in featureColumnContinuous:
            #     deep_columns.append(featureColumnContinuous[realTensor])
            #
            # for embeddingTensor in featureDeepEmbedding:
            #     deep_columns.append(featureDeepEmbedding[embeddingTensor])


            #                         , "cross_cell": {"col2": ["native_country", "occupation"]
                             #, "col1": ["occupation", "education"]}

            #, "cross_cell": {"col12": {"column2_0": "native_country", "column2_1": "occupation"}
            #    , "col1": {"column_1": "occupation", "column_0": "education"}}


            # if 'cross_cell' in json_object: #json_object.has_key('cross_cell'):
            #     j_cross = json_object["cross_cell"]
            #     for jc, values in j_cross.items():
            #
            #         for c_key, c_value in values.items(): #3.5python
            #             cross_col1.append(featureColumnCategorical[c_value])
            #         wide_columns.append(tf.contrib.layers.crossed_column(cross_col1,hash_bucket_size=int(1e4)))


            # for cn, c_value in j_feature.items(): #change 3.5python
            #
            #
            #     if c_value["column_type"] == "CATEGORICAL":
            #         featureColumnCategorical[cn] = tf.contrib.layers.sparse_column_with_hash_bucket(
            #             cn, hash_bucket_size=1000)
            #     elif c_value["column_type"] == "CATEGORICAL_KEY":
            #         featureColumnCategorical[cn] = tf.contrib.layers.sparse_column_with_keys(column_name=cn,keys=c_value["keys"])
            #     elif c_value["column_type"] == "CONTINUOUS": #CONTINUOUS
            #         featureColumnContinuous[cn] = tf.contrib.layers.real_valued_column(cn)
            #
            #
            # # embedding column add
            # for key, value in featureColumnCategorical.items(): #3.5python
            #
            #     featureDeepEmbedding[key] = tf.contrib.layers.embedding_column(value, dimension=8)
            #
            # wide_columns = []
            # for sparseTensor in featureColumnCategorical:
            #     wide_columns.append(featureColumnCategorical[sparseTensor])
            #
            # # cross_cell checks null
            # cross_col1 = []
            # if 'cross_cell' in json_object: #json_object.has_key('cross_cell'):
            #     j_cross = json_object["cross_cell"]
            #     for jc, values in j_cross.items():
            #
            #         for c_key, c_value in values.items(): #3.5python
            #             cross_col1.append(featureColumnCategorical[c_value])
            #         wide_columns.append(tf.contrib.layers.crossed_column(cross_col1,hash_bucket_size=int(1e4)))
            #
            # ##Transformations column for wide
            # transfomation_col= {}
            # if 'Transformations' in json_object: #json_object.has_key('Transformations'):
            #     j_boundaries = json_object["Transformations"]
            #     for jc, values in j_boundaries.items(): #3.5python
            #
            #         trans_col_name = values["column_name"]
            #         trans_boundaries = values["boundaries"]
            #
            #         rvc = featureColumnContinuous[trans_col_name]
            #
            #         transfomation_col[jc] = tf.contrib.layers.bucketized_column(featureColumnContinuous[trans_col_name],trans_boundaries)
            #         wide_columns.append(tf.contrib.layers.bucketized_column(featureColumnContinuous[trans_col_name],trans_boundaries))
            #
            # deep_columns = []
            # for realTensor in featureColumnContinuous:
            #     deep_columns.append(featureColumnContinuous[realTensor])
            #
            # for embeddingTensor in featureDeepEmbedding:
            #     deep_columns.append(featureDeepEmbedding[embeddingTensor])
            #
            # if FLAGS.model_type == "wide_n_deep":
            #
            #     m = tf.contrib.learn.DNNLinearCombinedClassifier(
            #         model_dir=model_dir,
            #         linear_feature_columns=wide_columns,
            #         dnn_feature_columns=deep_columns,
            #         n_classes=label_cnt,  # 0.11 bug
            #         dnn_hidden_units=hidden_layers_value)
            # elif FLAGS.model_type == "wide":
            #
            #     m = tf.contrib.learn.LinearClassifier(model_dir=model_dir,
            #                                           feature_columns=wide_columns
            #                                           ,enable_centered_bias = True)
            # elif FLAGS.model_type =="deep":
            #
            #     m = tf.contrib.learn.DNNClassifier(model_dir=model_dir,
            #                                            feature_columns=deep_columns,
            #                                            n_classes = label_cnt, #0.11 bug
            #                                            hidden_units=hidden_layers_value)
            #
            # rv = self.network_update(nnid,model_dir)
            #
            return m
        except Exception as e:
            print("Error Message : {0}".format(e))
            raise Exception(e)

    #
    # def network_update(self,nnid, model_dir):
    #     """ Wide Deep Network update model directory
    #         :param nnid
    #         :param model_dir : directory of chkpoint of wdnn model
    #     """
    #     try:
    #         jd = jc.load_obj_json("{}")
    #         jd.query = model_dir
    #         jd.nn_id = nnid
    #         netconf.update_network(jd)
    #         return_data = {"status": "200", "result": nnid}
    #
    #     except Exception as e:
    #         return_data = {"status": "404", "result": str(e)}
    #         print("Error Message : {0}".format(e))
    #         raise Exception(e)
    #     finally:
    #         return return_data

    def df_validation(self, df, dataconf):
        print("age df_validation start ")

        for df_value in df["age"].values:
            if(np.issubdtype(df_value, int) == False):
                print("age integer faild " + str(df_value))
            #if(isinstance(df_value, int) == False ):
            #    print("age integer faild " + str(df_value))




    def input_fn(self, df, nnid, dataconf ):
        """Wide & Deep Network input tensor maker
            V1.0    16.11.04    Initial
                :param df : dataframe from hbase
                :param df, nnid
                :return: tensor sparse, constraint """
        try:
            self.df_validation(df, dataconf)

            # remove NaN elements
            df = df.dropna(how='any', axis=0)
            #df_test = df_test.dropna(how='any', axis=0)

            ##Make List for Continuous, Categorical Columns
            CONTINUOUS_COLUMNS = []
            CATEGORICAL_COLUMNS = []
            ##Get datadesc Continuous and Categorical infomation from Postgres nninfo
            #json_string = self.get_json_by_nnid(nnid) # DATACONF
            #json_object = json_string

            j_feature = dataconf['cell_feature']
            for cn, c_value in j_feature.items():
              if c_value["column_type"] == "CATEGORICAL":
                  CATEGORICAL_COLUMNS.append(cn)
              elif c_value["column_type"] == "CONTINUOUS":
                  CONTINUOUS_COLUMNS.append(cn)
              elif c_value["column_type"] =="CATEGORICAL_KEY":
                  CATEGORICAL_COLUMNS.append(cn)

#{"data_conf": {"label": {"income_bracket": "LABEL"}, "cross_cell": {"col1": ["occupation", "education"], "col2": ["native_country", "occupation"]}, "cell_feature": {"age": {"column_type": "CONTINUOUS"}, "race": {"column_type": "CATEGORICAL"}, "gender": {"keys": ["female", "male"], "column_type": "CATEGORICAL_KEY"}, "education": {"column_type": "CATEGORICAL"}, "workclass": {"column_type": "CATEGORICAL"}, "occupation": {"column_type": "CATEGORICAL"}, "capital_gain": {"column_type": "CONTINUOUS"}, "capital_loss": {"column_type": "CONTINUOUS"}, "relationship": {"column_type": "CATEGORICAL"}, "education_num": {"column_type": "CONTINUOUS"}, "hours_per_week": {"column_type": "CONTINUOUS"}, "marital_status": {"column_type": "CATEGORICAL"}, "native_country": {"column_type": "CATEGORICAL"}}, "Transformations": {"col1": {"boundaries": [18, 25, 30, 35, 40, 45, 50, 55, 60, 65], "column_name": "age"}}}}
            # Check Continuous Column is exsist?
            if len(CONTINUOUS_COLUMNS)>0 :
                #print(CONTINUOUS_COLUMNS)

                continuous_cols = {k: tf.constant(df[k].values) for k in CONTINUOUS_COLUMNS}
            # Check Categorical Column is exsist?
            if len(CATEGORICAL_COLUMNS) > 0 :

                for k in CATEGORICAL_COLUMNS:
                    df[k] = df[k].astype('str')
                # _indices = [[i, 0] for i in range(df['race'].size)]
                # _values = df['race'].values
                # _shape = [df['race'].size, 1]
                #
                # test_tensor3 = tf.SparseTensor(indices=[[0, 0], [1, 2]], values=[1, 2], dense_shape=[3, 4])
                #
                # test_Tensor2  = tf.SparseTensor(indices = _indices, values = _values,dense_shape = _shape )
                #
                # testTensor = tf.SparseTensor(
                #   indices=[[i, 0] for i in range(df['race'].size)],
                #   values=df['race'].values,
                #   dense_shape=[df['race'].size, 1])

                categorical_cols = {k: tf.SparseTensor(
                  indices=[[i, 0] for i in range(df[k].size)],
                  values=df[k].values,
                    dense_shape=[df[k].size, 1])
                                  for k in CATEGORICAL_COLUMNS}
            # categorical_cols = {k: tf.SparseTensor(
            #     indices=[[i, 0] for i in range(df[k].size)],
            #     values=df[k].values,
            #     shape=[df[k].size, 1])
            #                     for k in CATEGORICAL_COLUMNS}

            # Merges the two dictionaries into one.
            feature_cols = {}
            if(len(CONTINUOUS_COLUMNS)>0):

                feature_cols.update(continuous_cols)
            if len(CATEGORICAL_COLUMNS) > 0:

                feature_cols.update(categorical_cols)

            #test용도
            #feature_cols = categorical_cols

            #Get label distinct list from postgres 16.12.04
            #json_string = WdnnCommonManager.get_all_info_json_by_nnid(self, nnid=nnid)
            #dataconf
            LABEL_COLUMN = 'label'
            df[LABEL_COLUMN] = (df['income_bracket'].apply(lambda x: '>50K' in x)).astype(int)

            #_label_list = json_string['datasets']

            #label_list = eval(_label_list)
            #le = LabelEncoder()
            #le.fit(label_list)
            #lable_encoder_func = lambda x: le.transform([x])
            #df['label'] = df['label'].map(lable_encoder_func).astype(int)
            #label_encode = le.transform(label_list)

            label = tf.constant(df["label"].values)

            return feature_cols, label
        except Exception as e:
            print("Error Message : {0}".format(e))
            raise Exception(e)