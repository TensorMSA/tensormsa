from unittest import TestCase
import requests
import json, os

url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")

class test_api_basic_0_node_rule(TestCase):
    def test_insert_menu_info(self):
            resp = requests.post('http://' + url + '/api/v1/type/wf/target/menu/',
                                 json={
                                     "wf_task_menu_id": "data",
                                     "wf_task_menu_name": "data",
                                     "wf_task_menu_desc": "data",
                                     "visible_flag": True
                                 })
            data = json.loads(resp.json())
            self.assertEqual(data, 'data')

    def test_insert_submenu_info(self):
        resp = requests.post('http://' + url + '/api/v1/type/wf/target/menu/data/submenu/',
                     json={
                        "wf_task_submenu_id": "data_image",
                        "wf_task_submenu_name": "data_image",
                        "wf_task_submenu_desc": "data_image",
                        "wf_node_class_path": "cluster.data.data_node_image",
                        "wf_node_class_name": "DataNodeImage"
                     })
        data = json.loads(resp.json())
        self.assertEqual(data, 'data_image')