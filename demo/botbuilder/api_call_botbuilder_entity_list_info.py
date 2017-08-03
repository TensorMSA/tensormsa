import requests
import json, os
url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")

resp = requests.post('http://' + url + '/api/v1/type/service/botbuilder/entitylist/',
                     json={
                        "cb_id": "cb0001",
                        "intent_id": "1",
                        'entity_type' : "key", #(custom/essential/response/default/key)
                        'entity_list' : {"key": ["이름", "직급", "직책", "근태코드", "그룹", "근무조", "업무", "날짜", "장소"]},
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))
