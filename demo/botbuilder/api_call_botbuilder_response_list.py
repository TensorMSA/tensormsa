import requests
import json, os
url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8989")

resp = requests.post('http://' + url + '/api/v1/type/service/botbuilder/response/',
                     json={
                        "response_type" : "entity",
                        "output_entity" : {"entity":["tagdate","tagloc","tagmenu"]},
                        "output_data" : "",
                        "nn_id" : "", #Seq2Seq 사용시
                        "story_id" : "1"
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

resp = requests.post('http://' + url + '/api/v1/type/service/botbuilder/response/',
                     json={
                        "response_type" : "entity",
                        "output_entity" : {},
                        "output_data" : "",
                        "nn_id" : "", #Seq2Seq 사용시
                        "story_id" : "2"
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

resp = requests.post('http://' + url + '/api/v1/type/service/botbuilder/response/',
                     json={
                        "response_type" : "entity",
                        "output_entity" : {},
                        "output_data" : "",
                        "nn_id" : "", #Seq2Seq 사용시
                        "story_id" : "3"
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))
