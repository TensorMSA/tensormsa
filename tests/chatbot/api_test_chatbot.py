from unittest import TestCase
#from django.utils import unittest
import requests
import json, os

url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")

class api_test_chatbot(TestCase):

    def setUp(self):
        print('Start ChatBot test')

    def tearDown(self):
        print('Finish ChatBot test')

    def test_api_Call(self):
        resp = requests.put('http://' + url + '/api/v1/type/service/chatbot/C00001/',
                            json={"unique_id": "",
                                  "package_id": "",
                                  "intent_id": "",
                                  "intent_name": "",
                                  "input_data": "김수상 지금 어디갔어",
                                  "convert_data": "",
                                  "intent_history": [],
                                  "request_type": "text",
                                  "service_type": "",
                                  "story_board_id": "3",
                                  "story_req_entity": {},
                                  "story_set_entity": {},
                                  "opt_sel_list": {},
                                  "ontology_id": "",
                                  "ontology_req_parms": {},
                                  "ontology_set_parms": {},
                                  "output_data": ""
                                  })
        data = json.loads(resp.json())
        self.assertTrue(json.loads(data)['output_data'])

    def test_api_reserve_meeting(self):
        resp = requests.put('http://' + url + '/api/v1/type/service/chatbot/C00001/',
                            json={"unique_id": "",
                                  "package_id": "",
                                  "intent_id": "",
                                  "intent_name": "",
                                  "input_data": "회의를 김수상,김승우,백지현 과장으로 10시부터 11시까지 판교에 예약 해줘",
                                  "convert_data": "",
                                  "intent_history": [],
                                  "request_type": "text",
                                  "service_type": "",
                                  "story_board_id": "3",
                                  "story_req_entity": {},
                                  "story_set_entity": {},
                                  "opt_sel_list": {},
                                  "ontology_id": "",
                                  "ontology_req_parms": {},
                                  "ontology_set_parms": {},
                                  "output_data": ""
                                  })
        data = json.loads(resp.json())
        self.assertTrue(json.loads(data)['output_data'])

    def test_api_find_business(self):
        resp = requests.put('http://' + url + '/api/v1/type/service/chatbot/C00001/',
                            json={"unique_id": "",
                                  "package_id": "",
                                  "intent_id": "",
                                  "intent_name": "",
                                  "input_data" : "야드 담당자 알려줘",
                                  "convert_data": "",
                                  "intent_history": [],
                                  "request_type": "text",
                                  "service_type": "",
                                  "story_board_id": "3",
                                  "story_req_entity": {},
                                  "story_set_entity": {},
                                  "opt_sel_list": {},
                                  "ontology_id": "",
                                  "ontology_req_parms": {},
                                  "ontology_set_parms": {},
                                  "output_data": ""
                                  })
        data = json.loads(resp.json())
        self.assertTrue(json.loads(data)['output_data'])

    def test_api_present(self):
        resp = requests.put('http://' + url + '/api/v1/type/service/chatbot/C00001/',
                            json={"unique_id": "",
                                  "package_id": "",
                                  "intent_id": "",
                                  "intent_name": "",
                                  "input_data": "김수상 지금 어디갔어",
                                  "convert_data": "",
                                  "intent_history": [],
                                  "request_type": "text",
                                  "service_type": "",
                                  "story_board_id": "3",
                                  "story_req_entity": {},
                                  "story_set_entity": {},
                                  "opt_sel_list": {},
                                  "ontology_id": "",
                                  "ontology_req_parms": {},
                                  "ontology_set_parms": {},
                                  "output_data": ""
                                  })
        data = json.loads(resp.json())
        self.assertTrue(json.loads(data)['output_data'])