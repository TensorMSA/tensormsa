from unittest import TestCase
import requests
import os

url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")

class api_test_chatbot(TestCase):

    def setUp(self):
        print('Start ChatBot test')
        self.input_1 = ["포항에 근무하는 과장 찾아줘","포항 차장 알려줘"]
        self.input_2 = ["정보기획실 김수상의 팀장 찾아줘","김수상의 그룹장 찾아줘", "정보기획실 김수상의 리더 찾아줘"]
        self.input_3 = ["정보기획실장에게 전화 걸어줘"]
        self.input_4 = ["포항 김수상에게 연락해줘"]
        self.input_5 = ["김수상은 휴가 인가요"]
        self.input_6 = ["터키법인장 알아"]
        self.input_7 = ["인니법인장", "정보기획실장"]
        self.input_8 = ["포항 정보기획실 김수상 찾아줘", "정보기획실 김수상 알아","정보기획실 김수상 찾아줘"]
        self.input_9 = ["정보기획실 과장은 누구", "정보기획실 P4"]

    def tearDown(self):
        print('Finish ChatBot test')

    def test_call(self):
        self.chat_api_call(self.input_1, '1')
        self.chat_api_call(self.input_2, '2')
        self.chat_api_call(self.input_3, '3')
        self.chat_api_call(self.input_4, '4')
        self.chat_api_call(self.input_5, '5')
        self.chat_api_call(self.input_6, '6')
        self.chat_api_call(self.input_7, '7')
        self.chat_api_call(self.input_8, '8')
        self.chat_api_call(self.input_9, '9')



    def chat_api_call(self, sentences, i):
        for text in sentences:
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
            self.assertEqual(resp.json()['test_intent_id'], [i], msg="Intent " + i + " is wrong")