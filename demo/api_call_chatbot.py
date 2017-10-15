import requests
import json, os
url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")

#No Intent
resp = requests.put('http://' + url + '/api/v1/type/service/chatbot/cb00013/',
                    json={
                            "intent_id" : ['1'],
                            "edit_history" : [],
                            #"input_data": "여행 정보 알려줘",
                            "input_data": "오늘 판교에 피자 주문 하고 싶어",#오늘 판교
                            #"input_data": "호텔 예약 해줘",
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

#Exist Intent - Test Make Slot
# resp = requests.put('http://' + url + '/api/v1/type/service/chatbot/cb0001/',
#                     json={
#                             "intent_id" : ['1'],
#                             "edit_history" : [],
#                             "input_data": "오늘",
#                             "convert_data" : "",
#                             "intent_history" : [],
#                             "request_type" : "text",
#                             "service_type" : "I",
#                             "story_board_id" : "",
#                             "story_key_entity" : [],
#                             'story_slot_entity': {'tagmenu': ['메뉴'], 'tagloc': ['판교']},
#                             "output_data" : ""
#                           })
#
# print("evaluation result : {0}".format(resp.json()))
# print("chatbot output is result : " + resp.json()['output_data'])resp = requests.put('http://' + url + '/api/v1/type/service/chatbot/cb0001/',
#                     json={
#                             "intent_id" : ['1'],
#                             "edit_history" : [],
#                             "input_data": "오늘",
#                             "convert_data" : "",
#                             "intent_history" : [],
#                             "request_type" : "text",
#                             "service_type" : "I",
#                             "story_board_id" : "",
#                             "story_key_entity" : [],
#                             'story_slot_entity': {'tagmenu': ['메뉴'], 'tagloc': ['판교']},
#                             "output_data" : ""
#                           })
#
# print("evaluation result : {0}".format(resp.json()))
# print("chatbot output is result : " + resp.json()['output_data'])