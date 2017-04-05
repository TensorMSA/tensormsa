import requests
import json, os
from common.utils import *

println("S")

url = gUrl
nn_id = "nn00004"
node_sub_menu = "data_image"

# get workflow version info
resp = requests.get('http://' + url + '/api/v1/type/common/target/nninfo/'+nn_id+'/version/')
data = json.loads(resp.json())

wf_ver_id = 0
for i in data:
    if i["pk"] > wf_ver_id:
        wf_ver_id = i["pk"]

wf_ver_id = str(wf_ver_id)

# get workflow node list info (train, eval)
resp = requests.get('http://' + url + '/api/v1/type/wf/state/data/detail/upload/file/nnid/'+nn_id+'/ver/'+wf_ver_id+'/dir/'+node_sub_menu+'/')
datalist = json.loads(resp.json())

print("get file node list")
for node in datalist:
    print(datalist[node])

print("")
print("create file node list")
for node in datalist:
    typepath = datalist[node]["nn_wf_node_name"]

    files = {'file1': open('/home/dev/hoyai/demo/data/cat_vs_dog.zip','rb'),
             'file2': open('/home/dev/hoyai/demo/data/sample_cnn_img.zip','rb')}

    resp = requests.post('http://' + url + '/api/v1/type/wf/state/data/detail/upload/file/nnid/'+nn_id+'/ver/'+wf_ver_id+'/dir/'+typepath+'/',
                         files=files)
    data = json.loads(resp.json())
    print(data)

println("E")


