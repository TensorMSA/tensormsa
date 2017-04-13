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

println("S")
url = gUrl
nn_id = "nn00004"

# get workflow version
resp = requests.get('http://' + url + '/api/v1/type/common/target/nninfo/nnid/'+nn_id+'/version/')
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
                         "param":{"epoch":2
                                  ,"traincnt": 20
                                  ,"batch_size":10000
                                  ,"predictcnt": 10
                         },
                         "config": {"num_classes":10,
                                    "learnrate": 0.001,
                                     "layeroutputs":32,
                                     "type":"category"
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
                         ,"labels":[]
                        })
netconf = json.loads(resp.json())
# print("insert workflow node conf info evaluation result : {0}".format(netconf))

# CNN Network WorkFlow Node :  Data Config Setup
node = "datasrc"
resp = requests.put('http://' + url + '/api/v1/type/wf/state/imgdata/src/local/form/file/prg/source/nnid/'+nn_id+'/ver/'+wf_ver_id+'/node/'+node+'/',
                     json={
                            "preprocess": {"x_size": 32,
                                           "y_size": 32,
                                           "channel":3,
                                           "filesize": 1000000}
                     })
dataconf = json.loads(resp.json())
# print("insert workflow node conf info evaluation result : {0}".format(dataconf))

# CNN Network WorkFlow Node :  Eval Config Setup
node = "eval_node"
resp = requests.put('http://' + url + '/api/v1/type/wf/state/netconf/detail/cnn/nnid/'+nn_id+'/ver/'+wf_ver_id+'/node/'+node+'/',json={})
evalconf = json.loads(resp.json())

# CNN Network WorkFlow Node :  Eval Data Config Setup
# (CNN Network WorkFlow Node의 Data Config를 Setup 해준다.)
node = 'evaldata'
resp = requests.put('http://' + url + '/api/v1/type/wf/state/imgdata/src/local/form/file/prg/source/nnid/'+nn_id+'/ver/'+wf_ver_id+'/node/'+node+'/',json={
                            "preprocess": {"x_size": 32,
                                           "y_size": 32,
                                           "channel":3,
                                           "filesize": 1000000}
                     })
edataconf = json.loads(resp.json())

# CNN Network Training
# (CNN Network Training을 실행한다 .)
resp = requests.post('http://' + url + '/api/v1/type/runmanager/state/train/nnid/'+nn_id+'/ver/'+wf_ver_id+'/')
data = json.loads(resp.json())
# print(data)

def spaceprint(val, cnt):
    leng = len(str(val))
    cnt = cnt - leng
    restr = ""
    for i in range(cnt):
        restr += " "
    restr = restr+str(val)
    return restr

for train in data:
    if train != None and train != "" and train != {} and train != "status" and train != "result":
        try:
            for tr in train["TrainResult"]:
                print(tr)
        except:
            maxcnt = 0
            line = ""
            for label in train["labels"]:
                if maxcnt<len(label):
                    maxcnt = len(label)

            for i in range(len(train["labels"])):
                for j in range(maxcnt+4):
                    line += "="

            label_sub = []
            for label in train["labels"]:
                label = spaceprint(label,maxcnt)
                label_sub.append(label)

            space = ""
            for s in range(maxcnt):
                space +=" "

            print(space, label_sub)
            print(space, line)
            for i in range(len(train["labels"])):
                predict_sub = []
                for j in range(len(train["predicts"][i])):
                    pred = spaceprint(train["predicts"][i][j],maxcnt)

                    predict_sub.append(pred)

                print(spaceprint(train["labels"][i],maxcnt), predict_sub)

println("E")






