import requests
import json, os

url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")

##################################################
# Data Menu
##################################################

resp = requests.post('http://' + url + '/api/v1/type/automl/state/rule/graph_id/cnn/',
                     json=
                     {
                        "netconf_node" :{
                                        "format" :{
                                                         "param":{"traincnt": {"type":100,"option":None,"auto":[1,500,1]}
                                                                  ,"epoch": {"type":100,"option":None,"auto":[1,500,1]}
                                                                  ,"batch_size":{"type":200,"option":None,"auto":[100,1000000,100]}
                                                                  ,"predictcnt": {"type":5,"option":None,"auto":False}
                                                                  ,"predlog": {"type":"N","option":None,"auto":False}
                                                         },
                                                         "config": {"num_classes":{"type":1,"option":None,"auto":False},
                                                                    "learnrate": {"type":0.001,"option":None,"auto":[0.0001,0.1,0.001]},
                                                                    "layeroutputs":{"type":32,"option":None,"auto":[5,100,10]},
                                                                    "net_type":"cnn",
                                                                    "eval_type":{"type":"sel","option":["category"],"auto":False},
                                                                    "optimizer":{"type":"sel","option":["AdamOptimizer","RMSPropOptimizer"],"auto":False}
                                                                     }
                                                         ,"layer1": {"active": {"type":"sel","option":["relu"],"auto":False},
                                                                     "cnnfilter": {"type":"list","option":[3, 3],"auto":False},
                                                                     "cnnstride": {"type":"list","option":[1, 1],"auto":False},
                                                                     "maxpoolmatrix": {"type":"list","option":[2, 2],"auto":False},
                                                                     "maxpoolstride": {"type":"list","option":[2, 2],"auto":False},
                                                                     "padding": {"type":"sel","option":["SAME", "NONE"],"auto":False},
                                                                     "droprate": {"type":0.8,"option":None,"auto":[0.0,1.0,0.1]},
                                                                     "layercnt":{"type":4,"option":None,"auto":[1,6,1]}
                                                                    }
                                                         ,"out": {"active": {"type":"sel","option":["softmax","relu",'tanh',"sigmoid"],"auto":False},
                                                                   "node_out": {"type":625,"option":None,"auto":[600,2000,5]},
                                                                   "padding": {"type":"sel","option":["SAME", "NONE"],"auto":False}
                                                                }
                                                         ,"labels":[]
                                                }
                                        },
                         "eval_node"    :{
                                        "format" : {}
                                        },
                         "datasrc"    :{
                                        "format" : {
                                                         "type":{"type":"sel","option":["imgdata","framedata","textdata","iobdata"],"auto":False},
                                                         "preprocess": {"x_size": 32, "y_size": 32, "channel":3, "filesize": 1000000, "yolo": "n"}
                                                    }
                                        },
                         "evaldata" :{
                                        "format" : {
                                                         "type":{"type":"sel","option":["imgdata","framedata","textdata","iobdata"],"auto":False}
                                                         ,"preprocess": {"x_size": 32, "y_size": 32, "channel":3, "filesize": 1000000, "yolo": "n"}
                                                    }
                                    }

                     })

# "auto":True,"range":[],"interval":1
# insert menu info
resp = requests.post('http://' + url + '/api/v1/type/automl/state/rule/graph_id/wcnn/',
                     json=
                     {
                         "data_node" :
                         {
                             "format" :
                                 {
                                     "type":{"type":"sel","option":["framedata","imgdata","textdata","iobdata"],"auto":False},
                                     "source_server":{"type":"sel","option":["local"],"auto":False},
                                     "source_sql":{"type":"sel","option":["all"],"auto":False},
                                     "preprocess": {"type":"sel","option":["None","Mecab","Twitter","kkma"],"auto":False},
                                 }
                         },
                         "test_data_node" :
                         {
                             "format" :
                                 {
                                     "type":{"type":"sel","option":["framedata","imgdata","textdata","iobdata"],"auto":False},
                                     "source_server":{"type":"sel","option":["local"],"auto":False},
                                     "source_sql":{"type":"sel","option":["all"],"auto":False},
                                     "preprocess": {"type":"sel","option":["None","Mecab","Twitter","kkma"],"auto":False},
                                 }
                         },
                         "netconf_node" :
                         {
                             "format" :
                                 {
                                     "param": {"epoch": {"type":"int","option":None,"auto":[1,10,1]}
                                              ,"traincnt": {"type":"int","option":None,"auto":[1,0,2]}
                                              ,"batch_size": {"type":"int","option":None,"auto":[5,100,10]}
                                              ,"predictcnt": {"type":"int","option":None,"auto":[5,100,10]}
                                     }
                                     ,"config": {"num_classes": {"type":"int","option":None,"auto":False}
                                                ,"learnrate": {"type":"int","option":None,"auto":[0.0001,0.1,0.001]}
                                                ,"layeroutputs": {"type":"int","option":None,"auto":[5,100,10]}
                                                ,"eval_type":{"type":"sel","option":["category"],"auto":False}
                                                ,"optimizer":{"type":"sel","option":["AdamOptimizer"],"auto":False}
                                                 }
                                     ,"layers": [{"active": {"type":"sel","option":["relu",'tanh',"sigmoid","softmax"],"auto":[0,1,1]}
                                                 ,"cnnfilter": {"type":"list","option":[15, 15],"auto":False}
                                                 ,"cnnstride": {"type":"list","option":[1, 1],"auto":False}
                                                 ,"maxpoolmatrix": {"type":"list","option":[2, 2],"auto":False}
                                                 ,"maxpoolstride": {"type":"list","option":[2, 2],"auto":False}
                                                 ,"padding": {"type":"sel","option":["SAME", "NONE"],"auto":[0,1,1]}
                                                 ,"learnrate": {"type": "int", "option": None, "auto": [0.0001, 0.1, 0.001]}
                                                 ,"layercnt":{"type": "int", "option": None, "auto": [1,5,1]}
                                                },
                                                 {"active": {"type": "sel",
                                                             "option": ["relu", 'tanh', "sigmoid", "softmax"],
                                                             "auto": [0, 1, 1]}
                                                     , "cnnfilter": {"type": "list", "option": [15, 15], "auto": False}
                                                     , "cnnstride": {"type": "list", "option": [1, 1], "auto": False}
                                                     ,
                                                  "maxpoolmatrix": {"type": "list", "option": [2, 2], "auto": False}
                                                     ,
                                                  "maxpoolstride": {"type": "list", "option": [2, 2], "auto": False}
                                                     , "padding": {"type": "sel", "option": ["SAME", "NONE"],
                                                                   "auto": [0, 1, 1]}
                                                     , "learnrate": {"type": "int", "option": None,
                                                                     "auto": [0.0001, 0.1, 0.001]}
                                                     , "layercnt": {"type": "int", "option": None, "auto": [1, 5, 1]}
                                                  }
                                                 ]
                                     ,"out": {"active": {"type":"sel","option":["relu",'tanh',"sigmoid","softmax"],"auto":[0,1,1]}
                                             ,"node_out": {"type": "int", "option": None, "auto": [500,1000,50]}
                                             ,"padding":  {"type":"sel","option":["SAME", "NONE"],"auto":[0,1,1]}
                                            }
                                     ,"labels":[]
                                 }
                         },
                         "pre_feed_test" :
                         {
                             "format" :
                                 {
                                     "encode_column":{"type":"str","option":None,"auto":False},
                                     "decode_column":{"type": "str", "option" : None,"auto":False},
                                     "channel":{"type" : "sel", "option" : [1,2,3],"auto":False},
                                     "encode_len": {"type" : "int", "option" : None,"auto":[5,20,2]},
                                     "preprocess":{"type" : "sel", "option" : ["None", "Mecab", "Twitter","kkma"],"auto":False},
                                     "vocab_size":{"type" : "int", "option" : None,"auto":False},
                                     "char_encode":{"type" : "sel", "option" : [True,False],"auto":[0,1,1]},
                                     "char_max_len":{"type" : "int", "option" : None,"auto":False},
                                     "lable_size":{"type" : "int", "option" : None,"auto":False},
                                     "embed_type":{"type" : "sel", "option" : ["onehot", "word2vec", "fasttext", "glove"],"auto":False},
                                 }
                         },
                         "pre_feed_train" :
                         {
                             "format" :
                                 {
                                     "encode_column":{"type":"str","option":None,"auto":False},
                                     "decode_column":{"type": "str", "option" : None,"auto":False},
                                     "channel":{"type" : "sel", "option" : [1,2,3],"auto":False},
                                     "encode_len": {"type" : "int", "option" : None,"auto":[5,10,1]},
                                     "preprocess":{"type" : "sel", "option" : ["None", "Mecab", "Twitter","kkma"],"auto":False},
                                     "vocab_size":{"type" : "int", "option" : None,"auto":False},
                                     "char_encode":{"type" : "sel", "option" : [True,False],"auto":[0,1,1]},
                                     "char_max_len":{"type" : "int", "option" : None,"auto":[5,10,1]},
                                     "lable_size":{"type" : "int", "option" : None,"auto":False},
                                     "embed_type":{"type" : "sel", "option" : ["onehot", "word2vec", "fasttext", "glove"],"auto":False},
                                 }
                         },
                         "eval_node" :
                         {
                             "format" :
                                {
                                    "type": {"type" : "sel", "option" : ["Category", "regression", "w2v","seq2seq"],"auto":False}
                                }
                         }
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))


resp = requests.post('http://' + url + '/api/v1/type/automl/state/rule/graph_id/wdnn/',
                     json=
                     {})


resp = requests.post('http://' + url + '/api/v1/type/automl/state/rule/graph_id/resnet/',
                     json=
                     {
                         "netconf_node" :{
                            "format" :
                                 {
                                             "param": {"traincnt": {"type":"int","option":None,"auto":[1,100,2]}
                                                      ,"epoch": {"type":"int","option":None,"auto":[1,10,1]}
                                                      ,"batch_size": {"type":"int","option":None,"auto":[10,1000,10]}
                                                      ,"predictcnt": 5
                                                      ,"predictlog": "N"
                                                      ,"augmentation": "Y"
                                             },
                                             "config": {"num_classes": 1
                                                        ,"learnrate": {"type":"int","option":None,"auto":[0.0001,0.1,0.001]}
                                                        , "layeroutputs": {"type":"int","option":None,"auto":[1,152,10]}
                                                        ,"eval_type":{"type":"sel","option":["category"],"auto":False}
                                                        ,"optimizer":{"type":"sel","option":["adam","rmsp"],"auto":False}
                                                         }
                                             ,"labels":[]
                                        }
                        },
                         "eval_node"    :{ "format" : {}  },
                         "datasrc"    :{
                            "format" : {
                                             "type":{"type":"sel","option":["imgdata","framedata","textdata","iobdata"],"auto":False},
                                             "preprocess": {"x_size": 32, "y_size": 32, "channel":3, "filesize": 1000000, "yolo": "n"}
                                           }
                        },
                         "evaldata" :{ "format" : {
                                                 "type":{"type":"sel","option":["imgdata","framedata","textdata","iobdata"],"auto":False}
                                                 ,"preprocess": {"x_size": 32, "y_size": 32, "channel":3, "filesize": 1000000, "yolo": "n"}
                                             }
                         }
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))



resp = requests.put('http://' + url + '/api/v1/type/automl/state/rule/graph_id/graph_flow_desc/',
                     json=
                     {
                            "cnn" : "CNN Network Description"
                            ,"resnet" : "ResNet Network Description"
                            ,"wcnn" : "WCNN Network Description"
                            ,"wdnn" : "WDNN Network Description"
                     })