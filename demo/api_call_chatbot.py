import requests
import json, os
url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")

# resp = requests.post('http://' + url + '/api/v1/type/service/chatbot/')
# data = json.loads(resp.json())
# print("evaluation result : {0}".format(data))
resp = requests.put('http://' + url + '/api/v1/type/service/chatbot/cb0007/',
                    json={
                            "intent_id" : "7",
                            "edit_history" : [],
                            "input_data": "김수상의 전화번호",
                            "convert_data" : "",
                            "intent_history" : [],
                            "request_type" : "text",
                            "service_type" : "I",
                            "story_board_id" : "",
                            "story_key_entity" : [],
                            "story_slot_entity" : {},
                            "output_data" : ""
                          })

print("evaluation result : {0}".format(resp.json()))
print("chatbot output is result : " + resp.json()['output_data'])

