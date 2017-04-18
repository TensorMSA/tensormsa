import requests
import json, os
from demo.api_basic_0_util import get_all_files

url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")

train_files =  get_all_files('/home/dev/csv/')

resp = requests.post('http://' + url + '/api/v1/type/wf/state/framedata/src/local/form/frame/prg/source/nnid/nn00009/ver/1/node/data_node/',
                     files = train_files)
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

resp = requests.put('http://' + url + '/api/v1/type/wf/state/framedata/src/local/form/frame/prg/source/nnid/nn00009/ver/1/node/data_node/',
                     json={
                         "type": "csv",
                         "source_server": "local",
                         "source_sql": "all",
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))
#
#update preprocess
resp = requests.put('http://' + url + '/api/v1/type/wf/state/framedata/src/local/form/raw/prg/pre/nnid/nn00009/ver/1/node/data_node/',
                      json={
                          "preprocess":  "null",
                      })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))
#
 # update store_path
resp = requests.put('http://' + url + '/api/v1/type/wf/state/framedata/src/local/form/frame/prg/store/nnid/nn00009/ver/1/node/data_node/',
                      json={
                          "store_path": "test"
                      })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))