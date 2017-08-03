import requests
import json, os
url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")

resp = requests.post('http://' + url + '/api/v1/type/service/botbuilder/intent/',
                     json={
                        #intent
                        "cb_id": "cb0001",
                        "intent_id": "1",
                        "intent_type": "model",
                        "intent_desc": "",
                        "rule_value": {"key": ["알려줘"]},
                        "nn_type": "Seq2Seq",
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))
