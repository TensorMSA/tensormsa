import requests
import json, os

url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")

# update source_info
resp = requests.put('http://' + url + '/api/v1/type/wf/state/netconf/detail/seq2seq/nnid/nn00004/ver/1/node/netconf_node/',
                     json={
                         "encoder_len" : 10,
                         "decoder_len" : 10,
                         "encoder_depth" : 2,
                         "decoder_depth" : 2,
                         "cell_type" : "lstm",   #vanila, lstm, gru
                         "cell_size" : 500,
                         "drop_out" : 0.8,
                         "word_embed_type" : "w2v",   #w2v, onehot
                         "word_embed_id" : "nn00002",
                         "batch_size" : 100,
                         "iter" : 10,
                         "early_stop" : 0.9,
                         "learning_rate" : 0.001
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))



# update source_info
resp = requests.put('http://' + url + '/api/v1/type/wf/state/netconf/detail/seq2seq/nnid/nn00007/ver/1/node/netconf_node/',
                     json={
                         "encoder_len" : 10,
                         "decoder_len" : 2,
                         "encoder_depth" : 2,
                         "decoder_depth" : 2,
                         "cell_type" : "lstm",   #vanila, lstm, gru
                         "cell_size" : 500,
                         "drop_out" : 0.8,
                         "word_embed_type" : "w2v",   #w2v, onehot
                         "word_embed_id" : "nn00002",
                         "vocab_size" : 0,
                         "batch_size" : 100,
                         "iter" : 10,
                         "early_stop" : 0.9,
                         "learning_rate" : 0.001
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# update source_info
resp = requests.put('http://' + url + '/api/v1/type/wf/state/netconf/detail/seq2seq/nnid/nn00007/ver/1/node/netconf_node/',
                     json={
                         "encoder_len" : 10,
                         "decoder_len" : 2,
                         "encoder_depth" : 2,
                         "decoder_depth" : 2,
                         "cell_type" : "lstm",   #vanila, lstm, gru
                         "cell_size" : 500,
                         "drop_out" : 0.8,
                         "word_embed_type" : "onehot",   #w2v, onehot
                         "word_embed_id" : "",
                         "vocab_size" : 100,
                         "batch_size" : 100,
                         "iter" : 10,
                         "early_stop" : 0.9,
                         "learning_rate" : 0.001
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))