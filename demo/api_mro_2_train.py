import requests
import json, os
from common.utils import *

# [TEST - Celery]
# apt-get install rabbitmq-server
# service rabbitmq-server start
# rabbitmqctl add_user tensormsa tensormsa
# rabbitmqctl set_user_tags tensormsa administrator
# rabbitmqctl set_permissions -p / tensormsa '.*' '.*' '.*'
# celery -A hoyai worker -l info
# ./manage.py runserver [HOST]:8000

println("S")

nn_id = "nn00004"

# get workflow version info
resp = requests.get('http://' + gUrl + '/api/v1/type/common/target/nninfo/'+nn_id+'/version/')
data = json.loads(resp.json())

wf_ver_id = 0
for i in data:
    if i["pk"] > wf_ver_id:
        wf_ver_id = i["pk"]

wf_ver_id = str(wf_ver_id)

# get workflow version info

node_id = nn_id+"_"+wf_ver_id+"_netconf_node"

# update workflow node conf info
resp = requests.put('http://' + gUrl + '/api/v1/type/wf/state/netconf/detail/cnn/nnid/'+nn_id+'/ver/'+wf_ver_id+'/node/netconf_node/',
                     json={
                         "key" : {"node_id": node_id,
                                  "nn_id": nn_id,
                                  "wf_ver_id": wf_ver_id,
                                  "modelname": "model"
                                  }
                         ,"config": {"learnrate": 0.001,
                                 "traincnt": 1,
                                 "batch_size":1000,
                                 "num_classes":5,
                                 "predictcnt": 4
                                 }
                         ,"layer1": {
                                 "type": "cnn",
                                 "active": "relu",
                                 "cnnfilter": [3, 3],
                                 "cnnstride": [1, 1],
                                 "maxpoolmatrix": [2, 2],
                                 "maxpoolstride": [2, 2],
                                 "node_in": 1,
                                 "node_out": 32,
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
                                 "maxpoolstride": [2, 2],
                                 "node_in": 32,
                                 "node_out": 64,
                                 "regualizer": "",
                                 "padding": "SAME",
                                 "droprate": ""
                                }
                         # ,"layer3": {
                         #         "type": "cnn",
                         #         "active": "relu",
                         #         "cnnfilter": [3, 3],
                         #         "cnnstride": [1, 1],
                         #         "maxpoolmatrix": [2, 2],
                         #         "maxpoolstride": [2, 2],
                         #         "node_in": 64,
                         #         "node_out": 128,
                         #         "regualizer": "",
                         #         "padding": "SAME",
                         #         "droprate": "0.1"
                         #        }
                          ,"out": {
                                 "active": "softmax",
                                 "cnnfilter": "",
                                 "cnnstride": "",
                                 "maxpoolmatrix": "",
                                 "maxpoolstride": "",
                                 "node_in": 128,
                                 "node_out": 1024,
                                 "regualizer": "",
                                 "padding": "SAME",
                                 "droprate": ""
                                }
                        })
data = json.loads(resp.json())
# print("insert workflow node conf info evaluation result : {0}".format(data))

node_id = nn_id+"_"+wf_ver_id+"_datasrc"

resp = requests.put('http://' + gUrl + '/api/v1/type/wf/state/imgdata/src/local/form/file/prg/source/nnid/'+nn_id+'/ver/'+wf_ver_id+'/node/datasrc/',
                     json={
                         "node_id": node_id,
                         "type": "local image",
                         "labels":[],
                         "source_path": "/hoya_src_root/"+nn_id+"/"+wf_ver_id+"/datasrc",
                         "preprocess": {"x_size": 100,
                                        "y_size": 100,
                                        "channel":3},
                         "store_path": "/hoya_str_root/"+nn_id+"/"+wf_ver_id+"/datasrc"
                     })

# Run All Workflow
resp = requests.post('http://' + gUrl + '/api/v1/type/runmanager/state/train/nnid/'+nn_id+'/ver/'+wf_ver_id+'/')
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

println("E")



