import requests
import json, os
from common.utils import *

println("Start")

# url(r'^api/v1/type/wf/state/data/detail/upload/file/nnid/(?P<nnid>.*)/ver/(?P<ver>.*)/dir/(?P<dir>.*)/',
files = {'files': open('/home/dev/hoyai/test2.csv','rb')}

resp = requests.post('http://' + gUrl + '/api/v1/type/wf/state/data/detail/upload/file/nnid/nn00004/ver/1/dir/scm/',
                     files=files,
                     json={
                         "nn_id": "nn00004",
                         "wf_id": "5",
                         "node_id": "5"
                     })
data = json.dumps(resp.json())
# print("evaluation result : {0}".format(data))


println("End")


