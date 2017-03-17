import requests
import json, os
from common.utils import *
url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")
println("S")
# [TEST - Celery]
# apt-get install rabbitmq-server
# service rabbitmq-server start
# rabbitmqctl add_user tensormsa tensormsa
# rabbitmqctl set_user_tags tensormsa administrator
#rabbitmqctl set_permissions -p / tensormsa '.*' '.*' '.*'
# celery -A hoyai worker -l info
# ./manage.py runserver [HOST]:8000
typeStr = "cnn"
nn_id = "nn00004"

files = {'files': open('/hoya_src_root/dataTest/car/2car.jpg','rb')}

resp = requests.post('http://' + gUrl + '/api/v1/type/service/state/predict/type/'+typeStr+'/nnid/'+nn_id+'/',
                     files=files,
                     json={
                         "type": "cnn"
                     }
                     )

data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

println("E")


