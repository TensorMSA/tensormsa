import requests
import json, os

url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")

# update source_info
resp = requests.put('http://' + url + '/api/v1/type/wf/state/netconf/detail/w2v/nnid/nn00004/ver/3/node/netconf_node/',
                     json={
                         "model_path" : "test"
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))