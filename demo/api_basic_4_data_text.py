import requests
import json, os

url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")

resp = requests.put('http://' + url + '/api/v1/type/wf/state/textdata/src/local/form/raw/prg/source/nnid/nn00004/ver/3/node/data_node/',
                     json={
                         "type": "local image",
                         "source_path": "/home/dev/",
                         "preprocess": {"x_size": 100,
                                        "y_size": 100},
                         "store_path": "/home/dev/"
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))
