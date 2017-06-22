import requests
import json, os

url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")

##################################################
# Data Menu
##################################################

# "auto":True,"range":[],"interval":1
# insert menu info
resp = requests.post('http://' + url + '/api/v1/type/automl/state/rule/graph_id/charcnn_csv/',
                     json=
                     {
                         "data_node" :
                         {
                             "format" :
                                 {
                                     "type":{"type":"sel","option":["csv","txt","iob"],"auto":False},
                                     "source_server":{"type":"sel","option":["local"],"auto":False},
                                     "source_sql":{"type":"sel","option":["all"],"auto":False},
                                     "preprocess": {"type":"sel","option":["None","Mecab","Twitter","kkma"],"auto":False},
                                 }
                         },
                         "test_data_node" :
                         {
                             "format" :
                                 {
                                     "type":{"type":"sel","option":["csv","txt","iob"],"auto":False},
                                     "source_server":{"type":"sel","option":["local"],"auto":False},
                                     "source_sql":{"type":"sel","option":["all"],"auto":False},
                                     "preprocess": {"type":"sel","option":["None","Mecab","Twitter","kkma"],"auto":False},
                                 }
                         },
                         "netconf_node" :
                         {
                             "format" :
                                 {
                                     "param": {"epoch": {"type":"int","option":None,"auto":(1,10,1)}
                                              ,"traincnt": {"type":"int","option":None,"auto":(1,0,2)}
                                              ,"batch_size": {"type":"int","option":None,"auto":(5,100,10)}
                                              ,"predictcnt": {"type":"int","option":None,"auto":(5,100,10)}
                                     },
                                     "config": {"num_classes": {"type":"int","option":None,"auto":False}
                                                ,"learnrate": {"type":"int","option":None,"auto":(0.0001,0.1,0.001)}
                                                ,"layeroutputs": {"type":"int","option":None,"auto":(5,100,10)}
                                                ,"eval_type":{"type":"sel","option":["category"],"auto":False}
                                                ,"optimizer":{"type":"sel","option":["AdamOptimizer"],"auto":False}
                                                 }
                                     ,"layers": [
                                                {"active": {"type":"sel","option":["relu",'tanh',"sigmoid","softmax"],"auto":(0,1,1)}
                                                 ,"cnnfilter": {"type":"list","option":[15, 15],"auto":False}
                                                 ,"cnnstride": {"type":"list","option":[1, 1],"auto":False}
                                                 ,"maxpoolmatrix": {"type":"list","option":[2, 2],"auto":False}
                                                 ,"maxpoolstride": {"type":"list","option":[2, 2],"auto":False}
                                                 ,"padding": {"type":"sel","option":["SAME", "NONE"],"auto":(0,1,1)}
                                                 ,"learnrate": {"type": "int", "option": None, "auto": (0.0001, 0.1, 0.001)}
                                                 ,"layercnt":{"type": "int", "option": None, "auto": (1,5,1)}
                                                }
                                               ]
                                     ,"out": {"active": {"type":"sel","option":["relu",'tanh',"sigmoid","softmax"],"auto":(0,1,1)}
                                             ,"node_out": {"type": "int", "option": None, "auto": (500,1000,50)}
                                             ,"padding":  {"type":"sel","option":["SAME", "NONE"],"auto":(0,1,1)}
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
                                     "encode_len": {"type" : "int", "option" : None,"auto":(5,20,2)},
                                     "preprocess":{"type" : "sel", "option" : ["None", "Mecab", "Twitter","kkma"],"auto":False},
                                     "vocab_size":{"type" : "int", "option" : None,"auto":False},
                                     "char_encode":{"type" : "sel", "option" : [True,False],"auto":(0,1,1)},
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
                                     "encode_len": {"type" : "int", "option" : None,"auto":(5,10,1)},
                                     "preprocess":{"type" : "sel", "option" : ["None", "Mecab", "Twitter","kkma"],"auto":False},
                                     "vocab_size":{"type" : "int", "option" : None,"auto":False},
                                     "char_encode":{"type" : "sel", "option" : [True,False],"auto":(0,1,1)},
                                     "char_max_len":{"type" : "int", "option" : None,"auto":(5,10,1)},
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