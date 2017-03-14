import requests
import json, os

url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")


resp = requests.post('http://' + url + '/api/v1/type/wf/state/framedata/src/local/form/raw/prg/source/nnid/nn00004/ver/2/node/data_node/',
                     json={
                         "type": "csv",
                         "source_server": "local",
                         "source_sql": "all",
                         "source_path": "test",
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))
#
#update preprocess
resp = requests.post('http://' + url + '/api/v1/type/wf/state/framedata/src/local/form/raw/prg/pre/nnid/nn00004/ver/2/node/data_node/',
                      json={
                          "preprocess":  "null",
                      })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))
#
 # update store_path
resp = requests.post('http://' + url + '/api/v1/type/wf/state/framedata/src/local/form/raw/prg/store/nnid/nn00004/ver/2/node/data_node/',
                      json={
                          "store_path": "test"
                      })
