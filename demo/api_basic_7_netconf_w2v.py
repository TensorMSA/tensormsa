import requests
import json, os

url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")

nn_id = "nn00002"
wf_ver_id = "1"

# update source_info
# set netconf_node in NN_WF_NODE_INFO
resp = requests.put('http://' + url + '/api/v1/type/wf/state/netconf/detail/w2v/nnid/' + nn_id + '/ver/' + wf_ver_id + '/node/netconf_node/',
                     json={
                        "window_size" : 5,
                        "vector_size" : 100,
                        "batch_size" : 100,
                        "iter" : 5,
                        "min_count" : 0
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))


nn_id = "nn00009"
wf_ver_id = "1"

# update source_info
# set netconf_node in NN_WF_NODE_INFO
resp = requests.put('http://' + url + '/api/v1/type/wf/state/netconf/detail/w2v/nnid/' + nn_id + '/ver/' + wf_ver_id + '/node/netconf_node/',
                     json={
                        "window_size" : 5,
                        "vector_size" : 300,
                        "batch_size" : 100,
                        "iter" : 5,
                        "min_count" : 0
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))