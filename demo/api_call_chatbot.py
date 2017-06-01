import requests
import json, os
url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")

# resp = requests.post('http://' + url + '/api/v1/type/service/chatbot/')
# data = json.loads(resp.json())
# print("evaluation result : {0}".format(data))
resp = requests.put('http://' + url + '/api/v1/type/service/chatbot/C00001/',
                    json={  #"unique_id" : "",
                            #"package_id" : "",
                            "intent_id" : "",
                            # "intent_name" : "",
                            #"input_data" : "야드 담당자 알려줘",
                            "input_data" : "최욱 교대조 알아",
                            #"input_data": "회의를 김수상,김승우,신민호 차장으로 10시부터 11시까지 판교에 예약 해줘",
                            "convert_data" : "",
                            "intent_history" : [],
                            "request_type" : "text",
                            "service_type" : "",
                            "story_board_id" : "",
                            "story_key_entity" : [],
                            "story_slot_entity" : {},
                            # "opt_sel_list" : {},
                            # "ontology_id" : "",
                            # "ontology_req_parms" : {},
                            # "ontology_set_parms" : {},
                            "output_data" : ""
                          })
data = json.loads(resp.json())

print("evaluation result : {0}".format(data))
print("chatbot output is result : " + json.loads(data)['output_data'])

