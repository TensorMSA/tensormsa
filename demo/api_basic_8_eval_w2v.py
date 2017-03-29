import requests
import json, os
from demo.api_basic_0_util import get_all_files

url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")

train_files =  get_all_files('/home/dev/csv/')

resp = requests.post('http://' + url + '/api/v1/type/wf/state/textdata/src/local/form/raw/prg/source/nnid/nn00002/ver/1/node/test_data_node/',
                     files = train_files)
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# update source_info
resp = requests.put('http://' + url + '/api/v1/type/wf/state/textdata/src/local/form/raw/prg/source/nnid/nn00002/ver/1/node/test_data_node/',
                     json={
                         "source_server": "local",
                         "source_sql": "all",
                         "max_sentence_len" : 50
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# update preprocess
# preprocess : kkma, twiter, mecab, nltk
resp = requests.put('http://' + url + '/api/v1/type/wf/state/textdata/src/local/form/raw/prg/pre/nnid/nn00002/ver/1/node/test_data_node/',
                     json={
                         "preprocess":  "mecab",
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# update store_path
resp = requests.put('http://' + url + '/api/v1/type/wf/state/textdata/src/local/form/raw/prg/store/nnid/nn00002/ver/1/node/test_data_node/')
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))
