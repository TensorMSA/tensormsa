import requests
import json, os
url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")

resp = requests.post('http://' + url + '/api/v1/type/service/botbuilder/tagging/',
                     json={
                        "cb_id": "cb0001",
                        "pos_type": "mecab",
                        "proper_noun": {"tagwc": [1, "/hoya_model_root/chatbot/wc.txt", False],
                                        "tagceo": [1, "/hoya_model_root/chatbot/ceo.txt", False],
                                        "tagloc": [1, "/hoya_model_root/chatbot/loc.txt", False],
                                        "tagorg": [1, "/hoya_model_root/chatbot/org.txt", False],
                                        "tagrot": [1, "/hoya_model_root/chatbot/rot.txt", False],
                                        "tagdate": [4, "/hoya_model_root/chatbot/super.txt", False],
                                        "taghead": [1, "/hoya_model_root/chatbot/head.txt", False],
                                        "tagname": [2, "/hoya_model_root/chatbot/name.txt", False],
                                        "tagrank": [1, "/hoya_model_root/chatbot/rank.txt", False],
                                        "tagcompany": [2, "/hoya_model_root/chatbot/company.txt", False]},

                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))
