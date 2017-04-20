import requests
import json, os
from common.utils import *
url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")

# Test API for Document for vector using by Gensim

nn_id = "nn00001"
wf_ver = "1"

print('http://' + url + '/api/v1/type/result/nnid/' + nn_id + '/ver/'+ wf_ver +'/')
resp = requests.get('http://' + url + '/api/v1/type/result/nnid/' + nn_id + '/ver/'+ wf_ver +'/')
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

