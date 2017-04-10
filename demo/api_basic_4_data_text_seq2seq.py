import requests
import json, os
from demo.api_basic_0_util import get_all_files

url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")

train_files =  get_all_files('/home/dev/train/')
eval_files =  get_all_files('/home/dev/eval/')

# update source_info
resp = requests.post('http://' + url + '/api/v1/type/wf/state/textdata/src/local/form/raw/prg/source/nnid/nn00004/ver/1/node/data_encode_node/',
                     files = train_files,)
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# update source_info
resp = requests.put('http://' + url + '/api/v1/type/wf/state/textdata/src/local/form/raw/prg/source/nnid/nn00004/ver/1/node/data_encode_node/',
                     json={
                         "source_server": "local",
                         "source_sql": "all",
                         "max_sentence_len": 50
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# update preprocess
# preprocess : kkma, twiter, mecab, nltk
resp = requests.put('http://' + url + '/api/v1/type/wf/state/textdata/src/local/form/raw/prg/pre/nnid/nn00004/ver/1/node/data_encode_node/',
                     json={
                         "preprocess":  "mecab",
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# update store_path
resp = requests.put('http://' + url + '/api/v1/type/wf/state/textdata/src/local/form/raw/prg/store/nnid/nn00004/ver/1/node/data_encode_node/')
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# check properties are updated well
resp = requests.get('http://' + url + '/api/v1/type/wf/state/textdata/src/local/form/raw/prg/source/nnid/nn00004/ver/1/node/data_encode_node/')
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))


# update source_info
resp = requests.post('http://' + url + '/api/v1/type/wf/state/textdata/src/local/form/raw/prg/source/nnid/nn00004/ver/1/node/data_decode_node/',
                     files = eval_files,)
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# update source_info
resp = requests.put('http://' + url + '/api/v1/type/wf/state/textdata/src/local/form/raw/prg/source/nnid/nn00004/ver/1/node/data_decode_node/',
                     json={
                         "source_server": "local",
                         "source_sql": "all",
                         "max_sentence_len": 50
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# update preprocess
# preprocess : kkma, twiter, mecab, nltk
resp = requests.put('http://' + url + '/api/v1/type/wf/state/textdata/src/local/form/raw/prg/pre/nnid/nn00004/ver/1/node/data_decode_node/',
                     json={
                         "preprocess":  "mecab",
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# update store_path
resp = requests.put('http://' + url + '/api/v1/type/wf/state/textdata/src/local/form/raw/prg/store/nnid/nn00004/ver/1/node/data_decode_node/')
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# check properties are updated well
resp = requests.get('http://' + url + '/api/v1/type/wf/state/textdata/src/local/form/raw/prg/source/nnid/nn00004/ver/1/node/data_decode_node/')
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))
