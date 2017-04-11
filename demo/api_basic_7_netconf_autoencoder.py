import requests
import json, os

url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")

nn_id = "nn00005"
wf_ver_id = "1"

# update source_info
# set netconf_node in NN_WF_NODE_INFO
resp = requests.put('http://' + url + '/api/v1/type/wf/state/netconf/detail/autoencoder/nnid/' + nn_id + '/ver/' + wf_ver_id + '/node/netconf_node/',
                     json={
                         # Parameters
                        "learning_rate" : 0.01,
                        "iter" : 10,
                        "batch_size" : 256,
                        "examples_to_show" : 10,
                        # Network Parameters
                        "n_hidden" : 256, # 1st layer num features
                        "n_input" : 30000,  # data input (img shape: 28*28)
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))
