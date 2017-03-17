class NeuralCommonWdnn():
    pass
import tensorflow as tf
import json
import tempfile
from django.conf import settings
from sklearn.preprocessing import LabelEncoder

#
#
# flags = tf.app.flags
# FLAGS = flags.FLAGS
# flags.DEFINE_string("model_type", "wide_n_deep",
#                     "Valid model types: {'wide', 'deep', 'wide_n_deep'}.")
# flags.DEFINE_integer("train_steps", 10000, "Number of training steps.")
#
# """
# WDNN NETWORK COMMON CLASS
#     WDNN Network needs input_fn, wdnn_build function.
# """
#
# class WdnnCommonManager:
#     def __init__(self):
#
#     def input_fn(self, df, nnid):
#         """Wide & Deep Network input tensor maker
#             V1.0    16.11.04    Initial
#                 :param df : dataframe from hbase
#                 :param df, nnid
#                 :return: tensor sparse, constraint """
#         try:
#
#             ##Make List for Continuous, Categorical Columns
#             CONTINUOUS_COLUMNS = []
#             CATEGORICAL_COLUMNS = []
#             ##Get datadesc Continuous and Categorical infomation from Postgres nninfo
#             json_string = self.get_json_by_nnid(nnid) # DATACONF
#             json_object = json_string
#
#             j_feature = json_object['cell_feature']
#             for cn, c_value in j_feature.items():
#               if c_value["column_type"] == "CATEGORICAL":
#                   CATEGORICAL_COLUMNS.append(cn)
#               elif c_value["column_type"] == "CONTINUOUS":
#                   CONTINUOUS_COLUMNS.append(cn)
#               elif c_value["column_type"] =="CATEGORICAL_KEY":
#                   CATEGORICAL_COLUMNS.append(cn)
#
#             # Check Continuous Column is exsist?
#             if len(CONTINUOUS_COLUMNS)>0 :
#                 #print(CONTINUOUS_COLUMNS)
#
#                 continuous_cols = {k: tf.constant(df[k].values) for k in CONTINUOUS_COLUMNS}
#             # Check Categorical Column is exsist?
#             if len(CATEGORICAL_COLUMNS) > 0 :
#
#                 for k in CATEGORICAL_COLUMNS:
#                     df[k] = df[k].astype('str')
#                 categorical_cols = {k: tf.SparseTensor(
#                   indices=[[i, 0] for i in range(df[k].size)],
#                   values=df[k].values,
#                   shape=[df[k].size, 1])
#                                   for k in CATEGORICAL_COLUMNS}
#
#             # Merges the two dictionaries into one.
#             feature_cols = {}
#             if(len(CONTINUOUS_COLUMNS)>0):
#
#                 feature_cols.update(continuous_cols)
#             if len(CATEGORICAL_COLUMNS) > 0:
#
#                 feature_cols.update(categorical_cols)
#
#             #Get label distinct list from postgres 16.12.04
#             json_string = WdnnCommonManager.get_all_info_json_by_nnid(self, nnid=nnid)
#             _label_list = json_string['datasets']
#
#             label_list = eval(_label_list)
#             le = LabelEncoder()
#             le.fit(label_list)
#             lable_encoder_func = lambda x: le.transform([x])
#             df['label'] = df['label'].map(lable_encoder_func).astype(int)
#             label_encode = le.transform(label_list)
#
#             label = tf.constant(df["label"].values)
#
#             return feature_cols, label
#         except Exception as e:
#             print("Error Message : {0}".format(e))
#             raise Exception(e)
#
#     def get_json_by_nnid(self,nnid):
#         """get network configuration info json
#         :param nnid
#         :return: json string """
#
#         datadesc = netconf.load_ori_format(nnid)
#         result = json.loads(datadesc)
#
#         return result
#     def get_all_info_json_by_nnid(self,nnid):
#         """get network configuration info json
#         :param nnid
#         :return: json string """
#         result = netconf.get_network_config(nnid)
#
#         return result
#
#     def wdnn_build(self,nnid, model_dir = "No", train=True):
#         """ wide & deep netowork builder
#             :param nnid
#             :param model_dir : directory of chkpoint of wdnn model
#             :param train : train or predict
#             :return: tensorflow network model """
#         try:
#
#             conf,hidden_layers_value,json_object, label_object  = self.get_init_info_wdnn(nnid)
#
#             #Check Train or Predict
#             if(train):
#                 #model_dir = settings.HDFS_MODEL_ROOT + "/"+nnid + "/"+tempfile.mkdtemp().split("/")[2]
#                 model_dir = settings.HDFS_MODEL_ROOT + "/" + nnid
#             else:
#                 if(model_dir != "No"):
#                     model_dir = model_dir
#
#             label_cnt = len(list(label_object))
#
#             # continuous, categorical and embeddingforCategorical(deep) list
#             featureColumnCategorical = {}
#             featureColumnContinuous = {}
#             featureDeepEmbedding={}
#             j_feature = json_object["cell_feature"]
#
#
#             for cn, c_value in j_feature.items(): #change 3.5python
#
#
#                 if c_value["column_type"] == "CATEGORICAL":
#                     featureColumnCategorical[cn] = tf.contrib.layers.sparse_column_with_hash_bucket(
#                         cn, hash_bucket_size=1000)
#                 elif c_value["column_type"] == "CATEGORICAL_KEY":
#                     featureColumnCategorical[cn] = tf.contrib.layers.sparse_column_with_keys(column_name=cn,keys=c_value["keys"])
#                 elif c_value["column_type"] == "CONTINUOUS": #CONTINUOUS
#                     featureColumnContinuous[cn] = tf.contrib.layers.real_valued_column(cn)
#             # embedding column add
#             for key, value in featureColumnCategorical.items(): #3.5python
#
#                 featureDeepEmbedding[key] = tf.contrib.layers.embedding_column(value, dimension=8)
#
#             wide_columns = []
#             for sparseTensor in featureColumnCategorical:
#                 wide_columns.append(featureColumnCategorical[sparseTensor])
#
#             # cross_cell checks null
#             cross_col1 = []
#             if 'cross_cell' in json_object: #json_object.has_key('cross_cell'):
#                 j_cross = json_object["cross_cell"]
#                 for jc, values in j_cross.items():
#
#                     for c_key, c_value in values.items(): #3.5python
#                         cross_col1.append(featureColumnCategorical[c_value])
#                     wide_columns.append(tf.contrib.layers.crossed_column(cross_col1,hash_bucket_size=int(1e4)))
#
#             ##Transformations column for wide
#             transfomation_col= {}
#             if 'Transformations' in json_object: #json_object.has_key('Transformations'):
#                 j_boundaries = json_object["Transformations"]
#                 for jc, values in j_boundaries.items(): #3.5python
#
#                     trans_col_name = values["column_name"]
#                     trans_boundaries = values["boundaries"]
#
#                     rvc = featureColumnContinuous[trans_col_name]
#
#                     transfomation_col[jc] = tf.contrib.layers.bucketized_column(featureColumnContinuous[trans_col_name],trans_boundaries)
#                     wide_columns.append(tf.contrib.layers.bucketized_column(featureColumnContinuous[trans_col_name],trans_boundaries))
#
#             deep_columns = []
#             for realTensor in featureColumnContinuous:
#                 deep_columns.append(featureColumnContinuous[realTensor])
#
#             for embeddingTensor in featureDeepEmbedding:
#                 deep_columns.append(featureDeepEmbedding[embeddingTensor])
#
#             if FLAGS.model_type == "wide_n_deep":
#
#                 m = tf.contrib.learn.DNNLinearCombinedClassifier(
#                     model_dir=model_dir,
#                     linear_feature_columns=wide_columns,
#                     dnn_feature_columns=deep_columns,
#                     n_classes=label_cnt,  # 0.11 bug
#                     dnn_hidden_units=hidden_layers_value)
#             elif FLAGS.model_type == "wide":
#
#                 m = tf.contrib.learn.LinearClassifier(model_dir=model_dir,
#                                                       feature_columns=wide_columns
#                                                       ,enable_centered_bias = True)
#             elif FLAGS.model_type =="deep":
#
#                 m = tf.contrib.learn.DNNClassifier(model_dir=model_dir,
#                                                        feature_columns=deep_columns,
#                                                        n_classes = label_cnt, #0.11 bug
#                                                        hidden_units=hidden_layers_value)
#
#             rv = self.network_update(nnid,model_dir)
#
#             return m
#         except Exception as e:
#             print("Error Message : {0}".format(e))
#             raise Exception(e)
#     def get_init_info_wdnn(self, nnid):
#         """ Get infomation of Wdnn initial
#             :param nnid
#             :param model_dir : directory of chkpoint of wdnn model
#         """
#         json_string = netconf.load_ori_format(nnid)
#         json_object = json.loads(json_string)
#
#         conf = netconf.load_conf(nnid)
#         hidden_layers_value = conf.layer
#         result_temp = netconf.get_network_config(nnid)
#         label_cnt = json.loads(json.dumps(result_temp))
#         label_object  = label_cnt["datasets"]
#
#         return conf, hidden_layers_value, json_object, label_object
#
#     def network_update(self,nnid, model_dir):
#         """ Wide Deep Network update model directory
#             :param nnid
#             :param model_dir : directory of chkpoint of wdnn model
#         """
#         try:
#             jd = jc.load_obj_json("{}")
#             jd.query = model_dir
#             jd.nn_id = nnid
#             netconf.update_network(jd)
#             return_data = {"status": "200", "result": nnid}
#
#         except Exception as e:
#             return_data = {"status": "404", "result": str(e)}
#             print("Error Message : {0}".format(e))
#             raise Exception(e)
#         finally:
#             return return_data