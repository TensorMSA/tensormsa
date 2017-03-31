import requests
import json, os
from common.utils import *
url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")

# [TEST - Celery]
# apt-get install rabbitmq-server
# service rabbitmq-server start
# rabbitmqctl add_user tensormsa tensormsa
# rabbitmqctl set_user_tags tensormsa administrator
#rabbitmqctl set_permissions -p / tensormsa '.*' '.*' '.*'
# celery -A hoyai worker -l info
# ./manage.py runserver [HOST]:8000

# Run All Workflow
# url                                (r'^api/v1/type/service/state/predict/type/(?P<type>.*)/nnid/(?P<nnid>.*)/ver/(?P<ver>.*)/',
resp = requests.post('http://' + url + '/api/v1/type/service/state/predict/type/wdnn/nnid/nn00004/ver/11/',
                     json={
                         "type": "sim",
                         "val_1":["탄핵"],
                         "val_2":["."]
                     }
                     )
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))
