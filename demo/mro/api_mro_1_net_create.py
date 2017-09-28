import requests
import json, os
from common.utils import *
url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8989")

nn_id = "nn00000001"
biz_cate = "ERP"
biz_sub_cate = "MRO"
nn_title = "MRO Image Classification"
nn_desc = "MRO Image Classification"
nn_wf_ver_info = "MRO Image Classification"
network_type = "resnet"

# CNN Network : Create
# (CNN Network를 생성해 준다. ID가 같은 CNN Network가 있으면 재 생성 하지 않는다.)
resp = requests.post('http://' + url + '/api/v1/type/common/target/nninfo/nnid/'+nn_id+ '/',
                     json={
                         "biz_cate": biz_cate,
                         "biz_sub_cate": biz_sub_cate,
                         "nn_title" : nn_title,
                         "nn_desc": nn_desc,
                         "use_flag" : "Y",
                         "dir": "resnet",
                         "config": "N"
                     })
data = json.loads(resp.json())
print("Insert nn_info evaluation result : {0}".format(data))
# nn_id = data['nn_id']
# CNN Network WorkFlow : Create
# (CNN Network WorkFlow를 생성해 준다. 실행할 때마다 신규 버전을 새로 생성 한다.)<br>
resp = requests.post('http://' + url + '/api/v1/type/common/target/nninfo/nnid/'+nn_id+'/version/',
                     json={
                         "nn_def_list_info_nn_id": "",
                         "nn_wf_ver_info": nn_wf_ver_info,
                         "condition": "1",
                         "active_flag": "Y"
                     })
data = json.loads(resp.json())
print("Insert nn_info Work Flow Create")

# CNN Network WorkFlow Node : Create
# (CNN Network WorkFlow Node를 생성해 준다. 기존 Node가 있으면 재 생성 하지 않는다.)
# insert workflow version node info
wf_ver_id = str(1)
resp = requests.post('http://' + url + '/api/v1/type/wf/target/init/mode/simple/'+nn_id+'/wfver/'+wf_ver_id+'/',
                     json={
                         "type": network_type
                     })
data = json.loads(resp.json())
print("insert workflow version node info evaluation result : {0}".format(data))

resp = requests.post('http://' + url + '/api/v1/type/automl/state/train/nnid/'+nn_id+'/')
data = json.loads(resp.json())



