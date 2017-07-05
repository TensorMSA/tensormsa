import requests
import json, os
url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")

resp = requests.post('http://' + url + '/api/v1/type/service/botbuilder/',
                     json={
                        "cb_id" : "cb0001",
                        "chat_cate" : "EP",
                        "chat_sub_cate" : "people",
                        "cb_title" : "chatbot",
                        "cb_desc" : "find_people",
                        "creation_date": "2017-05-22T18:00:00.000",
                        "last_update_date": "2017-05-22T18:00:00.000",
                        "created_by" : "KSS",
                        "last_updated_by" : "KSS",

                        #Model List
                        "cb_id": "cb0001",
                        "nn_id": "lstmcrf0002", #wcnn_ksw01
                        'nn_purpose': "NER", # Intend ADD
                        'nn_type': "bilstmcrf",
                        'nn_label_data': {"entity": ["이름", "직급", "직책", "근태코드", "그룹", "근무조", "업무", "날짜", "장소"]},
                        'nn_desc': "ner",

                        #intent
                        "cb_id": "cb0001",
                        "intent_id": "1",
                        "intent_type": "model",
                        "intent_desc": "",
                        "rule_value": {"key": ["알려줘"]},
                        "nn_type": "Seq2Seq",

                        # #story
                        # 'story_id' : "1",
                        # 'story_desc' : "find_tel",

                        #entity
                        "cb_id": "cb0001",
                        "intent_id": "1",
                        'entity_type' : "key", #(custom/essential/response/default/key)
                        'entity_list' : {"key": ["이름", "직급", "직책", "근태코드", "그룹", "근무조", "업무", "날짜", "장소"]},
                        # entity
                        # "cb_id": "cb0001",
                        # "intent_id": "1",
                        # 'story_id': "1",
                        # 'entity_type': "essential",  # (custom/essential/response/default/key)
                        # 'entity_list': {"essential": ["이름"]},
                        # # entity
                        # "cb_id": "cb0001",
                        # "intent_id": "1",
                        # 'story_id': "1",
                        # 'entity_type': "key_values",  # (custom/essential/response/default/key)
                        # 'entity_list': {"장소": ["센터", "판교", "포항", "광양"], "직급": ["사원", "대리", "과장", "차장", "부장", "팀장", "사업부장", "상사", "리더"]},

                        #tagging
                        "cb_id": "cb0001",
                        "pos_type": "mecab",
                        "proper_noun": {"tagwc": [1, "/hoya_model_root/chatbot/wc.txt", False], "tagceo": [1, "/hoya_model_root/chatbot/ceo.txt", False], "tagloc": [1, "/hoya_model_root/chatbot/loc.txt", False], "tagorg": [1, "/hoya_model_root/chatbot/org.txt", False], "tagrot": [1, "/hoya_model_root/chatbot/rot.txt", False], "tagdate": [4, "/hoya_model_root/chatbot/super.txt", False], "taghead": [1, "/hoya_model_root/chatbot/head.txt", False], "tagname": [2, "/hoya_model_root/chatbot/name.txt", False], "tagrank": [1, "/hoya_model_root/chatbot/rank.txt", False], "tagcompany": [2, "/hoya_model_root/chatbot/company.txt", False]},

                        #entity relation
                        "cb_id": "cb0001",
                        "entity_id" : "tagname",
                        "entity_uuid" : "asdf",
                        "entity_desc" : "이름",
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))
