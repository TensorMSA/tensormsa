import requests
import json, os

url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")

types = ["cnn", "frame",  "word2vec", "doc2vec", "seq2seq", "autoencoder", "anomaly", "seq2seq_csv", "renet", "word2vec_frame"]

for i in range(len(types)) :
    # insert workflow info
    resp = requests.post('http://' + url + '/api/v1/type/wf/target/init/mode/simple/nn0000' + str(i) +'/wfver/1/',
                         json={
                             "type": types[i]
                         })
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))
