import requests
import json, os
from demo.api_basic_0_util import get_all_files

url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")

train_files =  get_all_files('/home/dev/csv/')

resp = requests.post('http://' + url + '/api/v1/type/wf/state/framedata/src/local/form/raw/prg/source/nnid/nn00009/ver/1/node/test_data_node/',
                     files = train_files)
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

resp = requests.put('http://' + url + '/api/v1/type/wf/state/framedata/src/local/form/raw/prg/source/nnid/nn00009/ver/1/node/test_data_node/',
                     json={
                         "type": "csv",
                         "source_server": "local",
                         "source_sql": "all",
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

#update preprocess
resp = requests.put('http://' + url + '/api/v1/type/wf/state/framedata/src/local/form/raw/prg/pre/nnid/nn00009/ver/1/node/test_data_node/',
                    json={"preprocess" : "null"})
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

 # update store_path
resp = requests.put('http://' + url + '/api/v1/type/wf/state/framedata/src/local/form/raw/prg/store/nnid/nn00009/ver/1/node/test_data_node/')
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))


# merge data sets to one
resp = requests.put('http://' + url + '/api/v1/type/wf/state/pre/detail/feed/src/frame/net/word2vec/nnid/nn00009/ver/1/node/pre_feed_fr2wv_test/',
                     json={
                         "col_list" : ["a","b"],
                         "max_sentence_len": 10,
                         "preprocess": "mecab",
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))