import requests
import json, os
from common.utils import *
url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")


nnid = 'nn00031'
ver = '1'
files = {
            'file': open('/hoya_src_root/nn00031/1/predict/predict.csv','rb')
        }

resp = requests.post('http://' + url + '/api/v1/type/service/state/predict/type/wdnn/nnid/'+nnid+'/ver/'+ver+'/',
                     files=files
                     )
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

