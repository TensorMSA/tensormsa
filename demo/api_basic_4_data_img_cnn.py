import requests
import json, os
from demo.api_basic_0_util import get_all_files

url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")

train_files =  get_all_files('/home/dev/img/')

resp = requests.post('http://' + url + '/api/v1/type/wf/state/imgdata/src/local/form/file/prg/source/nnid/nn00005/ver/1/node/datasrc/',
                     files = train_files)
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

resp = requests.put('http://' + url + '/api/v1/type/wf/state/imgdata/src/local/form/file/prg/source/nnid/nn00005/ver/1/node/datasrc/',
                     json={
                         "type": "local image",
                         "source_path": "/hoya_src_root/nn00005/1/datasrc",
                         "preprocess": {"x_size": 100,
                                        "y_size": 100,
                                        "channel": 3
                                        },
                        "labels":[],
                         "store_path": "/hoya_str_root/nn00005/1/datasrc"
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))
