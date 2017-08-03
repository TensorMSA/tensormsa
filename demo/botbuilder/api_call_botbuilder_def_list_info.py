import requests
import json, os
url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")

resp = requests.post('http://' + url + '/api/v1/type/service/botbuilder/def/',
                     json={
                        "cb_id" : "cb0001",
                        "chat_cate" : "EP",
                        "chat_sub_cate" : "people",
                        "cb_title" : "chatbot",
                        "cb_desc" : "find_people",
                        "creation_date": "2017-05-22T18:00:00.000",
                        "last_update_date": "2017-05-22T18:00:00.000",
                        "created_by" : "KSS",
                        "last_updated_by" : "KSS"
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))
