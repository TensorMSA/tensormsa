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
                         "config": {"learnrate": 0.001,
                                     "traincnt": 100,
                                     "batch_size":10000,
                                     "num_classes":10,
                                     "predictcnt": 10,
                                     "layeroutputs":32
                                     }
                         ,"layer1": {"type": "cnn",
                                     "active": "relu",
                                     "cnnfilter": [3, 3],
                                     "cnnstride": [1, 1],
                                     "maxpoolmatrix": [2, 2],
                                     "maxpoolstride": [2, 2],
                                     "padding": "SAME",
                                     "droprate": "0.8",
                                     "layercnt":2
                                    }
                         ,"layer2": {"type": "cnn",
                                     "active": "relu",
                                     "cnnfilter": [3, 3],
                                     "cnnstride": [1, 1],
                                     "maxpoolmatrix": [2, 2],
                                     "maxpoolstride": [2, 2],
                                     "padding": "SAME",
                                     "droprate": "0.8",
                                     "layercnt":1
                                    }
                          ,"out": {"active": "softmax",
                                   "node_out": 625,
                                   "padding": "SAME"
                                }
                        })
netconf = json.loads(resp.json())
# print("insert workflow node conf info evaluation result : {0}".format(netconf))

# CNN Network WorkFlow Node :  Eval Config Setup
node = "eval_node"
resp = requests.put('http://' + url + '/api/v1/type/wf/state/netconf/detail/cnn/nnid/'+nn_id+'/ver/'+wf_ver_id+'/node/'+node+'/',json={})
evalconf = json.loads(resp.json())
# print("insert workflow node conf info evaluation result : {0}".format(evalconf))

# CNN Network WorkFlow Node :  Data Config Setup
node = "datasrc"
resp = requests.put('http://' + url + '/api/v1/type/wf/state/imgdata/src/local/form/file/prg/source/nnid/'+nn_id+'/ver/'+wf_ver_id+'/node/'+node+'/',
                     json={
                            "preprocess": {"x_size": 32,
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
                            "preprocess": {"x_size": 32,
                                        "y_size": 32,
                                        "channel":3}
                         ,"labels":[]

                     })
edataconf = json.loads(resp.json())
# print("insert workflow node conf info evaluation result : {0}".format(edataconf))

# CNN Network Training
# (CNN Network Training을 실행한다.)
resp = requests.post('http://' + url + '/api/v1/type/runmanager/state/train/nnid/'+nn_id+'/ver/'+wf_ver_id+'/')
data = json.loads(resp.json())
# print(data)

for train in data:
    if train != None and train != "" and train != {} and train != "status" and train != "result" and train["TrainResult"] != None:
        # print(train)
        for tr in train["TrainResult"]:
            print(tr)


println("E")






