import requests
import json, os
url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")

cb_id = "cb00013"
resp = requests.post('http://' + url + '/api/v1/type/service/botbuilder/entitylist/',
                     json={
                        "cb_id": cb_id,
                        "intent_id": "1",
                        'entity_type' : "key", #(custom/essential/response/default/key)
                        'entity_list' : {"key": ["tagdate", "tagloc", "tagmenu"]}
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

resp = requests.post('http://' + url + '/api/v1/type/service/botbuilder/entitylist/',
                     json={
                        "cb_id": cb_id,
                        "intent_id": "2",
                        'entity_type' : "key", #(custom/essential/response/default/key)
                        'entity_list' : {"key": ["tagdate", "tagloc"]}
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

resp = requests.post('http://' + url + '/api/v1/type/service/botbuilder/entitylist/',
                     json={
                        "cb_id": cb_id,
                        "intent_id": "3",
                        'entity_type' : "key", #(custom/essential/response/default/key)
                        'entity_list' : {"key": ["tagdate", "tagloc"]}
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))