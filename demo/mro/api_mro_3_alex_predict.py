import requests
import json, os
from common.utils import *
import operator

println("S")
# [TEST - Celery]
# apt-get install rabbitmq-server
# service rabbitmq-server start
# rabbitmqctl add_user tensormsa tensormsa
# rabbitmqctl set_user_tags tensormsa administrator
# rabbitmqctl set_permissions -p / tensormsa '.*' '.*' '.*'
# celery -A hoyai worker -l info
# ./manage.py runserver [HOST]:8000
url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")
nn_id = "mro001"
wf_ver_id = 1
# get workflow version info
if wf_ver_id == 0:
    resp = requests.get('http://' + url + '/api/v1/type/common/target/nninfo/nnid/'+nn_id+'/version/')
    data = json.loads(resp.json())

    for config in data:
        if config["fields"]["active_flag"] == "Y":
            wf_ver_id = config["fields"]["nn_wf_ver_id"]

wf_ver_id = str(wf_ver_id)

files = {
        #  'files000001':  open('/home/dev/hoyai/demo/data/airplane/1air.jpg','rb')
        # ,'files000002':  open('/home/dev/hoyai/demo/data/airplane/2air.jpg','rb')
        # ,'files000003':  open('/home/dev/hoyai/demo/data/bolt/1bolt.jpg','rb')
        # ,'files000004':  open('/home/dev/hoyai/demo/data/bolt/2bolt.jpg','rb')
        # ,'files000005':  open('/home/dev/hoyai/demo/data/car/1car.jpg','rb')
        # ,'files000006':  open('/home/dev/hoyai/demo/data/car/2car.jpg','rb')
        # ,'files000007':  open('/home/dev/hoyai/demo/data/glove/1glove.jpg','rb')
        # ,'files000008':  open('/home/dev/hoyai/demo/data/glove/2glove.jpg','rb')
        # ,'files000009':  open('/home/dev/hoyai/demo/data/motor/1motor.jpg','rb')
        # ,'files000010':  open('/home/dev/hoyai/demo/data/motor/2motor.jpg','rb')

 'files000001':  open('/home/dev/hoyai/demo/data/airplane/1air.jpg','rb')
    ,'files000002':  open('/home/dev/hoyai/demo/data/airplane/2air.jpg','rb')
# ,'files000003':  open('/hoya_src_root/nn00004/21/personData/LSH/20170418_094624.jpg','rb')

 #  'files000004':  open('/hoya_src_root/nn00004/21/personDataTest/PSC/20170417_180614.jpg','rb')
 # ,'files000005':  open('/hoya_src_root/nn00004/21/personDataTest/PJH/20170417_180225(0).jpg','rb')
# , 'files000006':  open('/hoya_src_root/nn00004/21/personDataTest/LSH/20170417_180436.jpg','rb')

        }

restURL = 'http://' + url + '/api/v1/type/service/state/predict/type/cnn/nnid/'+nn_id+'/ver/'+wf_ver_id+'/'

resp = requests.post(restURL, files=files, json={
                         "config": {}
                         ,"labels":[]
                        }
                     )
data = json.loads(resp.json())
try:
    if data["status"] == "404":
        print(data["result"])
except:
    for train in data:
        print("FileName = "+train)
        print(data[train]['key'])
        print(data[train]['val'])
        print('')

println("E")


