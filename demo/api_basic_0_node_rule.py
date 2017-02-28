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
                        "wf_node_class_path": "cluster.data.data_node_image",
                        "wf_node_class_name": "DataNodeImage"
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# insert submenu info
resp = requests.post('http://' + url + '/api/v1/type/wf/target/menu/data/submenu/',
                     json={
                        "wf_task_submenu_id": "data_frame",
                        "wf_task_submenu_name": "data_frame",
                        "wf_task_submenu_desc": "data_frame",
                        "wf_node_class_path": "cluster.data.data_node_frame",
                        "wf_node_class_name": "DataNodeFrame"
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# insert submenu info
resp = requests.post('http://' + url + '/api/v1/type/wf/target/menu/data/submenu/',
                     json={
                        "wf_task_submenu_id": "data_text",
                        "wf_task_submenu_name": "data_text",
                        "wf_task_submenu_desc": "data_text",
                        "wf_node_class_path": "cluster.data.data_node_text",
                        "wf_node_class_name": "DataNodeText"
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
                        "wf_node_class_path": "cluster.preprocess.preprocess_node_merge",
                        "wf_node_class_name": "PreProcessNodeMerge"
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# insert submenu info
resp = requests.post('http://' + url + '/api/v1/type/wf/target/menu/preprocess/submenu/',
                     json={
                        "wf_task_submenu_id": "pre_prenet",
                        "wf_task_submenu_name": "pre_prenet",
                        "wf_task_submenu_desc": "pre_prenet",
                        "wf_node_class_path": "cluster.preprocess.preprocess_node_prenet",
                        "wf_node_class_name": "PreProcessNodePreNet"
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
                        "wf_node_class_path": "cluster.dataconfig.dataconf_node_frame",
                        "wf_node_class_name" : "DataConfNodeFrame"
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
                        "wf_node_class_path": "cluster.neuralnet.neuralnet_node_wdnn",
                        "wf_node_class_name" : "NeuralNetNodeWdnn"
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# insert submenu info
resp = requests.post('http://' + url + '/api/v1/type/wf/target/menu/netconf/submenu/',
                     json={
                        "wf_task_submenu_id": "nf_cnn",
                        "wf_task_submenu_name": "nf_cnn",
                        "wf_task_submenu_desc": "nf_cnn",
                        "wf_node_class_path": "cluster.neuralnet.neuralnet_node_cnn",
                        "wf_node_class_name" : "NeuralNetNodeCnn"
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))


# insert submenu info
resp = requests.post('http://' + url + '/api/v1/type/wf/target/menu/netconf/submenu/',
                     json={
                        "wf_task_submenu_id": "nf_renet",
                        "wf_task_submenu_name": "nf_renet",
                        "wf_task_submenu_desc": "nf_renet",
                        "wf_node_class_path": "cluster.neuralnet.neuralnet_node_residual",
                        "wf_node_class_name": "NeuralNetNodeReNet"
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))


##################################################
# Test Menu
##################################################

# insert menu info
resp = requests.post('http://' + url + '/api/v1/type/wf/target/menu/',
                     json={
                        "wf_task_menu_id": "eval",
                        "wf_task_menu_name": "eval",
                        "wf_task_menu_desc": "eval",
                        "visible_flag": True
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# insert submenu info
resp = requests.post('http://' + url + '/api/v1/type/wf/target/menu/eval/submenu/',
                     json={
                        "wf_task_submenu_id": "eval_ten",
                        "wf_task_submenu_name": "eval_ten",
                        "wf_task_submenu_desc": "eval_ten",
                        "wf_node_class_path": "cluster.eval.eval_node_tenfold",
                        "wf_node_class_name": "EvalNodeTenFold"
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# insert submenu info
resp = requests.post('http://' + url + '/api/v1/type/wf/target/menu/netconf/submenu/',
                     json={
                        "wf_task_submenu_id": "eval_ran",
                        "wf_task_submenu_name": "eval_ran",
                        "wf_task_submenu_desc": "eval_ran",
                        "wf_node_class_path": "cluster.eval.eval_node_random",
                        "wf_node_class_name": "EvalNodeRandom"
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))


# insert submenu info
resp = requests.post('http://' + url + '/api/v1/type/wf/target/menu/netconf/submenu/',
                     json={
                        "wf_task_submenu_id": "eval_extra",
                        "wf_task_submenu_name": "eval_extra",
                        "wf_task_submenu_desc": "eval_extra",
                        "wf_node_class_path": "cluster.eval.eval_node_extra",
                        "wf_node_class_name": "EvalNodeExtra"
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))