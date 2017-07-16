from unittest import TestCase
import requests
import json, os

url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")

class api_test_chatbot(TestCase):

   # def __init__(self):

    def setUp(self):
        print('Start ChatBot test')
        self.input_1 = ["포항에 근무하는 과장 찾아줘"]
        self.input_2 = ["정보기획실 김수상의 팀장 찾아줘","김수상의 그룹장 찾아줘", "정보기획실 김수상의 리더 찾아줘"]
        self.input_3 = ["정보기획실장에게 전화 걸어줘"]
        self.input_4 = ["포항 김수상에게 연락해줘"]
        self.input_5 = ["김수상은 휴가 인가요"]
        self.input_8 = ["포항 정보기획실 김수상 찾아줘", "정보기획실 김수상 알아"]
        self.input_9 = ["정보기획실 과장은 누구", "정보기획실 P4"]

    def tearDown(self):
        print('Finish ChatBot test')

    def test_api_Call_1(self):
        for text in self.input_1:
            resp = requests.put('http://' + url + '/api/v1/type/service/chatbot/cb0001/',
                                                  json={
                                    "intent_id": "",
                                    "edit_history": [],
                                    "input_data": text,
                                    "convert_data": "",
                                    "intent_history": [],
                                    "request_type": "text",
                                    "service_type": "I",
                                    "story_board_id": "",
                                    "story_key_entity": [],
                                    "story_slot_entity": {},
                                    "output_data": ""
                                      })
            print(resp.json()['test_intent_id'])
            self.assertEqual(resp.json()['test_intent_id'], ['1'], msg="Intent 1 is wrong")

    def test_api_Call_2(self):
        for text in self.input_2:
            resp = requests.put('http://' + url + '/api/v1/type/service/chatbot/cb0001/',
                                                  json={
                                    "intent_id": "",
                                    "edit_history": [],
                                    "input_data": text,
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
        for text in self.input_3:

            resp = requests.put('http://' + url + '/api/v1/type/service/chatbot/cb0001/',
                                                  json={
                                    "intent_id": "",
                                    "edit_history": [],
                                    "input_data": text,
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
        for text in self.input_4:
            resp = requests.put('http://' + url + '/api/v1/type/service/chatbot/cb0001/',
                                                  json={
                                    "intent_id": "",
                                    "edit_history": [],
                                    "input_data": text,
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
        for text in self.input_5:
            resp = requests.put('http://' + url + '/api/v1/type/service/chatbot/cb0001/',
                                                  json={
                                    "intent_id": "",
                                    "edit_history": [],
                                    "input_data": text,
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

    def test_api_Call_8(self):
        for text in self.input_8:
            resp = requests.put('http://' + url + '/api/v1/type/service/chatbot/cb0001/',
                                                  json={
                                    "intent_id": "",
                                    "edit_history": [],
                                    "input_data": text,
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

    def test_api_Call_9_1(self):

        for text in self.input_9:
            resp = requests.put('http://' + url + '/api/v1/type/service/chatbot/cb0001/',
                                                  json={
                                    "intent_id": "",
                                    "edit_history": [],
                                    "input_data": text,
                                    "convert_data": "",
                                    "intent_history": [],
                                    "request_type": "text",
                                    "service_type": "I",
                                    "story_board_id": "",
                                    "story_key_entity": [],
                                    "story_slot_entity": {},
                                    "output_data": ""
                                      })
            self.assertEqual(resp.json()['test_intent_id'], ['9'], msg="Intent 9 is wrong")
