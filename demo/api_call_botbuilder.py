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
                        "nn_id": "lstmcrf025",
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
                        "proper_noun": {"부서": [3, "/home/dev/hoyai/demo/data/dept.txt"], "이름": [2, "/home/dev/hoyai/demo/data/name.txt"], "직급": [1, "/home/dev/hoyai/demo/data/grade.txt"], "회사": [0, "/home/dev/hoyai/demo/data/company.txt"]}
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))


