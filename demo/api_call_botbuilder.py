import requests
import json, os
url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")

resp = requests.post('http://' + url + '/api/v1/type/service/botbuilder/',
                     json={
                        "cb_id" : "cb0007",
                        "chat_cate" : "EP",
                        "chat_sub_cate" : "people",
                        "cb_title" : "chatbot",
                        "cb_desc" : "find_people",
                        "creation_date": "2017-05-22T18:00:00.000",
                        "last_update_date": "2017-05-22T18:00:00.000",
                        "created_by" : "KSS",
                        "last_updated_by" : "KSS",
                        #intent
                        "intent_id": "7",
                        "intent_type": "model",
                        "intent_desc": "",
                        "nn_id": "nn00001",
                        "nn_type": "Seq2Seq",
                        #story
                        'story_id' : "7",
                        'story_desc' : "find_tel",
                        #entity
                        'entity_type' : "key", #(custom/essential/response/default/key)
                        'entity_list' : "type"
                        })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))


