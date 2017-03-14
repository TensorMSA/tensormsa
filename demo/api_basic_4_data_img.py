import requests
import json, os

url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")

resp = requests.put('http://' + url + '/api/v1/type/wf/state/imgdata/src/local/form/file/prg/source/nnid/nn00004/ver/1/node/datasrc/',
                     json={
                         "type": "local image",
                         "source_path": "/hoya_src_root/nn00004/1/datasrc",
                         "preprocess": {"x_size": 100,
                                        "y_size": 100},
                         "store_path": "/hoya_str_root/nn00004/1/datasrc"
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))
