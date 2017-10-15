import requests
import json, os
url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")

cb_id = "cb00013"
#NER CASE
resp = requests.post('http://' + url + '/api/v1/type/service/botbuilder/model/',
                     json={
                        "cb_id": cb_id,
                        "nn_id": "lstmcrf0002",
                        'nn_purpose': "NER",
                        'nn_type': "bilstmcrf",
                        'nn_label_data': {"entity": []},
                        'nn_desc': "ner",
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

#Intent Case
resp = requests.post('http://' + url + '/api/v1/type/service/botbuilder/model/',
                     json={
                        "cb_id": cb_id,
                        "nn_id": "wcnntest02",
                        'nn_purpose': "Intend",
                        'nn_type': "char-cnn",
                        'nn_label_data': {"entity": []},
                        'nn_desc': "Intend",
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))
