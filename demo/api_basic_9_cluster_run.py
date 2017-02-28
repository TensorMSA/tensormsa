import requests
import json, os

url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")

# [TEST - Celery]
# apt-get install rabbitmq-server
# service rabbitmq-server start
# rabbitmqctl add_user tensormsa tensormsa
# rabbitmqctl set_user_tags tensormsa administrator
# celery -A hoyai worker -l info
# ./manage.py runserver [HOST]:8000

# insert workflow info
resp = requests.post('http://' + url + '/api/v1/type/runmanager/state/train/nnid/nn00004/ver/1/')
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

