import requests
import json, os

url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")

# merge data sets to one
resp = requests.post('http://' + url + '/api/v1/type/wf/state/pre/detail/feed/src/frame/net/seq2seq/nnid/nn00007/ver/1/node/feed_fr2seq/',
                     json={
                         "encode_column" : "a",
                         "decode_column" : "b",
                         "encode_len": 10,
                         "decode_len": 2,
                         "preprocess": "mecab",
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))