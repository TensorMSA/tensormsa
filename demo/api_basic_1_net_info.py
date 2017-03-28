import requests
import json, os

url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")


# delete nn_info
resp = requests.delete('http://' + url + '/api/v1/type/common/target/nninfo/',
                     json=["nn00003"])
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

for idx in range(0, 20) :
    #/etc/postgresql/9.6/main
    #insert nn_info
    resp = requests.post('http://' + url + '/api/v1/type/common/target/nninfo/',
                         json={
                             "nn_id": "nn0000" + str(idx),
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
                         "nn_id": "",
                         "biz_cate": "",
                         "biz_sub_cate": ""
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))


