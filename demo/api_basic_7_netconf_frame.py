import requests
import json, os

url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")

#url(r'^api/v1/type/wf/state/netconf/detail/wdnn/nnid/(?P<nnid>.*)/ver/(?P<ver>.*)/node/(?P<node>.*)/',
#WorkFlowNetConfWdnn
# update source_info
try:
    resp = requests.post('http://' + url + '/api/v1/type/wf/state/netconf/detail/wdnn/nnid/nn00001/ver/1/node/netconf_node/',
                        json={
                            "model_path": "test",
                            "hidden_layers": [100,50],
                            "activation_function": "Relu",
                            "batch_size" : 9000,
                            "epoch" : 1,
                            "model_type" : "category"
                        })
    # data = json.loads(resp.json())
    # print("evaluation result : {0}".format(data))
    # resp = requests.post('http://' + url + '/api/v1/type/wf/state/netconf/detail/wdnn/nnid/nn00001/ver/1/node/netconf_node/',
    #                     json={
    #                         "model_path": "test",
    #                         "hidden_layers": [100,50],
    #                         "activation_function": "Relu",
    #                         "batch_size" : 9000,
    #                         "epoch" : 1,
    #                         "model_type" : "regression"
    #                     })
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))
except Exception as e:
    raise Exception(e)