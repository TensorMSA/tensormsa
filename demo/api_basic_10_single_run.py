import requests
import json, os
from common.utils import *
url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")

# [TEST - Celery]
# apt-get install rabbitmq-server
# service rabbitmq-server start
# rabbitmqctl add_user tensormsa tensormsa
# rabbitmqctl set_user_tags tensormsa administrator
# celery -A hoyai worker -l info
# ./manage.py runserver [HOST]:8000

# Single node Run
nn_id = "nn00004"
wf_ver_id = "2"
node_id = "nn00004_2_dataconf_node"

resp = requests.post('http://' + url + '/api/v1/type/runmanager/state/train/nnid/'+nn_id+'/ver/'+wf_ver_id+'/node/'+node_id+'/',
                    json={
                        "key": {"nn_id": nn_id,
                                "wf_ver_id": wf_ver_id,
                                "node_id": node_id
                                }
                     })

data = json.loads(resp.json())
print("evaluation result : {0}".format(data))