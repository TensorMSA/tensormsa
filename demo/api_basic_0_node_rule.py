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

# insert raw submenu info
resp = requests.post('http://' + url + '/api/v1/type/wf/target/menu/data/submenu/',
                     json={
                        "wf_task_submenu_id": "data_raw",
                        "wf_task_submenu_name": "data_raw",
                        "wf_task_submenu_desc": "data_raw",
                        "wf_node_class_path": "cluster.data.data_node_raw",
                        "wf_node_class_name": "DataNodeRaw"
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

# insert submenu info
resp = requests.post('http://' + url + '/api/v1/type/wf/target/menu/data/submenu/',
                     json={
                        "wf_task_submenu_id": "data_iob",
                        "wf_task_submenu_name": "data_iob",
                        "wf_task_submenu_desc": "data_iob",
                        "wf_node_class_path": "cluster.data.data_node_iob",
                        "wf_node_class_name": "DataNodeIob"
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
                        "wf_node_class_path": "cluster.preprocess.pre_node_merge_text2seq",
                        "wf_node_class_name": "PreNodeMergeText2Seq"
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
                        "wf_node_class_name": "PreNodePreNet"
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# insert submenu info
resp = requests.post('http://' + url + '/api/v1/type/wf/target/menu/preprocess/submenu/',
                     json={
                        "wf_task_submenu_id": "pre_feed_fr2cnn",
                        "wf_task_submenu_name": "pre_feed_fr2cnn",
                        "wf_task_submenu_desc": "pre_feed_fr2cnn",
                        "wf_node_class_path": "cluster.preprocess.pre_node_feed_fr2cnn",
                        "wf_node_class_name": "PreNodeFeedFr2Cnn"
                     })

# insert submenu info
resp = requests.post('http://' + url + '/api/v1/type/wf/target/menu/preprocess/submenu/',
                     json={
                        "wf_task_submenu_id": "pre_feed_fr2seq",
                        "wf_task_submenu_name": "pre_feed_fr2seq",
                        "wf_task_submenu_desc": "pre_feed_fr2seq",
                        "wf_node_class_path": "cluster.preprocess.pre_node_feed_fr2seq",
                        "wf_node_class_name": "PreNodeFeedFr2Seq"
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# insert submenu info
resp = requests.post('http://' + url + '/api/v1/type/wf/target/menu/preprocess/submenu/',
                     json={
                        "wf_task_submenu_id": "pre_feed_fr2wdnn",
                        "wf_task_submenu_name": "pre_feed_fr2wdnn",
                        "wf_task_submenu_desc": "pre_feed_fr2wdnn",
                        "wf_node_class_path": "cluster.preprocess.pre_node_feed_fr2wdnn",
                        "wf_node_class_name": "PreNodeFeedFr2Wdnn"
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# insert submenu info
resp = requests.post('http://' + url + '/api/v1/type/wf/target/menu/preprocess/submenu/',
                     json={
                        "wf_task_submenu_id": "pre_feed_img2cnn",
                        "wf_task_submenu_name": "pre_feed_img2cnn",
                        "wf_task_submenu_desc": "pre_feed_img2cnn",
                        "wf_node_class_path": "cluster.preprocess.pre_node_feed_img2cnn",
                        "wf_node_class_name": "PreNodeFeedImg2Cnn"
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# insert submenu info
resp = requests.post('http://' + url + '/api/v1/type/wf/target/menu/preprocess/submenu/',
                     json={
                        "wf_task_submenu_id": "pre_feed_img2renet",
                        "wf_task_submenu_name": "pre_feed_img2renet",
                        "wf_task_submenu_desc": "pre_feed_img2renet",
                        "wf_node_class_path": "cluster.preprocess.pre_node_feed_img2renet",
                        "wf_node_class_name": "PreNodeFeedImg2Renet"
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# insert submenu info
resp = requests.post('http://' + url + '/api/v1/type/wf/target/menu/preprocess/submenu/',
                     json={
                        "wf_task_submenu_id": "pre_feed_text2dv",
                        "wf_task_submenu_name": "pre_feed_text2dv",
                        "wf_task_submenu_desc": "pre_feed_text2dv",
                        "wf_node_class_path": "cluster.preprocess.pre_node_feed_text2dv",
                        "wf_node_class_name": "PreNodeFeedText2Dv"
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# insert submenu info
resp = requests.post('http://' + url + '/api/v1/type/wf/target/menu/preprocess/submenu/',
                     json={
                        "wf_task_submenu_id": "pre_feed_text2seq",
                        "wf_task_submenu_name": "pre_feed_text2seq",
                        "wf_task_submenu_desc": "pre_feed_text2seq",
                        "wf_node_class_path": "cluster.preprocess.pre_node_feed_text2seq",
                        "wf_node_class_name": "PreNodeFeedText2Seq"
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# insert submenu info
resp = requests.post('http://' + url + '/api/v1/type/wf/target/menu/preprocess/submenu/',
                     json={
                        "wf_task_submenu_id": "pre_feed_text2wv",
                        "wf_task_submenu_name": "pre_feed_text2wv",
                        "wf_task_submenu_desc": "pre_feed_text2wv",
                        "wf_node_class_path": "cluster.preprocess.pre_node_feed_text2wv",
                        "wf_node_class_name": "PreNodeFeedText2Wv"
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# insert submenu info
resp = requests.post('http://' + url + '/api/v1/type/wf/target/menu/preprocess/submenu/',
                     json={
                        "wf_task_submenu_id": "pre_feed_img2auto",
                        "wf_task_submenu_name": "pre_feed_img2auto",
                        "wf_task_submenu_desc": "pre_feed_img2auto",
                        "wf_node_class_path": "cluster.preprocess.pre_node_feed_img2auto",
                        "wf_node_class_name": "PreNodeFeedImg2Auto"
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# insert submenu info
resp = requests.post('http://' + url + '/api/v1/type/wf/target/menu/preprocess/submenu/',
                     json={
                        "wf_task_submenu_id": "pre_feed_fr2auto",
                        "wf_task_submenu_name": "pre_feed_fr2auto",
                        "wf_task_submenu_desc": "pre_feed_fr2auto",
                        "wf_node_class_path": "cluster.preprocess.pre_node_feed_fr2auto",
                        "wf_node_class_name": "PreNodeFeedFr2Auto"
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# insert submenu info
resp = requests.post('http://' + url + '/api/v1/type/wf/target/menu/preprocess/submenu/',
                     json={
                        "wf_task_submenu_id": "pre_feed_keras2frame",
                        "wf_task_submenu_name": "pre_feed_keras2frame",
                        "wf_task_submenu_desc": "pre_feed_keras2frame",
                        "wf_node_class_path": "cluster.preprocess.pre_node_feed_keras2frame",
                        "wf_node_class_name": "PreNodeFeedKerasFrame"
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))
#PreNodeFeedKerasFrame



# insert submenu info
resp = requests.post('http://' + url + '/api/v1/type/wf/target/menu/preprocess/submenu/',
                     json={
                        "wf_task_submenu_id": "pre_feed_fr2wv",
                        "wf_task_submenu_name": "pre_feed_fr2wv",
                        "wf_task_submenu_desc": "pre_feed_fr2wv",
                        "wf_node_class_path": "cluster.preprocess.pre_node_feed_fr2wv",
                        "wf_node_class_name": "PreNodeFeedFr2Wv"
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# insert submenu info
resp = requests.post('http://' + url + '/api/v1/type/wf/target/menu/preprocess/submenu/',
                     json={
                        "wf_task_submenu_id": "pre_feed_fr2wcnn",
                        "wf_task_submenu_name": "pre_feed_fr2wcnn",
                        "wf_task_submenu_desc": "pre_feed_fr2wcnn",
                        "wf_node_class_path": "cluster.preprocess.pre_node_feed_fr2wcnn",
                        "wf_node_class_name": "PreNodeFeedFr2Wcnn"
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# insert submenu info
resp = requests.post('http://' + url + '/api/v1/type/wf/target/menu/preprocess/submenu/',
                     json={
                        "wf_task_submenu_id": "pre_feed_iob2bilstmcrf",
                        "wf_task_submenu_name": "pre_feed_iob2bilstmcrf",
                        "wf_task_submenu_desc": "pre_feed_iob2bilstmcrf",
                        "wf_node_class_path": "cluster.preprocess.pre_node_feed_iob2bilstmcrf",
                        "wf_node_class_name": "PreNodeFeedIob2BiLstmCrf"
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))


# insert submenu info
resp = requests.post('http://' + url + '/api/v1/type/wf/target/menu/preprocess/submenu/',
                     json={
                        "wf_task_submenu_id": "pre_feed_text2fasttext",
                        "wf_task_submenu_name": "pre_feed_text2fasttext",
                        "wf_task_submenu_desc": "pre_feed_text2fasttext",
                        "wf_node_class_path": "cluster.preprocess.pre_node_feed_text2fasttext",
                        "wf_node_class_name": "PreNodeFeedText2FastText"
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
                        "wf_task_submenu_id": "data_dfconf",
                        "wf_task_submenu_name": "data_dfconf",
                        "wf_task_submenu_desc": "data_dfconf",
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

# insert submenu info
resp = requests.post('http://' + url + '/api/v1/type/wf/target/menu/netconf/submenu/',
                     json={
                        "wf_task_submenu_id": "word_to_vec",
                        "wf_task_submenu_name": "word_to_vec",
                        "wf_task_submenu_desc": "word_to_vec",
                        "wf_node_class_path": "cluster.neuralnet.neuralnet_node_w2v",
                        "wf_node_class_name": "NeuralNetNodeWord2Vec"
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# insert submenu info
resp = requests.post('http://' + url + '/api/v1/type/wf/target/menu/netconf/submenu/',
                     json={
                        "wf_task_submenu_id": "doc_to_vec",
                        "wf_task_submenu_name": "doc_to_vec",
                        "wf_task_submenu_desc": "doc_to_vec",
                        "wf_node_class_path": "cluster.neuralnet.neuralnet_node_d2v",
                        "wf_node_class_name": "NeuralNetNodeDoc2Vec"
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# insert submenu info
resp = requests.post('http://' + url + '/api/v1/type/wf/target/menu/netconf/submenu/',
                     json={
                        "wf_task_submenu_id": "seq_to_seq",
                        "wf_task_submenu_name": "seq_to_seq",
                        "wf_task_submenu_desc": "seq_to_seq",
                        "wf_node_class_path": "cluster.neuralnet.neuralnet_node_seq2seq",
                        "wf_node_class_name": "NeuralNetNodeSeq2Seq"
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# insert submenu info
resp = requests.post('http://' + url + '/api/v1/type/wf/target/menu/netconf/submenu/',
                     json={
                        "wf_task_submenu_id": "autoencoder",
                        "wf_task_submenu_name": "autoencoder",
                        "wf_task_submenu_desc": "autoencoder",
                        "wf_node_class_path": "cluster.neuralnet.neuralnet_node_autoencoder",
                        "wf_node_class_name": "NeuralNetNodeAutoEncoder"
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# insert submenu info
resp = requests.post('http://' + url + '/api/v1/type/wf/target/menu/netconf/submenu/',
                     json={
                        "wf_task_submenu_id": "wcnn",
                        "wf_task_submenu_name": "wcnn",
                        "wf_task_submenu_desc": "wcnn",
                        "wf_node_class_path": "cluster.neuralnet.neuralnet_node_wcnn",
                        "wf_node_class_name": "NeuralNetNodeWideCnn"
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# insert submenu info
resp = requests.post('http://' + url + '/api/v1/type/wf/target/menu/netconf/submenu/',
                     json={
                        "wf_task_submenu_id": "bilstmcrf",
                        "wf_task_submenu_name": "bilstmcrf",
                        "wf_task_submenu_desc": "bilstmcrf",
                        "wf_node_class_path": "cluster.neuralnet.neuralnet_node_bilstmcrf",
                        "wf_node_class_name": "NeuralNetNodeBiLstmCrf"
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# insert submenu info
resp = requests.post('http://' + url + '/api/v1/type/wf/target/menu/netconf/submenu/',
                     json={
                        "wf_task_submenu_id": "keras_dnn",
                        "wf_task_submenu_name": "keras_dnn",
                        "wf_task_submenu_desc": "keras_dnn",
                        "wf_node_class_path": "cluster.neuralnet.neuralnet_node_kerasdnn",
                        "wf_node_class_name": "NeuralNetNodeKerasdnn"
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))

# insert submenu info
resp = requests.post('http://' + url + '/api/v1/type/wf/target/menu/netconf/submenu/',
                     json={
                        "wf_task_submenu_id": "fasttext",
                        "wf_task_submenu_name": "fasttext",
                        "wf_task_submenu_desc": "fasttext",
                        "wf_node_class_path": "cluster.neuralnet.neuralnet_node_fasttext",
                        "wf_node_class_name": "NeuralNetNodeFastText"
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
resp = requests.post('http://' + url + '/api/v1/type/wf/target/menu/eval/submenu/',
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
resp = requests.post('http://' + url + '/api/v1/type/wf/target/menu/eval/submenu/',
                     json={
                        "wf_task_submenu_id": "eval_extra",
                        "wf_task_submenu_name": "eval_extra",
                        "wf_task_submenu_desc": "eval_extra",
                        "wf_node_class_path": "cluster.eval.eval_node_extra",
                        "wf_node_class_name": "EvalNodeExtra"
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))