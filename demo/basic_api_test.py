import requests
import json, os
import tensorflow as tf
import logging
from django.conf import settings
from PIL import Image, ImageFilter
import datetime

url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")

#/etc/postgresql/9.6/main
#insert nn_info
resp = requests.post('http://' + url + '/api/v1/type/common/target/nninfo/',
                     json={
                         "nn_id": "nn00003",
                         "biz_cate": "MES",
                         "biz_sub_cate": "M60",
                         "nn_title" : "test",
                         "nn_desc": "test desc",
                         "use_flag" : "Y",
                         "dir": "purpose?",
                         "config": "N"
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))


# search nn_info
resp = requests.get('http://' + url + '/api/v1/type/common/target/nninfo/',
                     json={
                         "nn_id": "nn00003",
                         "biz_cate": "MES",
                         "biz_sub_cate": "M60"
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# delete nn_info
resp = requests.delete('http://' + url + '/api/v1/type/common/target/nninfo/',
                     json=["nn00003"])
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# search nn_info
resp = requests.get('http://' + url + '/api/v1/type/common/target/nninfo/',
                     json={
                         "nn_id": "nn00003",
                         "biz_cate": "MES",
                         "biz_sub_cate": "M60"
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))