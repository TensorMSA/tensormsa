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
nn_id = "mro0003"

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

'files000001':  open('//hoya_src_root/mro0001/test.jpg','rb')
    # ,'files000002':  open('/home/dev/hoyai/demo/data/airplane/2air.jpg','rb')
# ,'files000003':  open('/hoya_src_root/nn00004/21/personData/LSH/20170418_094624.jpg','rb')

 #  'files000004':  open('/hoya_src_root/nn00004/21/personDataTest/PSC/20170417_180614.jpg','rb')
 # ,'files000005':  open('/hoya_src_root/nn00004/21/personDataTest/PJH/20170417_180225(0).jpg','rb')
# , 'files000006':  open('/hoya_src_root/nn00004/21/personDataTest/LSH/20170417_180436.jpg','rb')

        }

restURL = 'http://' + url + '/api/v1/type/service/state/predict/type/renet/nnid/'+nn_id+'/ver/0/'

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


