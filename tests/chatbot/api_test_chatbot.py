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

    def test_api_Call_8(self):
        resp = requests.put('http://' + url + '/api/v1/type/service/chatbot/cb0001/',
                                              json={
                                "intent_id": "",
                                "edit_history": [],
                                "input_data": "포항 화성부 김수상 찾아줘",
                                "convert_data": "",
                                "intent_history": [],
                                "request_type": "text",
                                "service_type": "I",
                                "story_board_id": "",
                                "story_key_entity": [],
                                "story_slot_entity": {},
                                "output_data": ""
                                  })
        self.assertEqual(resp.json()['test_intent_id'], ['8'], msg="Intent 8 is wrong")

    def test_api_Call_1(self):
        resp = requests.put('http://' + url + '/api/v1/type/service/chatbot/cb0001/',
                                              json={
                                "intent_id": "",
                                "edit_history": [],
                                "input_data": "포항에 근무하는 과장 찾아줘",
                                "convert_data": "",
                                "intent_history": [],
                                "request_type": "text",
                                "service_type": "I",
                                "story_board_id": "",
                                "story_key_entity": [],
                                "story_slot_entity": {},
                                "output_data": ""
                                  })
        self.assertEqual(resp.json()['test_intent_id'], ['1'], msg="Intent 1 is wrong")

    def test_api_Call_2(self):
        resp = requests.put('http://' + url + '/api/v1/type/service/chatbot/cb0001/',
                                              json={
                                "intent_id": "",
                                "edit_history": [],
                                "input_data": "김수상의 그룹장 찾아줘",
                                "convert_data": "",
                                "intent_history": [],
                                "request_type": "text",
                                "service_type": "I",
                                "story_board_id": "",
                                "story_key_entity": [],
                                "story_slot_entity": {},
                                "output_data": ""
                                  })
        self.assertEqual(resp.json()['test_intent_id'], ['2'], msg="Intent 2 is wrong")

    def test_api_Call_3(self):
        resp = requests.put('http://' + url + '/api/v1/type/service/chatbot/cb0001/',
                                              json={
                                "intent_id": "",
                                "edit_history": [],
                                "input_data": "정보기획실장에게 전화 걸어줘",
                                "convert_data": "",
                                "intent_history": [],
                                "request_type": "text",
                                "service_type": "I",
                                "story_board_id": "",
                                "story_key_entity": [],
                                "story_slot_entity": {},
                                "output_data": ""
                                  })
        self.assertEqual(resp.json()['test_intent_id'], ['3'], msg="Intent 3 is wrong")

    def test_api_Call_4(self):
        resp = requests.put('http://' + url + '/api/v1/type/service/chatbot/cb0001/',
                                              json={
                                "intent_id": "",
                                "edit_history": [],
                                "input_data": "포항 김수상에게 연락해줘",
                                "convert_data": "",
                                "intent_history": [],
                                "request_type": "text",
                                "service_type": "I",
                                "story_board_id": "",
                                "story_key_entity": [],
                                "story_slot_entity": {},
                                "output_data": ""
                                  })
        self.assertEqual(resp.json()['test_intent_id'], ['4'], msg="Intent 4 is wrong")

    def test_api_Call_5(self):
        resp = requests.put('http://' + url + '/api/v1/type/service/chatbot/cb0001/',
                                              json={
                                "intent_id": "",
                                "edit_history": [],
                                "input_data": "김수상은 휴가 인가요",
                                "convert_data": "",
                                "intent_history": [],
                                "request_type": "text",
                                "service_type": "I",
                                "story_board_id": "",
                                "story_key_entity": [],
                                "story_slot_entity": {},
                                "output_data": ""
                                  })
        self.assertEqual(resp.json()['test_intent_id'], ['5'], msg="Intent 5 is wrong")

    def test_api_Call_8_1(self):
        resp = requests.put('http://' + url + '/api/v1/type/service/chatbot/cb0001/',
                                              json={
                                "intent_id": "",
                                "edit_history": [],
                                "input_data": "정보기획실 김수상 알아",
                                "convert_data": "",
                                "intent_history": [],
                                "request_type": "text",
                                "service_type": "I",
                                "story_board_id": "",
                                "story_key_entity": [],
                                "story_slot_entity": {},
                                "output_data": ""
                                  })
        self.assertEqual(resp.json()['test_intent_id'], ['8'], msg="Intent 8 is wrong")