import requests
import json, os
from common.utils import *
url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")

resp = requests.post('http://' + url + '/api/v1/type/service/chatbot/')
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))




