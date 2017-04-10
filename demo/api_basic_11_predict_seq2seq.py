import requests
import json, os
from common.utils import *
url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")


# Run All Workflow
resp = requests.post('http://' + url + '/api/v1/type/service/state/predict/type/seq2seq/nnid/nn00007/ver/active/',
                     json={"input_data" : "드래곤은 뭐지?" }
                     )
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))


# Run All Workflow
resp = requests.post('http://' + url + '/api/v1/type/service/state/predict/type/seq2seq/nnid/nn00007/ver/active/',
                     json={"input_data" : "칼베리온은 누구?" }
                     )
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))