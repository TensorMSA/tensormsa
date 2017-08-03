import requests
import json, os
url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")

resp = requests.post('http://' + url + '/api/v1/type/service/botbuilder/entityrelation/',
                     json={
                        "cb_id": "cb0001",
                        "entity_id" : "tagname",
                        "entity_uuid" : "asdf",
                        "entity_desc" : "이름",
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))
