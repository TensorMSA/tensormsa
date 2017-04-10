import requests
import json, os
from common.utils import *
url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")

# Test API for Document for vector using by Gensim

nn_id = "nn00003"

# Run All Workflow
resp = requests.post('http://' + url + '/api/v1/type/service/state/predict/type/d2v/nnid/' + nn_id + '/ver/active/',
                     json={
                         "type": "sim",
                         "val_1":["스마트"],
                         "val_2":["."]
                     }
                     )
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))



