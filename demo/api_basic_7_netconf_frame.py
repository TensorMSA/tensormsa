import requests
import json, os

url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")

#url(r'^api/v1/type/wf/state/netconf/detail/wdnn/nnid/(?P<nnid>.*)/ver/(?P<ver>.*)/node/(?P<node>.*)/',
#WorkFlowNetConfWdnn
# update source_info
try:
    resp = requests.post('http://' + url + '/api/v1/type/wf/state/netconf/detail/wdnn/nnid/nn00004/ver/2/node/netconf_node/',
                        json={
                            "model_path": "test",
                            "hidden_layers": [50,20],
                            "activation_function": "Relu"
                        })
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))
except Exception as e:
    raise Exception(e)