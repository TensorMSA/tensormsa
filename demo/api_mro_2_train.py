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
url = gUrl
nn_id = "nn00004"

# get workflow version info
resp = requests.get('http://' + url + '/api/v1/type/common/target/nninfo/'+nn_id+'/version/')
data = json.loads(resp.json())

wf_ver_id = 0
for i in data:
    if i["pk"] > wf_ver_id:
        wf_ver_id = i["pk"]

wf_ver_id = str(wf_ver_id)

# CNN Network WorkFlow Node : Network Config Setup
# (CNN Network WorkFlow Node의 Network Config를 Setup 해준다.)
node = "netconf_node"
resp = requests.put('http://' + url + '/api/v1/type/wf/state/netconf/detail/cnn/nnid/'+nn_id+'/ver/'+wf_ver_id+'/node/'+node+'/',
                     json={
                         "key" : {"node": node,
                                  "nn_id": nn_id,
                                  "wf_ver_id": wf_ver_id
                                  }
                         ,"config": {"learnrate": 0.001,
                                 "traincnt": 20,
                                 "batch_size":10000,
                                 "num_classes":5,
                                 "predictcnt": 5
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
                                 "droprate": "0.1"
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
                                 "droprate": "0.1"
                                }
                         ,"layer3": {
                                 "type": "cnn",
                                 "active": "relu",
                                 "cnnfilter": [3, 3],
                                 "cnnstride": [1, 1],
                                 "maxpoolmatrix": [2, 2],
                                 "maxpoolstride": [2, 2],
                                 "node_in": 64,
                                 "node_out": 128,
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
                                 "node_in": 128,
                                 "node_out": 625,
                                 "regualizer": "",
                                 "padding": "SAME",
                                 "droprate": ""
                                }
                        })
netconf = json.loads(resp.json())
# print("insert workflow node conf info evaluation result : {0}".format(netconf))

# CNN Network WorkFlow Node :  Eval Config Setup
node = "eval_node"
resp = requests.put('http://' + url + '/api/v1/type/wf/state/netconf/detail/cnn/nnid/'+nn_id+'/ver/'+wf_ver_id+'/node/'+node+'/',
                    json={
                      "key" : {"node": node,
                                  "nn_id": nn_id,
                                  "wf_ver_id": wf_ver_id
                                  }
                    })
evalconf = json.loads(resp.json())
# print("insert workflow node conf info evaluation result : {0}".format(evalconf))

# CNN Network WorkFlow Node :  Data Config Setup
node = "datasrc"
resp = requests.put('http://' + url + '/api/v1/type/wf/state/imgdata/src/local/form/file/prg/source/nnid/'+nn_id+'/ver/'+wf_ver_id+'/node/'+node+'/',
                     json={
                            "key" : {"node": node,
                                  "nn_id": nn_id,
                                  "wf_ver_id": wf_ver_id
                                  }
                         ,"preprocess": {"x_size": 32,
                                        "y_size": 32,
                                        "channel":3}
                         ,"labels":[]

                     })
dataconf = json.loads(resp.json())
# print("insert workflow node conf info evaluation result : {0}".format(dataconf))

# CNN Network WorkFlow Node :  Eval Data Config Setup
# (CNN Network WorkFlow Node의 Data Config를 Setup 해준다.)
node = 'evaldata'
resp = requests.put('http://' + url + '/api/v1/type/wf/state/imgdata/src/local/form/file/prg/source/nnid/'+nn_id+'/ver/'+wf_ver_id+'/node/'+node+'/',
                     json={
                            "key" : {"node": node,
                                  "nn_id": nn_id,
                                  "wf_ver_id": wf_ver_id
                                  }
                         ,"preprocess": {"x_size": 32,
                                        "y_size": 32,
                                        "channel":3}
                         ,"labels":[]

                     })
edataconf = json.loads(resp.json())
# print("insert workflow node conf info evaluation result : {0}".format(edataconf))


# # Sample Data Insert
# # (CNN Network Train을 할 수 있게 Sample Data를 특정 장소에 Copy 해준다..)
# import shutil
# sample_path = '/home/dev/hoyai/demo/data/sample_cnn_img.zip'
# source_path = dataconf["source_path"]
# esource_path = edataconf["source_path"]
#
# shutil.copy(sample_path, source_path)
# shutil.copy(sample_path, esource_path)
# print(source_path)
# print(esource_path)

# CNN Network Training
# (CNN Network Training을 실행한다.)
resp = requests.post('http://' + url + '/api/v1/type/runmanager/state/train/nnid/'+nn_id+'/ver/'+wf_ver_id+'/')
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))



println("E")



