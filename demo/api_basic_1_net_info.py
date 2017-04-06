import requests
import json, os

url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")
nn_id = ""
number = 20

for idx in range(0, number) :
    #insert nn_info
    if (idx > 9 and idx < number):
        nn_id = "nn000" + str(idx)
    else:
        nn_id = "nn0000" + str(idx)
    resp = requests.post('http://' + url + '/api/v1/type/common/target/nninfo/nnid/' + nn_id + '/',
                         json={
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
    resp = requests.get('http://' + url + '/api/v1/type/common/target/nninfo/nnid/' + nn_id + '/')
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))


