import requests
import json, os

url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")


# insert workflow info
resp = requests.post('http://' + url + '/api/v1/type/common/target/nninfo/nn00004/version/',
                     json={
                         "nn_def_list_info_nn_id": "",
                         "nn_wf_ver_info": "test version info",
                         "condition": "1",
                         "active_flag": "N"
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))


# update workflow info
resp = requests.put('http://' + url + '/api/v1/type/common/target/nninfo/nn00004/version/',
                     json={
                         "nn_wf_ver_id": "1",
                         "nn_def_list_info_nn_id": "",
                         "nn_wf_ver_info": "test version info",
                         "condition": "1",
                         "active_flag": "Y"
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# get workflow info
resp = requests.get('http://' + url + '/api/v1/type/common/target/nninfo/nn00004/version/')
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))