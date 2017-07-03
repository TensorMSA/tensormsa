import requests
import json, os
from common.utils import *
url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")

nn_id = "mro0003"
biz_cate = "ERP"
biz_sub_cate = "MRO"
nn_title = "MRO Image Classification"
nn_desc = "MRO Image Classification"
nn_wf_ver_info = "MRO Image Classification"
network_type = "renet"
# network_type = "renet"

# CNN Network : Create
# (CNN Network를 생성해 준다. ID가 같은 CNN Network가 있으면 재 생성 하지 않는다.)
resp = requests.post('http://' + url + '/api/v1/type/common/target/nninfo/nnid/'+nn_id+ '/',
                     json={
                         "biz_cate": biz_cate,
                         "biz_sub_cate": biz_sub_cate,
                         "nn_title" : nn_title,
                         "nn_desc": nn_desc,
                         "use_flag" : "Y",
                         "dir": "purpose?",
                         "config": "N"
                     })
data = json.loads(resp.json())
print("Insert nn_info evaluation result : {0}".format(data))

# CNN Network WorkFlow : Create
# (CNN Network WorkFlow를 생성해 준다. 실행할 때마다 신규 버전을 새로 생성 한다.)<br>
resp = requests.post('http://' + url + '/api/v1/type/common/target/nninfo/nnid/'+nn_id+'/version/',
                     json={
                         "nn_def_list_info_nn_id": "",
                         "nn_wf_ver_info": nn_wf_ver_info,
                         "condition": "1",
                         "active_flag": "N"
                     })
data = json.loads(resp.json())
print("Insert nn_info Work Flow Create")

# CNN Network WorkFlow : Get Active Version
# (여러개의 CNN Network WorkFlow중 Active한 Version을 가져온다.)<br>
# get workflow version info
resp = requests.get('http://' + url + '/api/v1/type/common/target/nninfo/nnid/'+nn_id+'/version/')
data = json.loads(resp.json())

# get Active workflow version
wf_ver_id = 0
max_wf_ver_id = 0
data = sorted(data, key=lambda k: k['fields']['nn_wf_ver_id'])
for config in data:
    # print("Version="+str(config['fields']['nn_wf_ver_id'])+" active="+str(config["fields"]["active_flag"]))
    if config["fields"]["active_flag"] == "Y":
        wf_ver_id = config['fields']['nn_wf_ver_id']
print("Active Version Workflow ID=" + str(wf_ver_id))

# get Max workflow version
for config in data:
    if config["fields"]["nn_wf_ver_id"] > wf_ver_id:
        wf_ver_id = config["fields"]["nn_wf_ver_id"]

# CNN Network WorkFlow : Set Active Version
# (여러개의 CNN Network WorkFlow중 특정 Version을 Active 시킨다. Active한 Version은 한 개만 존재 할 수 있다.)
# update workflow version info
resp = requests.put('http://' + url + '/api/v1/type/common/target/nninfo/nnid/'+nn_id+'/version/',
                     json={
                         "nn_wf_ver_id": wf_ver_id,
                         "nn_def_list_info_nn_id": "",
                         "nn_wf_ver_info": nn_wf_ver_info,
                         "condition": "1",
                         "active_flag": "Y"
                     })
data = json.loads(resp.json())
print("New Active Version Workflow ID="+str(wf_ver_id))

# CNN Network WorkFlow Node : Create
# (CNN Network WorkFlow Node를 생성해 준다. 기존 Node가 있으면 재 생성 하지 않는다.)
# insert workflow version node info
wf_ver_id = str(wf_ver_id)
resp = requests.post('http://' + url + '/api/v1/type/wf/target/init/mode/simple/'+nn_id+'/wfver/'+wf_ver_id+'/',
                     json={
                         "type": network_type
                     })
data = json.loads(resp.json())
print("insert workflow version node info evaluation result : {0}".format(data))





