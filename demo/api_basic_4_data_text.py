import requests
import json, os

url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")

# update source_info
resp = requests.post('http://' + url + '/api/v1/type/wf/state/textdata/src/local/form/raw/prg/source/nnid/nn00004/ver/3/node/data_node/',
                     json={
                         "source_server": "local",
                         "source_sql": "all",
                         "source_path": "test",
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# update preprocess
resp = requests.post('http://' + url + '/api/v1/type/wf/state/textdata/src/local/form/raw/prg/pre/nnid/nn00004/ver/3/node/data_node/',
                     json={
                         "preprocess":  "konlp",
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# update store_path
resp = requests.post('http://' + url + '/api/v1/type/wf/state/textdata/src/local/form/raw/prg/store/nnid/nn00004/ver/3/node/data_node/',
                     json={
                         "store_path": "test"
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# check properties are updated well
resp = requests.get('http://' + url + '/api/v1/type/wf/state/textdata/src/local/form/raw/prg/source/nnid/nn00004/ver/3/node/data_node/')
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))