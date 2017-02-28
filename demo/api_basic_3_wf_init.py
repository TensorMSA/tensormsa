import requests
import json, os

url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")


# insert workflow info
resp = requests.post('http://' + url + '/api/v1/type/wf/target/init/mode/simple/nn00004/wfver/1/',
                     json={
                         "type": "image"
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

