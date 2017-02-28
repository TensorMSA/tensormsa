import requests
import json, os
from common.utils import *

println("S")

nn_id = "nn00004"
wf_ver_id = "5"
node_id = "5"

resp = requests.put('http://' + gUrl + '/api/v1/type/wf/state/netconf/detail/cnn/nnid/'+nn_id+'/ver/'+wf_ver_id+'/node/'+node_id+'/',
                     json={
                         "key" : {"nn_id": nn_id,
                                 "wf_ver_id": wf_ver_id,
                                 "node_id": node_id
                                  }
                         ,"config": {"matrix": [4, 5],
                                 "learnrate": 0.01,
                                 "epoch": 2,
                                 "x_shape":[0,0],
                                 "y_shape":[0,0]
                                 }
                         ,"layer": {
                                 "type": "cnn",
                                 "active": "relu",
                                 "cnnfilter": [2, 2],
                                 "cnnstride": [1, 1],
                                 "maxpoolmatrix": [2, 2],
                                 "maxpoolstride": [1, 1],
                                 "node_in_out": [1, 32],
                                 "regualizer": "",
                                 "padding": "SAME",
                                 "droprate": ""
                                }
                         ,"drop": {
                                 "active": "tanh",
                                 "cnnfilter": [2, 2],
                                 "cnnstride": [1, 1],
                                 "maxpoolmatrix": [2, 2],
                                 "maxpoolstride": [1, 1],
                                 "node_in_out": [32, 64],
                                 "regualizer": "",
                                 "padding": "SAME",
                                 "droprate": "0.1"
                                }
                          ,"out": {
                                 "active": "softmax",
                                 "cnnfilter": "",
                                 "cnnstride": "",
                                 "maxpoolmatrix": "",
                                 "maxpoolstride": "",
                                 "node_in_out": "",
                                 "regualizer": "",
                                 "padding": "SAME",
                                 "droprate": ""
                                }
                        })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# search nn_info
resp = requests.get('http://' + gUrl + '/api/v1/type/wf/state/netconf/detail/cnn/nnid/'+nn_id+'/ver/'+wf_ver_id+'/node/'+node_id+'/',
                    json={
                        "key": {"nn_id": nn_id,
                                "wf_ver_id": wf_ver_id,
                                "node_id": node_id
                                }
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

println("E")