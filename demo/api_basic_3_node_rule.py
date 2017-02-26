import requests
import json, os

url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")

##################################################
# Data Menu
##################################################

# insert menu info
resp = requests.post('http://' + url + '/api/v1/type/wf/target/menu/',
                     json={
                        "wf_task_menu_id": "data",
                        "wf_task_menu_name": "data",
                        "wf_task_menu_desc": "data",
                        "visible_flag": True
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# insert submenu info
resp = requests.post('http://' + url + '/api/v1/type/wf/target/menu/data/submenu/',
                     json={
                        "wf_task_submenu_id": "data_image",
                        "wf_task_submenu_name": "data_image",
                        "wf_task_submenu_desc": "data_image",
                        "wf_node_class_name" : "cluster.data.data_node_image.DataNodeImage"
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# insert submenu info
resp = requests.post('http://' + url + '/api/v1/type/wf/target/menu/data/submenu/',
                     json={
                        "wf_task_submenu_id": "data_frame",
                        "wf_task_submenu_name": "data_frame",
                        "wf_task_submenu_desc": "data_frame",
                        "wf_node_class_name" : "cluster.data.data_node_frame.DataNodeFrame"
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# insert submenu info
resp = requests.post('http://' + url + '/api/v1/type/wf/target/menu/data/submenu/',
                     json={
                        "wf_task_submenu_id": "data_text",
                        "wf_task_submenu_name": "data_text",
                        "wf_task_submenu_desc": "data_text",
                        "wf_node_class_name" : "cluster.data.data_node_text.DataNodeText"
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))


##################################################
# PreProcess Menu
##################################################

# insert menu info
resp = requests.post('http://' + url + '/api/v1/type/wf/target/menu/',
                     json={
                        "wf_task_menu_id": "preprocess",
                        "wf_task_menu_name": "preprocess",
                        "wf_task_menu_desc": "preprocess",
                        "visible_flag": True
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# insert submenu info
resp = requests.post('http://' + url + '/api/v1/type/wf/target/menu/preprocess/submenu/',
                     json={
                        "wf_task_submenu_id": "pre_merge",
                        "wf_task_submenu_name": "pre_merge",
                        "wf_task_submenu_desc": "pre_merge",
                        "wf_node_class_name" : "cluster.preprocess.preprocess_node_merge.PreProcessNodeMerge"
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# insert submenu info
resp = requests.post('http://' + url + '/api/v1/type/wf/target/menu/preprocess/submenu/',
                     json={
                        "wf_task_submenu_id": "pre_prenet",
                        "wf_task_submenu_name": "pre_prenet",
                        "wf_task_submenu_desc": "pre_prenet",
                        "wf_node_class_name" : "cluster.preprocess.preprocess_node_prenet.PreProcessNodePreNet"
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))




##################################################
# DataConfig Menu
##################################################

# insert menu info
resp = requests.post('http://' + url + '/api/v1/type/wf/target/menu/',
                     json={
                        "wf_task_menu_id": "dataconf",
                        "wf_task_menu_name": "dataconf",
                        "wf_task_menu_desc": "dataconf",
                        "visible_flag": True
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# insert submenu info
resp = requests.post('http://' + url + '/api/v1/type/wf/target/menu/dataconf/submenu/',
                     json={
                        "wf_task_submenu_id": "df_frame",
                        "wf_task_submenu_name": "df_frame",
                        "wf_task_submenu_desc": "df_frame",
                        "wf_node_class_name" : "cluster.dataconfig.dataconf_node_frame.DataConfNodeFrame"
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))


##################################################
# NetConfig Menu
##################################################

# insert menu info
resp = requests.post('http://' + url + '/api/v1/type/wf/target/menu/',
                     json={
                        "wf_task_menu_id": "netconf",
                        "wf_task_menu_name": "netconf",
                        "wf_task_menu_desc": "netconf",
                        "visible_flag": True
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# insert submenu info
resp = requests.post('http://' + url + '/api/v1/type/wf/target/menu/netconf/submenu/',
                     json={
                        "wf_task_submenu_id": "nf_wdnn",
                        "wf_task_submenu_name": "nf_wdnn",
                        "wf_task_submenu_desc": "nf_wdnn",
                        "wf_node_class_name" : "cluster.neuralnet.neuralnet_node_wdnn.NeuralNetNodeWdnn"
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# insert submenu info
resp = requests.post('http://' + url + '/api/v1/type/wf/target/menu/netconf/submenu/',
                     json={
                        "wf_task_submenu_id": "nf_cnn",
                        "wf_task_submenu_name": "nf_cnn",
                        "wf_task_submenu_desc": "nf_cnn",
                        "wf_node_class_name" : "cluster.neuralnet.neuralnet_node_cnn.NeuralNetNodeCnn"
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))


# insert submenu info
resp = requests.post('http://' + url + '/api/v1/type/wf/target/menu/netconf/submenu/',
                     json={
                        "wf_task_submenu_id": "nf_renet",
                        "wf_task_submenu_name": "nf_renet",
                        "wf_task_submenu_desc": "nf_renet",
                        "wf_node_class_name" : "cluster.neuralnet.neuralnet_node_residual.NeuralNetNodeReNet"
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))