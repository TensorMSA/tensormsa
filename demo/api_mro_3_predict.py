import requests
import json, os
from common.utils import *

println("S")
# [TEST - Celery]
# apt-get install rabbitmq-server
# service rabbitmq-server start
# rabbitmqctl add_user tensormsa tensormsa
# rabbitmqctl set_user_tags tensormsa administrator
#rabbitmqctl set_permissions -p / tensormsa '.*' '.*' '.*'
# celery -A hoyai worker -l info
# ./manage.py runserver [HOST]:8000
typeStr = "cnn"
nn_id = "nn00004"

files = {
            'files000001': open('/hoya_src_root/dataTest/car/1car.jpg','rb')
           ,'files000002': open('/hoya_src_root/dataTest/car/2car.jpg','rb')
           ,'files000003': open('/hoya_src_root/dataTest/airplane/1air.jpg','rb')
        }

# get workflow version info
restURL = 'http://' + gUrl + '/api/v1/type/common/target/nninfo/'+nn_id+'/version/'

resp = requests.get(restURL)
data = json.loads(resp.json())

wf_ver_id = 0
for i in data:
    if i["pk"] > wf_ver_id:
        wf_ver_id = i["pk"]

wf_ver_id = str(wf_ver_id)

# get workflow version info

node_id = nn_id+"_"+wf_ver_id+"_netconf_node"

restURL = 'http://' + gUrl + '/api/v1/type/service/state/predict/type/'+typeStr+'/nnid/'+nn_id+'/ver/'+wf_ver_id+'/'

resp = requests.post(restURL,
                     files=files,
                     json={
                         "key" : {"node_id": node_id,
                                  "nn_id": nn_id,
                                  "wf_ver_id": wf_ver_id,
                                  "modelname": "model"
                                  }
                     }
                     )

# data = json.loads(resp.json())
# print("evaluation result : {0}".format(data))

println("E")


