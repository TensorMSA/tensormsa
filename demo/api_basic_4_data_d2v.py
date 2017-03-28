import requests
import json, os

url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")

nn_id = "nn00003"
wf_ver_id = "1"

# update source_info
resp = requests.post('http://' + url + '/api/v1/type/wf/state/textdata/src/local/form/raw/prg/source/nnid/' + nn_id + '/ver/' + wf_ver_id + '/node/data_node/',
                     json={
                         "source_server": "local",
                         "source_sql": "all",
                         "source_path": "test",
                         "max_sentence_len" : 50
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# update preprocess
# preprocess : kkma, twiter, mecab, nltk
resp = requests.put('http://' + url + '/api/v1/type/wf/state/textdata/src/local/form/raw/prg/pre/nnid/' + nn_id + '/ver/' + wf_ver_id + '/node/data_node/',
                     json={
                         "preprocess":  "mecab",
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# update store_path
resp = requests.put('http://' + url + '/api/v1/type/wf/state/textdata/src/local/form/raw/prg/store/nnid/' + nn_id + '/ver/' + wf_ver_id + '/node/data_node/',
                     json={
                         "store_path": "d2v"
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# check properties are updated well
resp = requests.get('http://' + url + '/api/v1/type/wf/state/textdata/src/local/form/raw/prg/source/nnid/' + nn_id + '/ver/' + wf_ver_id + '/node/data_node/')
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))