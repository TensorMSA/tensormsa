import requests, json
from common.utils import *

nn_id = 'nn00006'
wf_ver_id = '1'
node = 'eval_node'
resp = requests.put('http://' + gUrl + '/api/v1/type/wf/state/eval/nnid/'+nn_id+'/ver/'+wf_ver_id+'/node/'+node+'/'
                     ,json={"type":"category"})
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))