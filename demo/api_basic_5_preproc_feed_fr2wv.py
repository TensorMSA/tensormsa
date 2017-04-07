import requests
import json, os

url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")

# merge data sets to one
resp = requests.post('http://' + url + '/api/v1/type/wf/state/pre/detail/feed/src/frame/net/word2vec/nnid/nn00009/ver/1/node/pre_feed_fr2wv_train/',
                     json={
                         "col_list" : ["a","b"],
                         "max_sentence_len": 10,
                         "preprocess": "mecab",
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))