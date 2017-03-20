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
resp = requests.put('http://' + gUrl + '/api/v1/type/wf/state/netconf/detail/renet/nnid/'+nn_id+'/ver/'+wf_ver_id+'/node/netconf_node/',
                     json={
                         "model_path" : "/hoya_model_root/nn00004/12/netconf_node/"
                         ,"batch_size":32
                         ,"nb_classes":2
                         ,"nb_epoch":200
                         ,"data_augmentation":"False"
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
                         "preprocess": {"x_size": 32,
                                        "y_size": 32,
                                        "channel":3},
                         "store_path": "/hoya_str_root/"+nn_id+"/"+wf_ver_id+"/datasrc"
                     })

# Run All Workflow
resp = requests.post('http://' + gUrl + '/api/v1/type/runmanager/state/train/nnid/'+nn_id+'/ver/'+wf_ver_id+'/')
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

println("E")



