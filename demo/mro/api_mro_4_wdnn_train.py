import os, json
import requests

url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")
nnid = "nn00000005"
wfver = "1"

########################################################################################################################
# Net conf
resp = requests.post('http://' + url + '/api/v1/type/wf/state/netconf/detail/wdnn/nnid/'+nnid+'/ver/'+wfver+'/node/netconf_node/',
                    json={
                        "model_path": "test",
                        "hidden_layers": [100,50],
                        "activation_function": "Relu",
                        "batch_size" : 9000,
                        "epoch" : 1,
                        "model_type" : "category",
                        "train":True
                    })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

########################################################################################################################
# Data Conf
resp = requests.put('http://' + url + '/api/v1/type/wf/state/dataconf/detail/frame/nnid/'+nnid+'/ver/'+wfver+'/node/dataconf_node/',
                     json={"label": "Survived"
                            , "Transformations":{}
                            , "cross_cell":{}
                            , "cell_feature":{}
                            , "extend_cell_feature" :{}
                           ,"label_values" : []
                           ,"label_type" : "CATEGORICAL"
                           })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

########################################################################################################################
# Data Node
resp = requests.put('http://' + url + '/api/v1/type/wf/state/framedata/src/local/form/raw/prg/source/nnid/'+nnid+'/ver/'+wfver+'/node/data_node/',
                     json={
                         "type": "csv",
                         "source_server": "local",
                         "source_sql": "all",
                         "source_path": "test",
                         "multi_node_flag": True
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))
#
#update preprocess
resp = requests.put('http://' + url + '/api/v1/type/wf/state/framedata/src/local/form/raw/prg/pre/nnid/'+nnid+'/ver/'+wfver+'/node/data_node/',
                      json={
                          "preprocess":  "null",
                      })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# update store_path
resp = requests.put('http://' + url + '/api/v1/type/wf/state/framedata/src/local/form/raw/prg/store/nnid/'+nnid+'/ver/'+wfver+'/node/data_node/',
                      json={
                          "store_path": "test"
                      })
########################################################################################################################
# Eval data
resp = requests.put('http://' + url + '/api/v1/type/wf/state/framedata/src/local/form/raw/prg/source/nnid/'+nnid+'/ver/'+wfver+'/node/evaldata/',
                     json={
                         "type": "csv",
                         "source_server": "local",
                         "source_sql": "all",
                         "source_path": "test",
                         "multi_node_flag": False
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))
#
#update preprocess
resp = requests.put('http://' + url + '/api/v1/type/wf/state/framedata/src/local/form/raw/prg/pre/nnid/'+nnid+'/ver/'+wfver+'/node/evaldata/',
                      json={
                          "preprocess":  "null",
                      })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))
#
 # update store_path
resp = requests.put('http://' + url + '/api/v1/type/wf/state/framedata/src/local/form/raw/prg/store/nnid/'+nnid+'/ver/'+wfver+'/node/evaldata/',
                      json={
                          "store_path": "test"
                      })



########################################################################################################################
# CNN Network Training
# (CNN Network Training을 실행한다 .)
resp = requests.post('http://' + url + '/api/v1/type/runmanager/state/train/nnid/'+nnid+'/ver/'+wfver+'/')
data = json.loads(resp.json())
print(data)