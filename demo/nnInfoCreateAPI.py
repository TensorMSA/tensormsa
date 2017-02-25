# 네트워크 Create Api call
import requests
import json
from common.util import *

println("S")
url = "52.78.67.19:8000"

resp = requests.post('http://' + url + '/api/v1/type/common/target/nninfo/',
                             json={
                                 "category": "ERP",
                                 "subcate" : "MRO",
                                 "name": "MRO Classification",
                                 "desc" : "MRO Classification Description"
                             })

println("E")


print('resp=',resp)

data = json.loads(resp.json())
print("evaluation result : {0}".format(data))


