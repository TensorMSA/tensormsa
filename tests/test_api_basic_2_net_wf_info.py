from unittest import TestCase
import requests
import json, os

url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")

class test_api_basic_2_net_wf_info(TestCase):
        def test_insert_worflow_info(self):
            resp = requests.post('http://' + url + '/api/v1/type/common/target/nninfo/nn00004/version/',
                         json={
                             "nn_def_list_info_nn_id": "",
                             "nn_wf_ver_info": "test version info",
                             "condition": "1",
                             "active_flag": "N"
                         })
            data = json.loads(resp.json())
            self.assertEqual(data, 'nn00004')
