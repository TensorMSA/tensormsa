import requests
import json, os
from common.utils import *
url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8989")

nn_id = "nn00000030"
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