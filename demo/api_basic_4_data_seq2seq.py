import requests
import json, os

url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")

# update source_info
resp = requests.post('http://' + url + '/api/v1/type/wf/state/textdata/src/local/form/raw/prg/source/nnid/nn00004/ver/5/node/data_encode_node/',
                     json={
                         "source_server": "local",
                         "source_sql": "all",
                         "source_path": "encode",
                         "max_sentence_len": 50
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# update preprocess
# preprocess : kkma, twiter, mecab, nltk
resp = requests.post('http://' + url + '/api/v1/type/wf/state/textdata/src/local/form/raw/prg/pre/nnid/nn00004/ver/5/node/data_encode_node/',
                     json={
                         "preprocess":  "mecab",
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# update store_path
resp = requests.post('http://' + url + '/api/v1/type/wf/state/textdata/src/local/form/raw/prg/store/nnid/nn00004/ver/5/node/data_encode_node/',
                     json={
                         "store_path": "encode"
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# check properties are updated well
resp = requests.get('http://' + url + '/api/v1/type/wf/state/textdata/src/local/form/raw/prg/source/nnid/nn00004/ver/5/node/data_encode_node/')
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))



# update source_info
resp = requests.post('http://' + url + '/api/v1/type/wf/state/textdata/src/local/form/raw/prg/source/nnid/nn00004/ver/5/node/data_decode_node/',
                     json={
                         "source_server": "local",
                         "source_sql": "all",
                         "source_path": "decode",
                         "max_sentence_len": 50
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# update preprocess
# preprocess : kkma, twiter, mecab, nltk
resp = requests.post('http://' + url + '/api/v1/type/wf/state/textdata/src/local/form/raw/prg/pre/nnid/nn00004/ver/5/node/data_decode_node/',
                     json={
                         "preprocess":  "mecab",
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# update store_path
resp = requests.post('http://' + url + '/api/v1/type/wf/state/textdata/src/local/form/raw/prg/store/nnid/nn00004/ver/5/node/data_decode_node/',
                     json={
                         "store_path": "decode"
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# check properties are updated well
resp = requests.get('http://' + url + '/api/v1/type/wf/state/textdata/src/local/form/raw/prg/source/nnid/nn00004/ver/5/node/data_decode_node/')
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))
