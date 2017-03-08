import requests
import json, os
from common.utils import *

println("S")

nn_id = "nn00004"
biz_cate = "ERP"
biz_sub_cate = "MRO"
nn_title = "MRO Image Classification"
nn_desc = "MRO Image Classification"
nn_wf_ver_info = "MRO Image Classification"


#insert nn_info
resp = requests.post('http://' + gUrl + '/api/v1/type/common/target/nninfo/',
                     json={
                         "nn_id": nn_id,
                         "biz_cate": biz_cate,
                         "biz_sub_cate": biz_sub_cate,
                         "nn_title" : nn_title,
                         "nn_desc": nn_desc,
                         "use_flag" : "Y",
                         "dir": "purpose?",
                         "config": "N"
                     })
data = json.loads(resp.json())
print("insert nn_info evaluation result : {0}".format(data))

# insert workflow version info
resp = requests.post('http://' + gUrl + '/api/v1/type/common/target/nninfo/'+nn_id+'/version/',
                     json={
                         "nn_def_list_info_nn_id": "",
                         "nn_wf_ver_info": nn_wf_ver_info,
                         "condition": "1",
                         "active_flag": "N"
                     })
data = json.loads(resp.json())

# get workflow version info
resp = requests.get('http://' + gUrl + '/api/v1/type/common/target/nninfo/'+nn_id+'/version/')
data = json.loads(resp.json())

wf_ver_id = 0
for i in data:
    if i["pk"] > wf_ver_id:
        wf_ver_id = i["pk"]

wf_ver_id = str(wf_ver_id)

# update workflow version info
resp = requests.put('http://' + gUrl + '/api/v1/type/common/target/nninfo/'+nn_id+'/version/',
                     json={
                         "nn_wf_ver_id": wf_ver_id,
                         "nn_def_list_info_nn_id": "",
                         "nn_wf_ver_info": nn_wf_ver_info,
                         "condition": "1",
                         "active_flag": "Y"
                     })
data = json.loads(resp.json())
print("insert workflow version info evaluation result : {0}".format(data))

# insert workflow version node info
resp = requests.post('http://' + gUrl + '/api/v1/type/wf/target/init/mode/simple/'+nn_id+'/wfver/'+wf_ver_id+'/',
                     json={
                         "type": "image"
                     })
data = json.loads(resp.json())
print("insert workflow version node info evaluation result : {0}".format(data))

# get workflow version info

node_id = nn_id+"_"+wf_ver_id+"_netconf_node"

# update workflow node conf info
resp = requests.put('http://' + gUrl + '/api/v1/type/wf/state/netconf/detail/cnn/nodeid/'+node_id+'/',
                     json={
                         "key" : {"node_id": node_id
                                  }
                         ,"config": {"learnrate": 0.01,
                                 "epoch": 50
                                 }
                         ,"layer1": {
                                 "type": "cnn",
                                 "active": "relu",
                                 "cnnfilter": [3, 3],
                                 "cnnstride": [1, 1],
                                 "maxpoolmatrix": [2, 2],
                                 "maxpoolstride": [1, 1],
                                 "node_in_out": [1, 32],
                                 "regualizer": "",
                                 "padding": "SAME",
                                 "droprate": ""
                                }
                         ,"layer2": {
                                 "type": "cnn",
                                 "active": "relu",
                                 "cnnfilter": [3, 3],
                                 "cnnstride": [1, 1],
                                 "maxpoolmatrix": [2, 2],
                                 "maxpoolstride": [1, 1],
                                 "node_in_out": [32, 64],
                                 "regualizer": "",
                                 "padding": "SAME",
                                 "droprate": ""

                                }
                         ,"layer3": {
                                 "type": "cnn",
                                 "active": "relu",
                                 "cnnfilter": [3, 3],
                                 "cnnstride": [1, 1],
                                 "maxpoolmatrix": [2, 2],
                                 "maxpoolstride": [1, 1],
                                 "node_in_out": [64, 128],
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
# print("insert workflow node conf info evaluation result : {0}".format(data))

resp = requests.put('http://' + gUrl + '/api/v1/type/wf/state/imgdata/src/local/form/file/prg/source/nnid/'+nn_id+'/ver/'+wf_ver_id+'/node/datasrc/',
                     json={
                         "type": "local image",
                         "source_path": "/home/dev/",
                         "preprocess": {"x_size": 100,
                                        "y_size": 100},
                         "store_path": "/home/dev/"
                     })

println("E")



