import requests
import json, os
from common.utils import *

println("S")
url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")

resp = requests.post('http://' + url + '/api/v1/type/wf/state/netconf/detail/cnn/nnid/nn00004/ver/5/node/5/',
                     json={
                         "nn_id": "nn00004",
                         "wf_id": "5"
                     })
data = json.loads(resp.json())
# print("evaluation result : {0}".format(data))


println("E")