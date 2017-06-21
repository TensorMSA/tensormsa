import requests
import json, os

nn_id = 'nnnnn994'  # put some key value you want to test

url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")

resp = requests.post('http://' + url + '/api/v1/type/service/state/predict/type/wcnn/nnid/'+nn_id+'/ver/active/',
                     json={"input_data" : "[이름]" }
                     )
data = json.loads(resp.json())
print("evaluation result(2) : {0}".format(data))

#
# resp = requests.post('http://' + url + '/api/v1/type/service/state/predict/type/wcnn/nnid/'+nn_id+'/ver/active/',
#                      json={"input_data" : "[이름] 의 전화" }
#                      )
# data = json.loads(resp.json())
# print("evaluation result(6) : {0}".format(data))

# resp = requests.post('http://' + url + '/api/v1/type/service/state/predict/type/wcnn/nnid/'+nn_id+'/ver/active/',
#                      json={"input_data" : "[이름] 의 [직급] 전화 번호 알 아" }
#                      )
# data = json.loads(resp.json())
# print("evaluation result(6) : {0}".format(data))
#
# resp = requests.post('http://' + url + '/api/v1/type/service/state/predict/type/wcnn/nnid/'+nn_id+'/ver/active/',
#                      json={"input_data" : "[이름]을 찾아줘" , "num": 3, "clean_ans":False}
#                      )
# data = json.loads(resp.json())
# print("evaluation result(2) : {0}".format(data))
#
# resp = requests.post('http://' + url + '/api/v1/type/service/state/predict/type/wcnn/nnid/'+nn_id+'/ver/active/',
#                      json={"input_data" : "[이름] [직급] 을 찾아주라" , "num": 3, "clean_ans":False}
#                      )
# data = json.loads(resp.json())
# print("evaluation result(2) : {0}".format(data))
#
# resp = requests.post('http://' + url + '/api/v1/type/service/state/predict/type/wcnn/nnid/'+nn_id+'/ver/active/',
#                      json={"input_data" : "담당자 검색 해 줄레" , "num": 3, "clean_ans":False}
#                      )
# data = json.loads(resp.json())
# print("evaluation result(3) : {0}".format(data))
#
# resp = requests.post('http://' + url + '/api/v1/type/service/state/predict/type/wcnn/nnid/'+nn_id+'/ver/active/',
#                      json={"input_data" : "[이름] [직급] 찾 아 줘 " , "num": 0, "clean_ans":True}
#                      )
# data = json.loads(resp.json())
# print("evaluation result(2) : {0}".format(data))
#
# resp = requests.post('http://' + url + '/api/v1/type/service/state/predict/type/wcnn/nnid/'+nn_id+'/ver/active/',
#                      json={"input_data" : "[이름] 의 [직급] 찾 아 줘 " , "num": 0, "clean_ans":True}
#                      )
# data = json.loads(resp.json())
# print("evaluation result(6) : {0}".format(data))
#
# resp = requests.post('http://' + url + '/api/v1/type/service/state/predict/type/wcnn/nnid/'+nn_id+'/ver/active/',
#                      json={"input_data" : "[이름] [근태코드] 갔 어" , "num": 0, "clean_ans":True}
#                      )
# data = json.loads(resp.json())
# print("evaluation result(4) : {0}".format(data))
#
# resp = requests.post('http://' + url + '/api/v1/type/service/state/predict/type/wcnn/nnid/'+nn_id+'/ver/active/',
#                      json={"input_data" : "[이름] 의 [직급] 알 고 있 냐" , "num": 0, "clean_ans":True}
#                      )
# data = json.loads(resp.json())
# print("evaluation result(6) : {0}".format(data))
#
# resp = requests.post('http://' + url + '/api/v1/type/service/state/predict/type/wcnn/nnid/'+nn_id+'/ver/active/',
#                      json={"input_data" : "[이름] 의 사진" , "num": 0, "clean_ans":True}
#                      )
# data = json.loads(resp.json())
# print("evaluation result(8) : {0}".format(data))
#
# resp = requests.post('http://' + url + '/api/v1/type/service/state/predict/type/wcnn/nnid/'+nn_id+'/ver/active/',
#                      json={"input_data" : "[이름] 의 집 전화" , "num": 0, "clean_ans":True}
#                      )
# data = json.loads(resp.json())
# print("evaluation result(9) : {0}".format(data))
#
# resp = requests.post('http://' + url + '/api/v1/type/service/state/predict/type/wcnn/nnid/'+nn_id+'/ver/active/',
#                      json={"input_data" : "[이름] 의 휴대 전화" , "num": 0, "clean_ans":True}
#                      )
# data = json.loads(resp.json())
# print("evaluation result(10) : {0}".format(data))
#
# resp = requests.post('http://' + url + '/api/v1/type/service/state/predict/type/wcnn/nnid/'+nn_id+'/ver/active/',
#                      json={"input_data" : "[이름] 의 교대근무 조" , "num": 0, "clean_ans":True}
#                      )
# data = json.loads(resp.json())
# print("evaluation result(11) : {0}".format(data))
#
# resp = requests.post('http://' + url + '/api/v1/type/service/state/predict/type/wcnn/nnid/'+nn_id+'/ver/active/',
#                      json={"input_data" : "[이름] 의 직번은" , "num": 0, "clean_ans":True}
#                      )
# data = json.loads(resp.json())
# print("evaluation result(12) : {0}".format(data))
#
#
# resp = requests.post('http://' + url + '/api/v1/type/service/state/predict/type/wcnn/nnid/'+nn_id+'/ver/active/',
#                      json={"input_data" : "[이름] 의 [직급]" , "num": 0, "clean_ans":True}
#                      )
# data = json.loads(resp.json())
# print("evaluation result(2) : {0}".format(data))
#
# resp = requests.post('http://' + url + '/api/v1/type/service/state/predict/type/wcnn/nnid/'+nn_id+'/ver/active/',
#                      json={"input_data" : "[이름] 을 찾 아 줘" , "num": 0, "clean_ans":True}
#                      )
# data = json.loads(resp.json())
# print("evaluation result(2) : {0}".format(data))