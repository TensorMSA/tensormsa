import requests
import json, os
from common.utils import *
url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")

# resp = requests.post('http://' + url + '/api/v1/type/service/chatbot/')
# data = json.loads(resp.json())
# print("evaluation result : {0}".format(data))
resp = requests.put('http://' + url + '/api/v1/type/service/chatbot/C00001/',
                    json={  "unique_id" : "",
                            "package_id" : "",
                            "intent_id" : "",
                            "intent_name" : "",
                            "input_data" : "오늘 근무가?",
                            "convert_data" : "",
                            "intent_history" : [],
                            "request_type" : "text",
                            "service_type" : "",
                            "story_board_id" : "",
                            "story_req_entity" : {},
                            "story_set_entity" : {},
                            "opt_sel_list" : {},
                            "ontology_id" : "",
                            "ontology_req_parms" : {},
                            "ontology_set_parms" : {},
                            "output_data" : ""
                          })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))