from unittest import TestCase
import requests
import json, os

url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")

class test_api_basic_1_net_info(TestCase):
        def test_delete_nn_info(self):
            resp = requests.delete('http://' + url + '/api/v1/type/common/target/nninfo/',
                                   json=["nn00003"])
            data = json.loads(resp.json())
            self.assertEqual(data, ['nn00003'])

