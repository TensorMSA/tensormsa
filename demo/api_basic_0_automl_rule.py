import requests
import json, os

url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8989")

##############################################################################################################################
# cnn
##############################################################################################################################
resp = requests.post('http://' + url + '/api/v1/type/automl/state/rule/graph_id/cnn/',
                     json=
                     {
                         "netconf_node" :{
                                             "param":{"traincnt": {"type":"int","option":10,"auto":False}
                                                      ,"epoch": {"type":"int","option":10,"auto":False}
                                                      ,"batch_size":{"type":"int","option":None,"auto":[100,1000000,100]}
                                                      ,"predictcnt": {"type":"int","option":5,"auto":False}
                                                      ,"predlog": {"type":"sel","option":["N","Y"],"auto":False}
                                             },
                                             "config": {"num_classes":{"type":"int","option":1,"auto":False}
                                                        ,"learnrate": {"type":"int","option":None,"auto":[0.0001,0.1,0.001]}
                                                        ,"layeroutputs":{"type":"int","option":None,"auto":[5,100,3]}
                                                        ,"net_type":{"type":"str","option":"cnn","auto":False}
                                                        ,"eval_type":{"type":"sel","option":["category"],"auto":False}
                                                        ,"optimizer":{"type":"sel","option":["AdamOptimizer","RMSPropOptimizer"],"auto":False}
                                                         }
                                             ,"layer1": {"active": {"type":"sel","option":["relu"],"auto":False},
                                                         "cnnfilter": {"type":"int","option":[3, 3],"auto":False},
                                                         "cnnstride": {"type":"int","option":[1, 1],"auto":False},
                                                         "maxpoolmatrix": {"type":"int","option":[2, 2],"auto":False},
                                                         "maxpoolstride": {"type":"int","option":[2, 2],"auto":False},
                                                         "padding": {"type":"sel","option":["SAME", "NONE"],"auto":False},
                                                         "droprate": {"type":"int","option":None,"auto":[0.0,1.0,0.1]},
                                                         "layercnt":{"type":"int","option":None,"auto":[1,6,1]}
                                                        }
                                             ,"out": {"active": {"type":"sel","option":["softmax","relu",'tanh',"sigmoid"],"auto":False},
                                                       "node_out": {"type":"int","option":None,"auto":[600,2000,5]},
                                                       "padding": {"type":"sel","option":["SAME", "NONE"],"auto":False}
                                                    }
                                             ,"labels":{"type":"list","option":[],"auto":False}
                                        },
                         "netconf_data"    :{
                                             "type":{"type":"sel","option":["imgdata","framedata","textdata","iobdata"],"auto":False}
                                             ,"preprocess": {"x_size": {"type":"int","option":32,"auto":False}
                                                            , "y_size": {"type":"int","option":32,"auto":False}
                                                            , "channel":{"type":"int","option":3,"auto":False}
                                                            , "filesize": {"type":"int","option":1000000,"auto":False}
                                                            , "yolo": {"type":"sel","option":["N","Y"],"auto":False}}
                                        },
                         "eval_data" :{
                                             "type":{"type":"sel","option":["imgdata","framedata","textdata","iobdata"],"auto":False}
                                                , "preprocess": {"x_size": {"type": "int", "option": 32, "auto": False}
                                                    , "y_size": {"type": "int", "option": 32, "auto": False}
                                                    , "channel": {"type": "int", "option": 3, "auto": False}
                                                    , "filesize": {"type": "int", "option": 1000000, "auto": False}
                                                    , "yolo": {"type": "sel", "option": ["N", "Y"], "auto": False}}
                                    }

                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))
##############################################################################################################################
# resnet
##############################################################################################################################
resp = requests.post('http://' + url + '/api/v1/type/automl/state/rule/graph_id/resnet/',
                     json=
                     {
                         "netconf_node" :{
                                             "param": {"traincnt": {"type":"int","option":2,"auto":False}
                                                      ,"epoch": {"type":"int","option":5,"auto":False}
                                                      ,"batch_size": {"type":"int","option":None,"auto":[10,1000,10]}
                                                      ,"predictcnt": {"type":"int","option":5,"auto":False}
                                                      ,"predictlog": {"type":"sel","option":["N","Y"],"auto":False}
                                                      ,"augmentation": {"type":"sel","option":["N","Y"],"auto":False}
                                             }
                                             ,"config": {"num_classes": {"type":"int","option":1,"auto":False}
                                                        ,"learnrate": {"type":"int","option":None,"auto":[0.0001,0.1,0.001]}
                                                        , "layeroutputs": {"type":"int","option":18,"auto":False}
                                                        ,"eval_type":{"type":"sel","option":["category"],"auto":False}
                                                        ,"optimizer":{"type":"sel","option":["adam","rmsp"],"auto":False}
                                                         }
                                             ,"labels":{"type":"str","option":[],"auto":False}
                                        }
                        ,  "netconf_data"    :{
                                             "type":{"type":"sel","option":["imgdata","framedata","textdata","iobdata"],"auto":False}
                                             ,"preprocess": {"x_size": {"type":"int","option":32,"auto":False}
                                                            , "y_size": {"type":"int","option":32,"auto":False}
                                                            , "channel":{"type":"int","option":3,"auto":False}
                                                            , "filesize": {"type":"int","option":1000000,"auto":False}
                                                            , "yolo": {"type":"sel","option":["N","Y"],"auto":False}}
                                           }
                        , "eval_data" :{
                                                 "type":{"type":"sel","option":["imgdata","framedata","textdata","iobdata"],"auto":False}
                                                 ,"preprocess": {"x_size": {"type":"int","option":32,"auto":False}
                                                            , "y_size": {"type":"int","option":32,"auto":False}
                                                            , "channel":{"type":"int","option":3,"auto":False}
                                                            , "filesize": {"type":"int","option":1000000,"auto":False}
                                                            , "yolo": {"type":"sel","option":["N","Y"],"auto":False}
                                    }
                         }
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))
##############################################################################################################################
# wdnn
##############################################################################################################################
resp = requests.post('http://' + url + '/api/v1/type/automl/state/rule/graph_id/wdnn/',
                     json=
                     {
                        "data_node" :
                                     {
                                             "type":{"type":"sel","option":["csv"],"auto":False}
                                             ,"source_server":{"type":"sel","option":["local"],"auto":False}
                                             ,"source_sql":{"type":"sel","option":["all"],"auto":False}
                                             ,"source_path":{"type":"str","option":None,"auto":False}
                                             ,"multi_node_flag": {"type" : "sel", "option" : ["True","False"],"auto":False}
                                             ,"drop_duplicate": {"type" : "sel", "option" : ["False", "True"],"auto":False}
                                             ,"preprocess":{"type":"sel","option":["null","maxabs_scale",'scale','minmax_scale','robust_scale','normalize','maxabs_scale'],"auto":False}
                                             ,"store_path":{"type":"str","option":None,"auto":False}

                                     }
                         ,"dataconf_node":
                                     {
                                                        "label": {"type":"str","option":"SUCCESSFUL_BID_PRICE","auto":False}
                                                    ,"Transformations":{"type":"str","option":{},"auto":False}
                                                    ,"cross_cell":{"type":"str","option":{},"auto":False}
                                                    ,"cell_feature":{"type":"str","option":{},"auto":False}
                                                    ,"extend_cell_feature" :{"type":"str","option":{},"auto":False}
                                                    ,"label_values" : {"type":"str","option":[],"auto":False}
                                                    ,"label_type" : {"type":"sel","option":["CATEGORYCAL", "CONTINUOUS"],"auto":False}
                                     }
                         ,"netconf_node" :
                                     {
                                                    "model_path": {"type":"str","option":None,"auto":False}
                                                    ,"hidden_layers": {"type": "int", "option": [100,100], "auto": False}
                                                    ,"activation_function": {"type":"sel","option":["relu"],"auto":False}
                                                    ,"batch_size" : {"type":"int","option":1000,"auto":False}
                                                    ,"epoch" : {"type":"int","option":None,"auto":[1,10,1]}
                                                    ,"model_type" : {"type":"sel","option":["regression","category"],"auto":False}
                                                    ,"train" : {"type" : "sel", "option" : ["True","False"],"auto":False}
                                     }
                         ,"evaldata" :
                                    {
                                        "type": {"type": "sel", "option": ["csv"], "auto": False}
                                        , "source_server": {"type": "sel", "option": ["local"], "auto": False}
                                        , "source_sql": {"type": "sel", "option": ["all"], "auto": False}
                                        , "source_path": {"type": "str", "option": None, "auto": False}
                                        , "multi_node_flag": {"type": "sel", "option": ["False"], "auto": False}
                                        , "preprocess": {"type": "sel",
                                                         "option": ["null","maxabs_scale", 'scale', 'minmax_scale',
                                                                    'robust_scale', 'normalize', 'maxabs_scale'],
                                                         "auto": False}
                                        , "store_path": {"type": "str", "option": None, "auto": False}

                                    }
                         ,"eval_node" :
                                    {
                                        "type": {"type":"sel","option":["regression","category"],"auto":False}
                                    }
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

##############################################################################################################################
# wdnn keras
##############################################################################################################################
resp = requests.post('http://' + url + '/api/v1/type/automl/state/rule/graph_id/wdnn_keras/',
                     json=
                     {
                         "data_node":
                             {
                                 "source":
                                     {
                                         "type": {"type": "sel", "option": ["csv"], "auto": False}
                                         , "source_server": {"type": "sel", "option": ["local"], "auto": False}
                                         , "source_sql": {"type": "sel", "option": ["all"], "auto": False}
                                         , "source_path": {"type": "str", "option": None, "auto": False}
                                         ,
                                         "multi_node_flag": {"type": "sel", "option": ["True", "False"], "auto": False}
                                         , "drop_duplicate": {"type": "sel", "option": ["True", "False"], "auto": False}
                                     }
                                 , "pre":
                                 {
                                     "source_sql": {"type": "sel",
                                                    "option": ["maxabs_scale", 'scale', 'minmax_scale', 'robust_scale',
                                                               'normalize', 'maxabs_scale'], "auto": False}
                                 }
                                 , "store":
                                 {
                                     "store_path": {"type": "str", "option": None, "auto": False}
                                 }
                             }
                         , "dataconf_node":
                         {
                             "label": {"type": "str", "option": "SUCCESSFUL_BID_PRICE", "auto": False}
                             , "Transformations": {"type": "str", "option": {}, "auto": False}
                             , "cross_cell": {"type": "str", "option": {}, "auto": False}
                             , "cell_feature": {"type": "str", "option": {}, "auto": False}
                             , "extend_cell_feature": {"type": "str", "option": {}, "auto": False}
                             , "label_values": {"type": "str", "option": [], "auto": False}
                             , "label_type": {"type": "str", "option": "CONTINUOUS", "auto": False}
                         }
                         , "netconf_node":
                         {
                             "model_path": {"type": "str", "option": None, "auto": False}
                             , "hidden_layers": {"type": "int", "option": [100], "auto": False}
                             , "activation_function": {"type": "sel", "option": ["relu"], "auto": False}
                             , "batch_size": {"type": "int", "option": None, "auto": [100, 100000, 100]}
                             , "epoch": {"type": "int", "option": None, "auto": [10, 500, 10]}
                             , "model_type": {"type": "sel", "option": ["regression"], "auto": False}
                             , "train": {"type": "sel", "option": ["True", "False"], "auto": False}
                         }
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))
##############################################################################################################################
# word2vec
##############################################################################################################################
resp = requests.post('http://' + url + '/api/v1/type/automl/state/rule/graph_id/word2vec/',
                     json=
                     {
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))
##############################################################################################################################
# word2vec_frame
##############################################################################################################################
resp = requests.post('http://' + url + '/api/v1/type/automl/state/rule/graph_id/word2vec_frame/',
                     json=
                     {
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))
##############################################################################################################################
# doc2vec
##############################################################################################################################
resp = requests.post('http://' + url + '/api/v1/type/automl/state/rule/graph_id/doc2vec/',
                     json=
                     {
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))
##############################################################################################################################
# wcnn
##############################################################################################################################
resp = requests.post('http://' + url + '/api/v1/type/automl/state/rule/graph_id/wcnn/',
                     json=
                     {
                         "data_node":
                             {
                                 "source_type": {"type": "sel", "option": ['local'], "auto": False},
                                 "type": {"type": "sel", "option": ['csv'], "auto": False},
                                 "source_server": {"type": "sel", "option": ["local"], "auto": False},
                                 "source_sql": {"type": "sel", "option": ["all"], "auto": False},
                                 "preprocess": {"type": "sel", "option": ["none"], "auto": False},
                             },
                         "test_data_node":
                             {
                                 "source_type": {"type": "sel", "option": ['local'], "auto": False},
                                 "type": {"type": "sel", "option": ['csv'], "auto": False},
                                 "source_server": {"type": "sel", "option": ["local"], "auto": False},
                                 "source_sql": {"type": "sel", "option": ["all"], "auto": False},
                                 "preprocess": {"type": "sel", "option": ["none"], "auto": False},
                             },
                         "netconf_node":
                             {
                                 "param": {"epoch": {"type": "int", "option": None, "auto": [1, 10, 1]}
                                     , "traincnt": {"type": "int", "option": None, "auto": [1, 10, 2]}
                                     , "batch_size": {"type": "int", "option": None, "auto": [5, 100, 10]}
                                     , "predictcnt": {"type": "int", "option": None, "auto": [5, 100, 10]}
                                           }
                                 , "config": {"num_classes": {"type": "int", "option": 15, "auto": False}
                                 , "learnrate": {"type": "int", "option": None, "auto": [0.0001, 0.1, 0.001]}
                                 , "eval_type": {"type": "sel", "option": ["category"], "auto": False}
                                 , "optimizer": {"type": "sel", "option": ["AdamOptimizer"], "auto": False}
                                              }
                                 , "layers": {"active": {"type": "sel", "option": ["relu"], "auto": False},
                                              "cnnfilter": {"type": "int", "option": None, "auto": [[1,10,1],[1,3,1]]},
                                              "droprate":  {"type":"int","option":None,"auto":[0.0,1.0,0.1]}
                                              }
                                 , "out": {
                                 "active": {"type": "sel", "option": ["softmax"], "auto": False},
                                 "padding": {"type": "sel", "option": ["SAME"], "auto": False}
                             }
                                 , "labels": {"type": "str", "option": [], "auto": False}
                             },
                         "pre_feed_test":
                             {
                                 "encode_column": {"type": "str", "option": 'encode', "auto": False},
                                 "decode_column": {"type": "str", "option": 'decode', "auto": False},
                                 "channel": {"type": "sel", "option": [1,2,3], "auto": False},
                                 "encode_len": {"type": "int", "option": 10, "auto": False},
                                 "preprocess": {"type": "sel", "option": ['none','mecab'], "auto": False},
                                 "vocab_size": {"type": "int", "option": 100, "auto": False},
                                 "char_encode": {"type": "sel", "option": ['True','False'], "auto": [0, 1, 1]},
                                 "char_max_len": {"type": "int", "option": 5, "auto": False},
                                 "lable_size": {"type": "int", "option": 15, "auto": False},
                                 "embed_type": {"type": "sel", "option": ["onehot"], "auto": False},
                             },
                         "pre_feed_train":
                             {
                                 "encode_column": {"type": "str", "option": 'encode', "auto": False},
                                 "decode_column": {"type": "str", "option": 'decode', "auto": False},
                                 "channel": {"type": "sel", "option": [1,2,3], "auto": False},
                                 "encode_len": {"type": "int", "option": 10, "auto": False},
                                 "preprocess": {"type": "sel", "option": ['none','mecab'], "auto": False},
                                 "vocab_size": {"type": "int", "option": 100, "auto": False},
                                 "char_encode": {"type": "sel", "option": ['True','False'], "auto": [0, 1, 1]},
                                 "char_max_len": {"type": "int", "option": 5, "auto": False},
                                 "lable_size": {"type": "int", "option": 15, "auto": False},
                                 "embed_type": {"type": "sel", "option": ["onehot"], "auto": False},
                             },
                         "eval_node":
                             {
                                 "type": {"type": "sel", "option": ["category"], "auto": False}
                             }
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))
##############################################################################################################################
# seq2seq
##############################################################################################################################
resp = requests.post('http://' + url + '/api/v1/type/automl/state/rule/graph_id/seq2seq/',
                     json=
                     {
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))
##############################################################################################################################
# seq2seq_csv
##############################################################################################################################
resp = requests.post('http://' + url + '/api/v1/type/automl/state/rule/graph_id/seq2seq_csv/',
                     json=
                     {
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))
##############################################################################################################################
# autoencoder_img
##############################################################################################################################
resp = requests.post('http://' + url + '/api/v1/type/automl/state/rule/graph_id/autoencoder_img/',
                     json=
                     {
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))
##############################################################################################################################
# autoencoder_csv
##############################################################################################################################
resp = requests.post('http://' + url + '/api/v1/type/automl/state/rule/graph_id/autoencoder_csv/',
                     json=
                     {
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))
##############################################################################################################################
# bilstmcrf_iob
##############################################################################################################################
resp = requests.post('http://' + url + '/api/v1/type/automl/state/rule/graph_id/bilstmcrf_iob/',
                     json=
                     {
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))
##############################################################################################################################
# fasttext_txt
##############################################################################################################################
resp = requests.post('http://' + url + '/api/v1/type/automl/state/rule/graph_id/fasttext_txt/',
                     json=
                     {
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))



##############################################################################################################################
##############################################################################################################################
# Network Description
##############################################################################################################################
##############################################################################################################################
resp = requests.put('http://' + url + '/api/v1/type/automl/state/rule/graph_id/graph_flow_desc/',
json=
{
    "cnn" : "CNN (convolutional neural network)은 딥러닝의 한 종류로 앞의 컨볼루셔널 계층을 통해서 입력 받은 특징(Feature)를 추출하게 되고, 이렇게 추출된 특징을 기반으로 기존의 뉴럴 네트워크를 이용하여 분류를 해내게 된다."
    ,"resnet" : "ResNet Network Description"
    ,"wdnn": "wdnn Network Description"
    ,"wdnn_keras": "wdnn_keras Network Description"
    ,"word2vec": "word2vec Network Description"
    ,"word2vec_frame" : "word2vec_frame Network Description"
    ,"doc2vec" : "doc2vec Network Description"
    ,"wcnn" : "WCNN Network Description"
    ,"seq2seq" : "seq2seq Network Description"
    ,"seq2seq_csv" : "seq2seq_csv Network Description"
    ,"autoencoder_img" : "autoencoder_img Network Description"
    ,"autoencoder_csv" : "autoencoder_csv Network Description"
    ,"bilstmcrf_iob" : "bilstmcrf_iob Network Description"
    ,"fasttext_txt" : "fasttext_txt Network Description"
})
##############################################################################################################################
##############################################################################################################################
# Network Group
# Fram : 1
# Image : 2
# NLP : 3

# Multy Ex) 1, 2
##############################################################################################################################
##############################################################################################################################
resp = requests.put('http://' + url + '/api/v1/type/automl/state/rule/graph_id/graph_flow_group_id/',
json=
{
    "cnn" : "2"
    ,"resnet" : "2"
    ,"wdnn": "1"
    ,"wdnn_keras": "1"
    ,"word2vec" : "3"
    ,"word2vec_frame" : "3"
    ,"doc2vec" :"3"
    ,"wcnn" : "3"
    ,"seq2seq" : "3"
    ,"seq2seq_csv" : "3"
    ,"autoencoder_img" : "2"
    ,"autoencoder_csv" : "3"
    ,"bilstmcrf_iob" : "3"
    ,"fasttext_txt" : "3"
})
##############################################################################################################################
##############################################################################################################################
# Sample file path
##############################################################################################################################
##############################################################################################################################
resp = requests.put('http://' + url + '/api/v1/type/automl/state/rule/graph_id/train_file_path/',
json=
{
    "cnn" : "/samples/cnn_sample.zip"
    ,"resnet" : "/samples/resnet_sample.zip"
    ,"wdnn" : "/samples/wdnn_sample.csv"
    ,"wdnn_keras" : "/samples/wdnn_keras_sample.csv"
    ,"word2vec" : "/samples/word2vec_sample.zip"
    ,"word2vec_frame" : "/samples/word2vec_frame_sample.zip"
    ,"doc2vec" : "/samples/doc2vec_sample.zip"
    ,"wcnn" : "/samples/wcnn_sample.csv"
    ,"seq2seq" : "/samples/seq2seq_sample.csv"
    ,"seq2seq_csv" : "/samples/seq2seq_csv_sample.csv"
    ,"autoencoder_img" : "/samples/autoencoder_imgsample.csv"
    ,"autoencoder_csv" : "/samples/autoencoder_csv_sample.csv"
    ,"bilstmcrf_iob" : "/samples/bilstmcrf_iob_sample.csv"
    ,"fasttext_txt" : "/samples/fasttext_txt_sample.csv"

})
##############################################################################################################################
##############################################################################################################################
# Sample Network Create Type.
##############################################################################################################################
##############################################################################################################################
resp = requests.put('http://' + url + '/api/v1/type/automl/state/rule/graph_id/graph_flow_info_id/',
json=
{
    "cnn" : 1
    ,"resnet" : 1
    ,"wdnn": 2
    ,"wdnn_keras" : 3
    ,"word2vec" : 4
    ,"word2vec_frame" : 5
    ,"doc2vec" : 6
    ,"wcnn" : 7
    ,"seq2seq" : 8
    ,"seq2seq_csv" : 9
    ,"autoencoder_img" : 10
    ,"autoencoder_csv" : 11
    ,"bilstmcrf_iob" : 7
    ,"fasttext_txt" : 7

})





