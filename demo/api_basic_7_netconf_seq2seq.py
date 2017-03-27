import requests
import json, os

url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")

# update source_info
resp = requests.put('http://' + url + '/api/v1/type/wf/state/netconf/detail/seq2seq/nnid/nn00004/ver/5/node/netconf_node/',
                     json={
                         "model_path" : "test",
                         "encoder_len" : 50,
                         "decoder_len" : 50,
                         "encoder_depth" : 2,
                         "decoder_depth" : 2,
                         "cell_type" : "lstm",   #vanila, lstm, gru
                         "cell_size" : 50,
                         "drop_out" : 0.5,
                         "word_embed_type" : "w2v",   #w2v, onehot
                         "word_embed_id" : "nn00003",
                         "batch_size" : 100,
                         "iter" : 5,
                         "early_stop" : 0.9,
                         "learning_rate" : 0.01
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))



# update source_info
resp = requests.put('http://' + url + '/api/v1/type/wf/state/netconf/detail/seq2seq/nnid/nn00004/ver/8/node/netconf_node/',
                     json={
                         "model_path" : "test",
                         "encoder_len" : 50,
                         "decoder_len" : 50,
                         "encoder_depth" : 2,
                         "decoder_depth" : 2,
                         "cell_type" : "lstm",   #vanila, lstm, gru
                         "cell_size" : 50,
                         "drop_out" : 0.5,
                         "word_embed_type" : "w2v",   #w2v, onehot
                         "word_embed_id" : "nn00003",
                         "batch_size" : 100,
                         "iter" : 5,
                         "early_stop" : 0.9,
                         "learning_rate" : 0.01
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))