import requests
import json

url = "{0}:{1}".format("localhost" , "8000")

resp = requests.post('http://' + url + '/api/v1/type/wf/state/imgdata/detail/localimg/prg/source/nnid/nn00004/ver/1/',
                     json={
                         "type": "local image"
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))