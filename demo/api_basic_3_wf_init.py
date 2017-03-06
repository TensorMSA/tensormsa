import requests
import json, os

url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")


# insert workflow info
resp = requests.post('http://' + url + '/api/v1/type/wf/target/init/mode/simple/nn00004/wfver/1/',
                     json={
                         "type": "image"
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# insert workflow info
resp = requests.post('http://' + url + '/api/v1/type/wf/target/init/mode/simple/nn00004/wfver/2/',
                     json={
                         "type": "frame"
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# insert workflow info
resp = requests.post('http://' + url + '/api/v1/type/wf/target/init/mode/simple/nn00004/wfver/3/',
                     json={
                         "type": "word2vec"
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# insert workflow info
resp = requests.post('http://' + url + '/api/v1/type/wf/target/init/mode/simple/nn00004/wfver/4/',
                     json={
                         "type": "doc2vec"
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# insert workflow info
resp = requests.post('http://' + url + '/api/v1/type/wf/target/init/mode/simple/nn00004/wfver/5/',
                     json={
                         "type": "seq2seq"
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# insert workflow info
resp = requests.post('http://' + url + '/api/v1/type/wf/target/init/mode/simple/nn00004/wfver/6/',
                     json={
                         "type": "autoencoder"
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# insert workflow info
resp = requests.post('http://' + url + '/api/v1/type/wf/target/init/mode/simple/nn00004/wfver/7/',
                     json={
                         "type": "anomaly"
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))