import requests
import json, os
url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")

resp = requests.post('http://' + url + '/api/v1/type/service/botbuilder/model/',
                     json={
                        #Model List
                        "cb_id": "cb0001",
                        "nn_id": "lstmcrf0002", #wcnn_ksw01
                        'nn_purpose': "NER", # Intend ADD
                        'nn_type': "bilstmcrf",
                        'nn_label_data': {"entity": ["이름", "직급", "직책", "근태코드", "그룹", "근무조", "업무", "날짜", "장소"]},
                        'nn_desc': "ner",
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))
