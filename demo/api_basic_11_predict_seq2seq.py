import requests
import json, os
from common.utils import *
url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")

# Run All Workflow
resp = requests.post('http://' + url + '/api/v1/type/service/state/predict/type/seq2seq/nnid/nn00004/ver/active/',
                     json={"input_data" : "안녕" }
                     )
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))




