from master.workflow.common.workflow_state_menu import WorkFlowStateMenu
from master.automl.automl_rule import AutoMlRule

def set_all_default_rules() :
    """
    Set all necessary default rules  
    :return: 
    """
    exec_func_list = [
        set_menu_rule,
        set_submenu_rule,
        set_node_alias_rule,
        set_automl_rule,
        set_automl_rule_etc
    ]

    setup_result = []
    for func in exec_func_list :
        setup_result.append(func())

    return setup_result

def set_menu_rule():
    """
    Set menu (category of nodes) for default 
    """
    try:
        confs = [
            {
                "wf_task_menu_id": "data",
                "wf_task_menu_name": "data",
                "wf_task_menu_desc": "data",
                "visible_flag": True
            },
            {
                "wf_task_menu_id": "preprocess",
                "wf_task_menu_name": "preprocess",
                "wf_task_menu_desc": "preprocess",
                "visible_flag": True
            },
            {
                "wf_task_menu_id": "dataconf",
                "wf_task_menu_name": "dataconf",
                "wf_task_menu_desc": "dataconf",
                "visible_flag": True
            },
            {
                "wf_task_menu_id": "netconf",
                "wf_task_menu_name": "netconf",
                "wf_task_menu_desc": "netconf",
                "visible_flag": True
            },
            {
                "wf_task_menu_id": "eval",
                "wf_task_menu_name": "eval",
                "wf_task_menu_desc": "eval",
                "visible_flag": True
            }

        ]
        for conf in confs :
            WorkFlowStateMenu().put_menu_info(conf)
        return {"menu_rule" : True}
    except Exception as e:
        return {"menu_rule" : False}

def set_submenu_rule():
    """
    Set submenu rules 
    """
    try:
        confs = [
            {
                "wf_task_menu_id": "data",
                "wf_task_submenu_id": "data_raw",
                "wf_task_submenu_name": "data_raw",
                "wf_task_submenu_desc": "data_raw",
                "wf_node_class_path": "cluster.data.data_node_raw",
                "wf_node_class_name": "DataNodeRaw"
            },
            {
                "wf_task_menu_id": "data",
                "wf_task_submenu_id": "data_image",
                "wf_task_submenu_name": "data_image",
                "wf_task_submenu_desc": "data_image",
                "wf_node_class_path": "cluster.data.data_node_image",
                "wf_node_class_name": "DataNodeImage"
            },
            {
                "wf_task_menu_id": "data",
                "wf_task_submenu_id": "data_frame",
                "wf_task_submenu_name": "data_frame",
                "wf_task_submenu_desc": "data_frame",
                "wf_node_class_path": "cluster.data.data_node_frame",
                "wf_node_class_name": "DataNodeFrame"
            },
            {
                "wf_task_menu_id": "data",
                "wf_task_submenu_id": "data_text",
                "wf_task_submenu_name": "data_text",
                "wf_task_submenu_desc": "data_text",
                "wf_node_class_path": "cluster.data.data_node_text",
                "wf_node_class_name": "DataNodeText"
            },
            {
                "wf_task_menu_id": "data",
                "wf_task_submenu_id": "data_iob",
                "wf_task_submenu_name": "data_iob",
                "wf_task_submenu_desc": "data_iob",
                "wf_node_class_path": "cluster.data.data_node_iob",
                "wf_node_class_name": "DataNodeIob"
            },
            #########################################################################
            {
                "wf_task_menu_id": "preprocess",
                "wf_task_submenu_id": "pre_feed_frame",
                "wf_task_submenu_name": "pre_feed_frame",
                "wf_task_submenu_desc": "pre_feed_frame",
                "wf_node_class_path": "cluster.preprocess.pre_node_feed_frame",
                "wf_node_class_name": "PreNodeFeedFrame"
            },
            {
                "wf_task_menu_id": "preprocess",
                "wf_task_submenu_id": "pre_feed_image",
                "wf_task_submenu_name": "pre_feed_image",
                "wf_task_submenu_desc": "pre_feed_image",
                "wf_node_class_path": "cluster.preprocess.pre_node_feed_image",
                "wf_node_class_name": "PreNodeFeedImage"
            },
            {
                "wf_task_menu_id": "preprocess",
                "wf_task_submenu_id": "pre_feed_nlp",
                "wf_task_submenu_name": "pre_feed_nlp",
                "wf_task_submenu_desc": "pre_feed_nlp",
                "wf_node_class_path": "cluster.preprocess.pre_node_feed_nlp",
                "wf_node_class_name": "PreNodeFeedNlp"
            },


            {
                "wf_task_menu_id": "preprocess",
                "wf_task_submenu_id": "pre_merge",
                "wf_task_submenu_name": "pre_merge",
                "wf_task_submenu_desc": "pre_merge",
                "wf_node_class_path": "cluster.preprocess.pre_node_merge_text2seq",
                "wf_node_class_name": "PreNodeMergeText2Seq"
            },
            {
                "wf_task_menu_id": "preprocess",
                "wf_task_submenu_id": "pre_prenet",
                "wf_task_submenu_name": "pre_prenet",
                "wf_task_submenu_desc": "pre_prenet",
                "wf_node_class_path": "cluster.preprocess.preprocess_node_prenet",
                "wf_node_class_name": "PreNodePreNet"
            },
            {
                "wf_task_menu_id": "preprocess",
                "wf_task_submenu_id": "pre_feed_fr2cnn",
                "wf_task_submenu_name": "pre_feed_fr2cnn",
                "wf_task_submenu_desc": "pre_feed_fr2cnn",
                "wf_node_class_path": "cluster.preprocess.pre_node_feed_fr2cnn",
                "wf_node_class_name": "PreNodeFeedFr2Cnn"
            },
            {
                "wf_task_menu_id": "preprocess",
                "wf_task_submenu_id": "pre_feed_fr2seq",
                "wf_task_submenu_name": "pre_feed_fr2seq",
                "wf_task_submenu_desc": "pre_feed_fr2seq",
                "wf_node_class_path": "cluster.preprocess.pre_node_feed_fr2seq",
                "wf_node_class_name": "PreNodeFeedFr2Seq"
            },
            {
                "wf_task_menu_id": "preprocess",
                "wf_task_submenu_id": "pre_feed_fr2wdnn",
                "wf_task_submenu_name": "pre_feed_fr2wdnn",
                "wf_task_submenu_desc": "pre_feed_fr2wdnn",
                "wf_node_class_path": "cluster.preprocess.pre_node_feed_fr2wdnn",
                "wf_node_class_name": "PreNodeFeedFr2Wdnn"
            },
            {
                "wf_task_menu_id": "preprocess",
                "wf_task_submenu_id": "pre_feed_fr2ml",
                "wf_task_submenu_name": "pre_feed_fr2ml",
                "wf_task_submenu_desc": "pre_feed_fr2ml",
                "wf_node_class_path": "cluster.preprocess.pre_node_feed_fr2ml",
                "wf_node_class_name": "PreNodeFeedFr2ML"
            },
            {
                "wf_task_menu_id": "preprocess",
                "wf_task_submenu_id": "pre_feed_img2cnn",
                "wf_task_submenu_name": "pre_feed_img2cnn",
                "wf_task_submenu_desc": "pre_feed_img2cnn",
                "wf_node_class_path": "cluster.preprocess.pre_node_feed_img2cnn",
                "wf_node_class_name": "PreNodeFeedImg2Cnn"
            },
            {
                "wf_task_menu_id": "preprocess",
                "wf_task_submenu_id": "pre_feed_img2renet",
                "wf_task_submenu_name": "pre_feed_img2renet",
                "wf_task_submenu_desc": "pre_feed_img2renet",
                "wf_node_class_path": "cluster.preprocess.pre_node_feed_img2renet",
                "wf_node_class_name": "PreNodeFeedImg2Renet"
            },
            {
                "wf_task_menu_id": "preprocess",
                "wf_task_submenu_id": "pre_feed_text2dv",
                "wf_task_submenu_name": "pre_feed_text2dv",
                "wf_task_submenu_desc": "pre_feed_text2dv",
                "wf_node_class_path": "cluster.preprocess.pre_node_feed_text2dv",
                "wf_node_class_name": "PreNodeFeedText2Dv"
            },
            {
                "wf_task_menu_id": "preprocess",
                "wf_task_submenu_id": "pre_feed_text2seq",
                "wf_task_submenu_name": "pre_feed_text2seq",
                "wf_task_submenu_desc": "pre_feed_text2seq",
                "wf_node_class_path": "cluster.preprocess.pre_node_feed_text2seq",
                "wf_node_class_name": "PreNodeFeedText2Seq"
            },
            {
                "wf_task_menu_id": "preprocess",
                "wf_task_submenu_id": "pre_feed_text2wv",
                "wf_task_submenu_name": "pre_feed_text2wv",
                "wf_task_submenu_desc": "pre_feed_text2wv",
                "wf_node_class_path": "cluster.preprocess.pre_node_feed_text2wv",
                "wf_node_class_name": "PreNodeFeedText2Wv"
            },
            {
                "wf_task_menu_id": "preprocess",
                "wf_task_submenu_id": "pre_feed_img2auto",
                "wf_task_submenu_name": "pre_feed_img2auto",
                "wf_task_submenu_desc": "pre_feed_img2auto",
                "wf_node_class_path": "cluster.preprocess.pre_node_feed_img2auto",
                "wf_node_class_name": "PreNodeFeedImg2Auto"
            },
            {
                "wf_task_menu_id": "preprocess",
                "wf_task_submenu_id": "pre_feed_fr2auto",
                "wf_task_submenu_name": "pre_feed_fr2auto",
                "wf_task_submenu_desc": "pre_feed_fr2auto",
                "wf_node_class_path": "cluster.preprocess.pre_node_feed_fr2auto",
                "wf_node_class_name": "PreNodeFeedFr2Auto"
            },
            {
                "wf_task_menu_id": "preprocess",
                "wf_task_submenu_id": "pre_feed_keras2frame",
                "wf_task_submenu_name": "pre_feed_keras2frame",
                "wf_task_submenu_desc": "pre_feed_keras2frame",
                "wf_node_class_path": "cluster.preprocess.pre_node_feed_keras2frame",
                "wf_node_class_name": "PreNodeFeedKerasFrame"
            },
            {
                "wf_task_menu_id": "preprocess",
                "wf_task_submenu_id": "pre_feed_fr2wv",
                "wf_task_submenu_name": "pre_feed_fr2wv",
                "wf_task_submenu_desc": "pre_feed_fr2wv",
                "wf_node_class_path": "cluster.preprocess.pre_node_feed_fr2wv",
                "wf_node_class_name": "PreNodeFeedFr2Wv"
            },
            {
                "wf_task_menu_id": "preprocess",
                "wf_task_submenu_id": "pre_feed_fr2wcnn",
                "wf_task_submenu_name": "pre_feed_fr2wcnn",
                "wf_task_submenu_desc": "pre_feed_fr2wcnn",
                "wf_node_class_path": "cluster.preprocess.pre_node_feed_fr2wcnn",
                "wf_node_class_name": "PreNodeFeedFr2Wcnn"
            },
            {
                "wf_task_menu_id": "preprocess",
                "wf_task_submenu_id": "pre_feed_iob2bilstmcrf",
                "wf_task_submenu_name": "pre_feed_iob2bilstmcrf",
                "wf_task_submenu_desc": "pre_feed_iob2bilstmcrf",
                "wf_node_class_path": "cluster.preprocess.pre_node_feed_iob2bilstmcrf",
                "wf_node_class_name": "PreNodeFeedIob2BiLstmCrf"
            },
            {
                "wf_task_menu_id": "preprocess",
                "wf_task_submenu_id": "pre_feed_text2fasttext",
                "wf_task_submenu_name": "pre_feed_text2fasttext",
                "wf_task_submenu_desc": "pre_feed_text2fasttext",
                "wf_node_class_path": "cluster.preprocess.pre_node_feed_text2fasttext",
                "wf_node_class_name": "PreNodeFeedText2FastText"
            },
            #########################################################################
            {
                "wf_task_menu_id": "dataconf",
                "wf_task_submenu_id": "data_dfconf",
                "wf_task_submenu_name": "data_dfconf",
                "wf_task_submenu_desc": "data_dfconf",
                "wf_node_class_path": "cluster.dataconfig.dataconf_node_frame",
                "wf_node_class_name": "DataConfNodeFrame"
            },
            #########################################################################
            {
                "wf_task_menu_id": "netconf",
                "wf_task_submenu_id": "nf_frame",
                "wf_task_submenu_name": "nf_frame",
                "wf_task_submenu_desc": "nf_frame",
                "wf_node_class_path": "cluster.neuralnet.neuralnet_node_frame",
                "wf_node_class_name": "NeuralNetNodeFrame"
            },
            {
                "wf_task_menu_id": "netconf",
                "wf_task_submenu_id": "nf_image",
                "wf_task_submenu_name": "nf_image",
                "wf_task_submenu_desc": "nf_image",
                "wf_node_class_path": "cluster.neuralnet.neuralnet_node_image",
                "wf_node_class_name": "NeuralNetNodeImage"
            },
            {
                "wf_task_menu_id": "netconf",
                "wf_task_submenu_id": "nf_nlp",
                "wf_task_submenu_name": "nf_nlp",
                "wf_task_submenu_desc": "nf_nlp",
                "wf_node_class_path": "cluster.neuralnet.neuralnet_node_nlp",
                "wf_node_class_name": "NeuralNetNodeNlp"
            },


            {
                "wf_task_menu_id": "netconf",
                "wf_task_submenu_id": "nf_wdnn",
                "wf_task_submenu_name": "nf_wdnn",
                "wf_task_submenu_desc": "nf_wdnn",
                "wf_node_class_path": "cluster.neuralnet.neuralnet_node_wdnn",
                "wf_node_class_name": "NeuralNetNodeWdnn"
            },
            {
                "wf_task_menu_id": "netconf",
                "wf_task_submenu_id": "nf_ml",
                "wf_task_submenu_name": "nf_ml",
                "wf_task_submenu_desc": "nf_ml",
                "wf_node_class_path": "cluster.neuralnet.ml_node",
                "wf_node_class_name": "MLNode"
            },
            {
                "wf_task_menu_id": "netconf",
                "wf_task_submenu_id": "nf_cnn",
                "wf_task_submenu_name": "nf_cnn",
                "wf_task_submenu_desc": "nf_cnn",
                "wf_node_class_path": "cluster.neuralnet.neuralnet_node_cnn",
                "wf_node_class_name": "NeuralNetNodeCnn"
            },
            {
                "wf_task_menu_id": "netconf",
                "wf_task_submenu_id": "nf_renet",
                "wf_task_submenu_name": "nf_renet",
                "wf_task_submenu_desc": "nf_renet",
                "wf_node_class_path": "cluster.neuralnet.neuralnet_node_residual",
                "wf_node_class_name": "NeuralNetNodeReNet"
            },
            {
                "wf_task_menu_id": "netconf",
                "wf_task_submenu_id": "word_to_vec",
                "wf_task_submenu_name": "word_to_vec",
                "wf_task_submenu_desc": "word_to_vec",
                "wf_node_class_path": "cluster.neuralnet.neuralnet_node_w2v",
                "wf_node_class_name": "NeuralNetNodeWord2Vec"
            },
            {
                "wf_task_menu_id": "netconf",
                "wf_task_submenu_id": "doc_to_vec",
                "wf_task_submenu_name": "doc_to_vec",
                "wf_task_submenu_desc": "doc_to_vec",
                "wf_node_class_path": "cluster.neuralnet.neuralnet_node_d2v",
                "wf_node_class_name": "NeuralNetNodeDoc2Vec"
            },
            {
                "wf_task_menu_id": "netconf",
                "wf_task_submenu_id": "seq_to_seq",
                "wf_task_submenu_name": "seq_to_seq",
                "wf_task_submenu_desc": "seq_to_seq",
                "wf_node_class_path": "cluster.neuralnet.neuralnet_node_seq2seq",
                "wf_node_class_name": "NeuralNetNodeSeq2Seq"
            },
            {
                "wf_task_menu_id": "netconf",
                "wf_task_submenu_id": "autoencoder",
                "wf_task_submenu_name": "autoencoder",
                "wf_task_submenu_desc": "autoencoder",
                "wf_node_class_path": "cluster.neuralnet.neuralnet_node_autoencoder",
                "wf_node_class_name": "NeuralNetNodeAutoEncoder"
            },
            {
                "wf_task_menu_id": "netconf",
                "wf_task_submenu_id": "wcnn",
                "wf_task_submenu_name": "wcnn",
                "wf_task_submenu_desc": "wcnn",
                "wf_node_class_path": "cluster.neuralnet.neuralnet_node_wcnn",
                "wf_node_class_name": "NeuralNetNodeWideCnn"
            },
            {
                "wf_task_menu_id": "netconf",
                "wf_task_submenu_id": "bilstmcrf",
                "wf_task_submenu_name": "bilstmcrf",
                "wf_task_submenu_desc": "bilstmcrf",
                "wf_node_class_path": "cluster.neuralnet.neuralnet_node_bilstmcrf",
                "wf_node_class_name": "NeuralNetNodeBiLstmCrf"
            },
            {
                "wf_task_menu_id": "netconf",
                "wf_task_submenu_id": "keras_dnn",
                "wf_task_submenu_name": "keras_dnn",
                "wf_task_submenu_desc": "keras_dnn",
                "wf_node_class_path": "cluster.neuralnet.neuralnet_node_kerasdnn",
                "wf_node_class_name": "NeuralNetNodeKerasdnn"
            },
            {
                "wf_task_menu_id": "netconf",
                "wf_task_submenu_id": "fasttext",
                "wf_task_submenu_name": "fasttext",
                "wf_task_submenu_desc": "fasttext",
                "wf_node_class_path": "cluster.neuralnet.neuralnet_node_fasttext",
                "wf_node_class_name": "NeuralNetNodeFastText"
            },
            {
                "wf_task_menu_id": "eval",
                "wf_task_submenu_id": "eval_ten",
                "wf_task_submenu_name": "eval_ten",
                "wf_task_submenu_desc": "eval_ten",
                "wf_node_class_path": "cluster.eval.eval_node_tenfold",
                "wf_node_class_name": "EvalNodeTenFold"
            },
            {
                "wf_task_menu_id": "eval",
                "wf_task_submenu_id": "eval_ran",
                "wf_task_submenu_name": "eval_ran",
                "wf_task_submenu_desc": "eval_ran",
                "wf_node_class_path": "cluster.eval.eval_node_random",
                "wf_node_class_name": "EvalNodeRandom"
            },
            {
                "wf_task_menu_id": "eval",
                "wf_task_submenu_id": "eval_extra",
                "wf_task_submenu_name": "eval_extra",
                "wf_task_submenu_desc": "eval_extra",
                "wf_node_class_path": "cluster.eval.eval_node_extra",
                "wf_node_class_name": "EvalNodeExtra"
            }
        ]
        for conf in confs :
            WorkFlowStateMenu().put_submenu_info(conf)
        return {"submenu_rule" : True}
    except Exception as e:
        return {"submenu_rule" : False}


def set_node_alias_rule():
    """
    Set node alias name for simple grpah flow set up
    """
    try:
        confs = [
            {
                 "graph_flow_info_id": 1, "graph_seq": 1, "graph_node": "netconf_node",
                 "graph_node_name": "netconf_node"
            }
            ,{
                 "graph_flow_info_id": 1, "graph_seq": 2, "graph_node": "netconf_data",
                 "graph_node_name": "netconf_data"
            }
            ,{
                 "graph_flow_info_id": 1, "graph_seq": 3, "graph_node": "netconf_feed",
                 "graph_node_name": "netconf_feed"
             }
            ,{
                 "graph_flow_info_id": 1, "graph_seq": 4, "graph_node": "eval_node",
                 "graph_node_name": "eval_node"
             }
            ,{
                 "graph_flow_info_id": 1, "graph_seq": 5, "graph_node": "eval_data",
                 "graph_node_name": "eval_data"
             }
            ,{
                 "graph_flow_info_id": 1, "graph_seq": 6, "graph_node": "eval_feed",
                 "graph_node_name": "eval_feed"
             }
            ##############################################################################################################################
            # Network Create 2 : Wdnn
            ##############################################################################################################################
            ,{
                 "graph_flow_info_id": 2, "graph_seq": 1, "graph_node": "netconf_node",
                 "graph_node_name": "netconf_node"
             }
            ,{
                 "graph_flow_info_id": 2, "graph_seq": 2, "graph_node": "netconf_data",
                 "graph_node_name": "data_node"
             }
            ,{
                 "graph_flow_info_id": 2, "graph_seq": 3, "graph_node": "netconf_feed",
                 "graph_node_name": "pre_feed_fr2wdnn_train"
             }
            ,{
                 "graph_flow_info_id": 2, "graph_seq": 4, "graph_node": "eval_node",
                 "graph_node_name": "eval_node"
             }
            ,{
                 "graph_flow_info_id": 2, "graph_seq": 5, "graph_node": "eval_data",
                 "graph_node_name": "evaldata"
             }
            ,{
                 "graph_flow_info_id": 2, "graph_seq": 6, "graph_node": "eval_feed",
                 "graph_node_name": "pre_feed_fr2wdnn_test"
             }
            ,{
                 "graph_flow_info_id": 2, "graph_seq": 7, "graph_node": "netconf_data_conf",
                 "graph_node_name": "dataconf_node"
             }
            ##############################################################################################################################
            # Network Create 3 : wdnn_keras
            ##############################################################################################################################
            ,{
                 "graph_flow_info_id": 3, "graph_seq": 1, "graph_node": "netconf_node",
                 "graph_node_name": "netconf_node"
             }
            ,{
                 "graph_flow_info_id": 3, "graph_seq": 2, "graph_node": "netconf_data",
                 "graph_node_name": "data_node"
             }
            ,{
                 "graph_flow_info_id": 3, "graph_seq": 3, "graph_node": "netconf_feed",
                 "graph_node_name": "pre_feed_keras2frame_train"
             }
            ,{
                 "graph_flow_info_id": 3, "graph_seq": 4, "graph_node": "eval_node",
                 "graph_node_name": "eval_node"
             }
            ,{
                 "graph_flow_info_id": 3, "graph_seq": 5, "graph_node": "eval_data",
                 "graph_node_name": "evaldata"
             }
            ,{
                 "graph_flow_info_id": 3, "graph_seq": 6, "graph_node": "eval_feed",
                 "graph_node_name": "pre_feed_keras2frame_test"
             }
            ,{
                 "graph_flow_info_id": 3, "graph_seq": 7, "graph_node": "netconf_data_conf",
                 "graph_node_name": "dataconf_node"
             }
            ##############################################################################################################################
            # Network Create 4 : word2vec
            ##############################################################################################################################
            ,{
                 "graph_flow_info_id": 4, "graph_seq": 1, "graph_node": "netconf_node",
                 "graph_node_name": "netconf_node"
             }
            ,{
                 "graph_flow_info_id": 4, "graph_seq": 2, "graph_node": "netconf_data",
                 "graph_node_name": "data_node"
             }
            ,{
                 "graph_flow_info_id": 4, "graph_seq": 3, "graph_node": "netconf_feed",
                 "graph_node_name": "pre_feed_text2wv_train"
             }
            ,{
                 "graph_flow_info_id": 4, "graph_seq": 4, "graph_node": "eval_node",
                 "graph_node_name": "eval_node"
             }
            ,{
                 "graph_flow_info_id": 4, "graph_seq": 5, "graph_node": "eval_data",
                 "graph_node_name": "test_data_node"
             }
            ,{
                 "graph_flow_info_id": 4, "graph_seq": 6, "graph_node": "eval_feed",
                 "graph_node_name": "pre_feed_text2wv_test"
             }
            ##############################################################################################################################
            # Network Create 5 : word2vec_frame
            ##############################################################################################################################
            ,{
                 "graph_flow_info_id": 5, "graph_seq": 1, "graph_node": "netconf_node",
                 "graph_node_name": "netconf_node"
             }
            ,{
                 "graph_flow_info_id": 5, "graph_seq": 2, "graph_node": "netconf_data",
                 "graph_node_name": "data_node"
             }
            ,{
                 "graph_flow_info_id": 5, "graph_seq": 3, "graph_node": "netconf_feed",
                 "graph_node_name": "pre_feed_fr2wv_test"
             }
            ,{
                 "graph_flow_info_id": 5, "graph_seq": 4, "graph_node": "eval_node",
                 "graph_node_name": "eval_node"
             }
            ,{
                 "graph_flow_info_id": 5, "graph_seq": 5, "graph_node": "eval_data",
                 "graph_node_name": "test_data_node"
             }
            ,{
                 "graph_flow_info_id": 5, "graph_seq": 6, "graph_node": "eval_feed",
                 "graph_node_name": "pre_feed_fr2wv_test"
             }
            ##############################################################################################################################
            # Network Create 6 : doc2vec
            ##############################################################################################################################
            ,{
                 "graph_flow_info_id": 6, "graph_seq": 1, "graph_node": "netconf_node",
                 "graph_node_name": "netconf_node"
             }
            ,{
                 "graph_flow_info_id": 6, "graph_seq": 2, "graph_node": "netconf_data",
                 "graph_node_name": "data_node"
             }
            ,{
                 "graph_flow_info_id": 6, "graph_seq": 3, "graph_node": "netconf_feed",
                 "graph_node_name": "pre_feed_text2dv_train"
             }
            ,{
                 "graph_flow_info_id": 6, "graph_seq": 4, "graph_node": "eval_node",
                 "graph_node_name": "eval_node"
             }
            ,{
                 "graph_flow_info_id": 6, "graph_seq": 5, "graph_node": "eval_data",
                 "graph_node_name": "test_data_node"
             }
            ,{
                 "graph_flow_info_id": 6, "graph_seq": 6, "graph_node": "eval_feed",
                 "graph_node_name": "pre_feed_text2dv_test"
             }
            ##############################################################################################################################
            # Network Create 7 : wcnn
            ##############################################################################################################################
            ,{
                 "graph_flow_info_id": 7, "graph_seq": 1, "graph_node": "netconf_node",
                 "graph_node_name": "netconf_node"
             }
            ,{
                 "graph_flow_info_id": 7, "graph_seq": 2, "graph_node": "netconf_data",
                 "graph_node_name": "data_node"
             }
            ,{
                 "graph_flow_info_id": 7, "graph_seq": 3, "graph_node": "netconf_feed",
                 "graph_node_name": "pre_feed_train"
             }
            ,{
                 "graph_flow_info_id": 7, "graph_seq": 4, "graph_node": "eval_node",
                 "graph_node_name": "eval_node"
             }
            ,{
                 "graph_flow_info_id": 7, "graph_seq": 5, "graph_node": "eval_data",
                 "graph_node_name": "test_data_node"
             }
            ,{
                 "graph_flow_info_id": 7, "graph_seq": 6, "graph_node": "eval_feed",
                 "graph_node_name": "pre_feed_test"
             }
            ##############################################################################################################################
            # Network Create 8 : seq2seq
            ##############################################################################################################################
            ,{
                 "graph_flow_info_id": 8, "graph_seq": 1, "graph_node": "netconf_node",
                 "graph_node_name": "netconf_node"
             }
            ,{
                 "graph_flow_info_id": 8, "graph_seq": 2, "graph_node": "netconf_data_encode",
                 "graph_node_name": "data_encode_node"
             }
            ,{
                 "graph_flow_info_id": 8, "graph_sdeq": 3, "graph_node": "netconf_data_decode",
                 "graph_node_name": "data_decode_node"
             }
            ,{
                 "graph_flow_info_id": 8, "graph_seq": 4, "graph_node": "netconf_data_merge",
                 "graph_node_name": "text_merge_node"
             }
            ,{
                 "graph_flow_info_id": 8, "graph_seq": 5, "graph_node": "netconf_feed",
                 "graph_node_name": "feed_text2seq_train"
             }
            ,{
                 "graph_flow_info_id": 8, "graph_seq": 6, "graph_node": "eval_node",
                 "graph_node_name": "eval_node"
             }
            ,{
                 "graph_flow_info_id": 8, "graph_seq": 7, "graph_node": "eval_feed",
                 "graph_node_name": "feed_text2seq_test"
             }
            ##############################################################################################################################
            # Network Create 9 : seq2seq_csv
            ##############################################################################################################################
            ,{
                 "graph_flow_info_id": 9, "graph_seq": 1, "graph_node": "netconf_node",
                 "graph_node_name": "netconf_node"
             }
            ,{
                 "graph_flow_info_id": 9, "graph_seq": 2, "graph_node": "netconf_data",
                 "graph_node_name": "data_csv_node"
             }
            ,{
                 "graph_flow_info_id": 9, "graph_seq": 3, "graph_node": "netconf_feed",
                 "graph_node_name": "feed_fr2seq"
             }
            ,{
                 "graph_flow_info_id": 9, "graph_seq": 4, "graph_node": "eval_node",
                 "graph_node_name": "eval_node"
             }
            ,{
                 "graph_flow_info_id": 9, "graph_seq": 5, "graph_node": "eval_data",
                 "graph_node_name": "evaldata"
             }
            ,{
                 "graph_flow_info_id": 9, "graph_seq": 6, "graph_node": "eval_feed",
                 "graph_node_name": "feed_fr2seq_test"
             }
            ##############################################################################################################################
            # Network Create 10 : autoencoder_img
            ##############################################################################################################################
            ,{
                 "graph_flow_info_id": 10, "graph_seq": 1, "graph_node": "netconf_node",
                 "graph_node_name": "netconf_node"
             }
            ,{
                 "graph_flow_info_id": 10, "graph_seq": 2, "graph_node": "netconf_data",
                 "graph_node_name": "datasrc"
             }
            ,{
                 "graph_flow_info_id": 10, "graph_seq": 3, "graph_node": "netconf_feed",
                 "graph_node_name": "feed_img2auto_train"
             }
            ##############################################################################################################################
            # Network Create 11 : autoencoder_csv
            ##############################################################################################################################
            ,{
                 "graph_flow_info_id": 11, "graph_seq": 1, "graph_node": "netconf_node",
                 "graph_node_name": "netconf_node"
             }
            ,{
                 "graph_flow_info_id": 11, "graph_seq": 2, "graph_node": "netconf_data",
                 "graph_node_name": "datasrc"
             }
            ,{
                 "graph_flow_info_id": 11, "graph_seq": 3, "graph_node": "netconf_feed",
                 "graph_node_name": "feed_train"
             }
            ,{
                 "graph_flow_info_id": 11, "graph_seq": 4, "graph_node": "eval_node",
                 "graph_node_name": "eval_node"
             }
            ,{
                 "graph_flow_info_id": 11, "graph_seq": 5, "graph_node": "eval_data",
                 "graph_node_name": "evaldata"
             }
            ,{
                 "graph_flow_info_id": 11, "graph_seq": 6, "graph_node": "eval_feed",
                 "graph_node_name": "feed_test"
             }
            ##############################################################################################################################
            # Network Create 12 : ML
            ##############################################################################################################################
            , {
                "graph_flow_info_id": 12, "graph_seq": 1, "graph_node": "netconf_node",
                "graph_node_name": "netconf_node"
            }
            , {
                "graph_flow_info_id": 12, "graph_seq": 2, "graph_node": "netconf_data",
                "graph_node_name": "data_node"
            }
            , {
                "graph_flow_info_id": 12, "graph_seq": 3, "graph_node": "netconf_feed",
                "graph_node_name": "pre_feed_fr2ml_train"
            }
            , {
                "graph_flow_info_id": 12, "graph_seq": 4, "graph_node": "eval_node",
                "graph_node_name": "eval_node"
            }
            , {
                "graph_flow_info_id": 12, "graph_seq": 5, "graph_node": "eval_data",
                "graph_node_name": "evaldata"
            }
            , {
                "graph_flow_info_id": 12, "graph_seq": 6, "graph_node": "eval_feed",
                "graph_node_name": "pre_feed_fr2ml_test"
            }
            , {
                "graph_flow_info_id": 12, "graph_seq": 7, "graph_node": "netconf_data_conf",
                "graph_node_name": "dataconf_node"
            }
        ]
        for conf in confs :
            WorkFlowStateMenu().put_graph_info(conf)
        return {"node_alias" : True}
    except Exception as e:
        return {"node_alias" : False}
    

def set_automl_rule() :
    """
    set automl params for default
    :return: true or false
    """
    try :
        # CNN net conf
        conf = {"auto": {
                    "netconf_node": {
                        "param": {"traincnt": {"type": "int", "option": 3, "auto": False}
                            , "epoch": {"type": "int", "option": 10, "auto": False}
                            , "batch_size": {"type": "int", "option": 50000, "auto": False}
                            , "predictcnt": {"type": "int", "option": 3, "auto": False}
                            , "predlog": {"type": "sel", "option": ["N", "T", "F", "A"], "auto": False}
                                  },
                        "config": {"num_classes": {"type": "int", "option": 1, "auto": False}
                            , "learnrate": {"type": "int", "option": None, "auto": [0.001, 0.005, 0.001]}
                            , "layeroutputs": {"type": "int", "option": None, "auto": [5, 100, 3]}
                            , "net_type": {"type": "sel", "option": ["cnn"], "auto": False}
                            , "eval_type": {"type": "sel", "option": ["category"], "auto": False}
                            , "optimizer": {"type": "sel", "option": ["AdamOptimizer", "RMSPropOptimizer"], "auto": False}
                                   }
                        , "layer1": {"active": {"type": "sel", "option": ["relu"], "auto": False},
                                     "cnnfilter": {"type": "int", "option": [3, 3], "auto": False},
                                     "cnnstride": {"type": "int", "option": [1, 1], "auto": False},
                                     "maxpoolmatrix": {"type": "int", "option": [2, 2], "auto": False},
                                     "maxpoolstride": {"type": "int", "option": [2, 2], "auto": False},
                                     "padding": {"type": "sel", "option": ["SAME", "NONE"], "auto": False},
                                     "droprate": {"type": "int", "option": None, "auto": [0.6, 1.0, 0.1]},
                                     "layercnt": {"type": "int", "option": None, "auto": [1, 6, 1]}
                                     }
                        ,
                        "out": {"active": {"type": "sel", "option": ["softmax", "relu", 'tanh', "sigmoid"], "auto": False},
                                "node_out": {"type": "int", "option": None, "auto": [600, 2000, 5]},
                                "padding": {"type": "sel", "option": ["SAME", "NONE"], "auto": False}
                                }
                        # , "labels": {"type": "list", "option": [], "auto": False}
                    },
                    "netconf_data": {
                        "type": {"type": "sel", "option": ["imgdata", "framedata", "textdata", "iobdata"], "auto": False}
                        , "preprocess": {"x_size": {"type": "int", "option": 32, "auto": False}
                            , "y_size": {"type": "int", "option": 32, "auto": False}
                            , "channel": {"type": "int", "option": 3, "auto": False}
                            , "filesize": {"type": "int", "option": 1000000, "auto": False}
                            , "yolo": {"type": "sel", "option": ["N", "Y"], "auto": False}}
                    },
                    "eval_data": {
                        "type": {"type": "sel", "option": ["imgdata", "framedata", "textdata", "iobdata"], "auto": False}
                        , "preprocess": {
                              "x_size": {"type": "int", "option": 32, "auto": False}
                            , "y_size": {"type": "int", "option": 32, "auto": False}
                            , "channel": {"type": "int", "option": 3, "auto": False}
                            , "filesize": {"type": "int", "option": 1000000, "auto": False}
                            , "yolo": {"type": "sel", "option": ["N", "Y"], "auto": False}
                        }
                    }
                },
                    "single": {
                        "netconf_node": {
                            "param": {"traincnt": 5
                                , "epoch": 10
                                , "batch_size": 50000
                                , "predictcnt": 3
                                , "predlog": "N"  # T:Ture, F:False, A:True&False, N:None
                                      },
                            "config": {"num_classes": 1,
                                       "learnrate": 0.001,
                                       "layeroutputs": 32,
                                       "net_type": "cnn",
                                       "eval_type": "category",
                                       "optimizer": "AdamOptimizer"  # RMSPropOptimizer
                                       }
                            , "layer1": {"active": "relu",
                                         "cnnfilter": [3, 3],
                                         "cnnstride": [1, 1],
                                         "maxpoolmatrix": [2, 2],
                                         "maxpoolstride": [2, 2],
                                         "padding": "SAME",
                                         "droprate": "0.8",
                                         "layercnt": 1
                                         }
                            , "layer2": {"active": "relu",
                                         "cnnfilter": [3, 3],
                                         "cnnstride": [1, 1],
                                         "maxpoolmatrix": [1, 1],
                                         "maxpoolstride": [2, 2],
                                         "padding": "SAME",
                                         "droprate": "0.8",
                                         "layercnt": 1
                                         }
                            , "out": {"active": "softmax",
                                      "node_out": 625,
                                      "padding": "SAME"
                                      }
                            # , "labels": []
                        },
                        "netconf_data": {
                                  "type": ["imgdata"]
                                , "preprocess": {"x_size": 32,
                                                   "y_size": 32,
                                                   "channel":3,
                                                   "filesize": 1000000,
                                                   "yolo": "n"}
                        },
                        "eval_data": {
                                  "type": ["imgdata"]
                                , "preprocess": {"x_size": 32,
                                                   "y_size": 32,
                                                   "channel":3,
                                                   "filesize": 1000000,
                                                   "yolo": "n"}
                        }
                    }
                }

        AutoMlRule().set_graph_type_list('cnn', conf)

        # set netconf for resnet
        conf = {
            "auto": {
                "netconf_node": {
                    "param": {"traincnt": {"type": "int", "option": 5, "auto": False}
                        , "epoch": {"type": "int", "option": 5, "auto": False}
                        , "batch_size": {"type": "int", "option": None, "auto": [60, 300, 10]}
                        , "predictcnt": {"type": "int", "option": 2, "auto": False}
                        , "predictlog": {"type": "sel", "option": ["N", "T", "F", "A"], "auto": False}
                        , "augmentation": {"type": "sel", "option": ["N", "Y"], "auto": False}
                              }
                    , "config": {"layeroutputs": {"type": "sel", "option": [18,34,50,101,152], "auto": False} #[18,34,50,101,152]
                        , "eval_type": {"type": "sel", "option": ["category"], "auto": False}
                        , "optimizer": {"type": "sel", "option": ["adam", "rmsp"], "auto": False}
                        # , "pre_train": {"type": "sel", "option": ["Y", "N"], "auto": False}
                                 }
                    , "labels": {"type": "str", "option": [], "auto": False}
                }
                , "netconf_data": {
                    "type": {"type": "sel", "option": ["imgdata"], "auto": False} # ["imgdata", "framedata", "textdata", "iobdata"]
                    , "preprocess": {"x_size": {"type": "int", "option": 32, "auto": False}
                        , "y_size": {"type": "int", "option": 32, "auto": False}
                        , "channel": {"type": "int", "option": 3, "auto": False}
                        , "filesize": {"type": "int", "option": 1000000, "auto": False}
                        }
                }
                , "eval_data": {
                    "type": {"type": "sel", "option": ["imgdata"], "auto": False}# ["imgdata", "framedata", "textdata", "iobdata"]
                    , "preprocess": {"x_size": {"type": "int", "option": 32, "auto": False}
                        , "y_size": {"type": "int", "option": 32, "auto": False}
                        , "channel": {"type": "int", "option": 3, "auto": False}
                        , "filesize": {"type": "int", "option": 1000000, "auto": False}
                                     }
                }
            },
            "single": {
                "netconf_node": {
                    "param": {"traincnt": 5
                        , "epoch": 5
                        , "batch_size": 80
                        , "predictcnt": 2
                        , "predictlog": "N"  # T:Ture, F:False, A:True&False, TT:Ture, FF:False, AA:True&False, N:None
                        , "augmentation": "N"
                              },
                    "config": {"layeroutputs": 18,  # 18, 34, 50, 101, 152, 200
                               "optimizer": "adam",  #
                               "eval_type": "category",
                               # "pre_train": "Y"
                               }
                    # , "labels": []
                }
                , "netconf_data": {
                    "preprocess": {"x_size": 32,
                                   "y_size": 32,
                                   "channel": 3,
                                   "filesize": 1000000
                                   }
                }
                , "eval_data": {
                    "preprocess": {"x_size": 32,
                                   "y_size": 32,
                                   "channel": 3,
                                   "filesize": 1000000
                                   }
                }

            }
        }
        AutoMlRule().set_graph_type_list('resnet', conf)

        # set netconf for inceptionv4
        conf = {
            "auto": {
                "netconf_node": {
                    "param": {"traincnt": {"type": "int", "option": 5, "auto": False}
                        , "epoch": {"type": "int", "option": 5, "auto": False}
                        , "batch_size": {"type": "int", "option": None, "auto": [60, 300, 10]}
                        , "predictcnt": {"type": "int", "option": 2, "auto": False}
                        , "predictlog": {"type": "sel", "option": ["N", "T", "F", "A"], "auto": False}
                        , "augmentation": {"type": "sel", "option": ["N", "Y"], "auto": False}
                        , "fit_size": {"type": "int", "option": 1000, "auto": False}
                              }
                    , "config": {"eval_type": {"type": "sel", "option": ["category"], "auto": False}
                                , "optimizer": {"type": "sel", "option": [], "auto": ["adam", "sgd", "rmsprop", "adagrad", "adadelta", "adamax", "nadam"]}
                                # , "pre_train": {"type": "sel", "option": ["Y", "N"], "auto": False}
                                 }
                    , "labels": {"type": "str", "option": [], "auto": False}
                }
                , "netconf_data": {
                    "type": {"type": "sel", "option": ["imgdata"], "auto": False} #["imgdata", "framedata", "textdata", "iobdata"]
                    , "preprocess": {"x_size": {"type": "int", "option": 299, "auto": False}
                        , "y_size": {"type": "int", "option": 299, "auto": False}
                        , "channel": {"type": "int", "option": 3, "auto": False}
                        , "filesize": {"type": "int", "option": 1000000, "auto": False}
                                     }
                }
                , "eval_data": {
                    "type": {"type": "sel", "option": ["imgdata"], "auto": False} #["imgdata", "framedata", "textdata", "iobdata"]
                    , "preprocess": {"x_size": {"type": "int", "option": 299, "auto": False}
                        , "y_size": {"type": "int", "option": 299, "auto": False}
                        , "channel": {"type": "int", "option": 3, "auto": False}
                        , "filesize": {"type": "int", "option": 1000000, "auto": False}
                                     }
                }
            },
            "single": {
                "netconf_node": {
                    "param": {"traincnt": 5
                        , "epoch": 5
                        , "batch_size": 80
                        , "predictcnt": 2
                        , "predictlog": "N"  # T:Ture, F:False, A:True&False, TT:Ture, FF:False, AA:True&False, N:None
                        , "augmentation": "N"
                        , "fit_size": 1000
                              },
                    "config": {"optimizer": "adam",  #
                               "eval_type": "category",
                               # "pre_train":"Y"
                               }
                    # , "labels": []
                }
                , "netconf_data": {
                    "preprocess": {"x_size": 299,
                                   "y_size": 299,
                                   "channel": 3,
                                   "filesize": 1000000
                                   }
                }
                , "eval_data": {
                    "preprocess": {"x_size": 299,
                                   "y_size": 299,
                                   "channel": 3,
                                   "filesize": 1000000
                                   }
                }

            }
        }
        AutoMlRule().set_graph_type_list('inceptionv4', conf)

        # # set netconf for inception_resnet_v2
        # conf = {
        #     "auto": {
        #         "netconf_node": {
        #             "param": {"traincnt": {"type": "int", "option": 5, "auto": False}
        #                 , "epoch": {"type": "int", "option": 5, "auto": False}
        #                 , "batch_size": {"type": "int", "option": None, "auto": [60, 300, 10]}
        #                 , "predictcnt": {"type": "int", "option": 2, "auto": False}
        #                 , "predictlog": {"type": "sel", "option": ["N", "T", "F", "A"], "auto": False}
        #                 , "augmentation": {"type": "sel", "option": ["N", "Y"], "auto": False}
        #                 , "fit_size": {"type": "int", "option": 1000, "auto": False}
        #                       }
        #             , "config": {"eval_type": {"type": "sel", "option": ["category"], "auto": False}
        #                 , "optimizer": {"type": "sel", "option": ["adam", "rmsp"], "auto": False}
        #                 , "pre_train": {"type": "sel", "option": ["Y","N"], "auto": False}
        #                          }
        #             , "labels": {"type": "str", "option": [], "auto": False}
        #         }
        #         , "netconf_data": {
        #             "type": {"type": "sel", "option": ["imgdata"], "auto": False}
        #         # ["imgdata", "framedata", "textdata", "iobdata"]
        #             , "preprocess": {"x_size": {"type": "int", "option": 299, "auto": False}
        #                 , "y_size": {"type": "int", "option": 299, "auto": False}
        #                 , "channel": {"type": "int", "option": 3, "auto": False}
        #                 , "filesize": {"type": "int", "option": 1000000, "auto": False}
        #                              }
        #         }
        #         , "eval_data": {
        #             "type": {"type": "sel", "option": ["imgdata"], "auto": False}
        #         # ["imgdata", "framedata", "textdata", "iobdata"]
        #             , "preprocess": {"x_size": {"type": "int", "option": 299, "auto": False}
        #                 , "y_size": {"type": "int", "option": 299, "auto": False}
        #                 , "channel": {"type": "int", "option": 3, "auto": False}
        #                 , "filesize": {"type": "int", "option": 1000000, "auto": False}
        #                              }
        #         }
        #     },
        #     "single": {
        #         "netconf_node": {
        #             "param": {"traincnt": 5
        #                 , "epoch": 5
        #                 , "batch_size": 80
        #                 , "predictcnt": 2
        #                 , "predictlog": "N"  # T:Ture, F:False, A:True&False, TT:Ture, FF:False, AA:True&False, N:None
        #                 , "augmentation": "N"
        #                 , "fit_size": 1000
        #                       },
        #             "config": {"optimizer": "adam",  #
        #                        "eval_type": "category",
        #                        "pre_train": "Y"
        #                        }
        #             # , "labels": []
        #         }
        #         , "netconf_data": {
        #             "preprocess": {"x_size": 299,
        #                            "y_size": 299,
        #                            "channel": 3,
        #                            "filesize": 1000000
        #                            }
        #         }
        #         , "eval_data": {
        #             "preprocess": {"x_size": 299,
        #                                "y_size": 299,
        #                            "channel": 3,
        #                            "filesize": 1000000
        #                            }
        #         }
        #
        #     }
        # }
        # AutoMlRule().set_graph_type_list('inception_resnet_v2', conf)

        # set netconf for wdnn
        conf = {
            "auto": {
                "data_node":
                    {
                        "type": {"type": "sel", "option": ["csv"], "auto": False}
                        , "preprocess": {"type": "sel",
                                         "option": ["null"],
                                         "auto": False}
                        , "source_sql": {"type": "sel", "option": ["all"], "auto": False}
                        , "store_path": {"type": "str", "option": None, "auto": False}
                        , "source_path": {"type": "str", "option": None, "auto": False}
                        , "source_type": {"type": "sel", "option": ["local"], "auto": False}
                        , "predict_path": {"type": "str", "option": None, "auto": False}
                        , "source_server": {"type": "sel", "option": ["local"], "auto": False}
                        , "drop_duplicate": {"type": "sel", "option": ["False"], "auto": False}
                        , "multi_node_flag": {"type": "sel", "option": ["False"], "auto": False}
                        , "max_sentence_len": {"type": "int", "option": 0, "auto": False}
                        , "source_parse": {"type": "str", "option": "raw", "auto": False}
                    }
                , "dataconf_node":
                    {
                        "label": {"type": "str", "option": "LABEL", "auto": False}
                        , "Transformations": {"type": "str", "option": {}, "auto": False}
                        , "cross_cell": {"type": "str", "option": {}, "auto": False}
                        , "cell_feature": {"type": "str", "option": {}, "auto": False}
                        , "extend_cell_feature": {"type": "str", "option": {}, "auto": False}
                        , "cell_feature_unique": {"type": "str", "option": [], "auto": False}
                        , "label_values": {"type": "str", "option": [], "auto": False}
                        , "label_type": {"type": "sel", "option": ["CATEGORYCAL"], "auto": False}
                    }
                , "netconf_node":
                    {
                        "model_path": {"type": "str", "option": None, "auto": False}
                        , "hidden_layers": {"type": "int", "option": None, "auto": [[1, 4, 1], [1, 100, 1]]}
                        , "activation_function": {"type": "sel", "option": ["relu"], "auto": False}
                        , "batch_size": {"type": "int", "option": 1000, "auto": False}
                        , "epoch": {"type": "int", "option": None, "auto": [1, 10, 1]}
                        , "model_type": {"type": "sel", "option": ["category"], "auto": False}
                        , "auto_demension": {"type": "sel", "option": ["False"], "auto": False}
                        , "train": {"type": "sel", "option": ["True"], "auto": False}
                        , "optimizer_type": {"type": "str", "option": [] , "auto": ["GD","Adagrad","Adam","PGD","RMS"]}
                        , "learning_rates": {"type": "int", "option": None, "auto": [0.0001, 0.1, 0.001]}
                        #, "learning_rates": {"type": "int", "option": None, "auto": [[1, 4, 1], [1, 100, 1]]}
                        #optimizer_type
                        #learning_rates
                    }
                , "evaldata":
                    {
                        "type": {"type": "sel", "option": ["csv"], "auto": False}
                        , "preprocess": {"type": "sel",
                                         "option": ["null"],
                                         "auto": False}
                        , "source_sql": {"type": "sel", "option": ["all"], "auto": False}
                        , "store_path": {"type": "str", "option": None, "auto": False}
                        , "source_path": {"type": "str", "option": None, "auto": False}
                        , "source_type": {"type": "sel", "option": ["local"], "auto": False}
                        , "predict_path": {"type": "str", "option": None, "auto": False}
                        , "source_server": {"type": "sel", "option": ["local"], "auto": False}
                        , "drop_duplicate": {"type": "sel", "option": ["False"], "auto": False}
                        , "multi_node_flag": {"type": "sel", "option": ["False"], "auto": False}
                        , "max_sentence_len": {"type": "int", "option": 0, "auto": False}
                        , "source_parse": {"type": "str", "option": "raw", "auto": False}
                    }
                , "eval_node":
                    {
                        "type": {"type": "sel", "option": ["category"], "auto": False}
                    }
            }, "single": {
                "data_node":
                    {
                        "type": "csv",
                        "source_server": "local",
                        "source_sql": "all",
                        "source_path": None,
                        "multi_node_flag": False,
                        "preprocess": "null",
                        "store_path": None,
                            "source_type": "local"

                    }
                , "dataconf_node":
                    {
                        "label": "LABEL",
                        "Transformations": {},
                        "cross_cell": {},
                        "cell_feature": {},
                        "extend_cell_feature": {},
                        "cell_feature_unique":{},
                        "label_values": [],
                        "label_type": "CATEGORICAL"
                    }
                , "netconf_node":
                    {
                        "model_path": None,
                        "hidden_layers": [50, 50, 50, 30],
                        "activation_function": "Relu",
                        "batch_size": 500,
                        "epoch": 500,
                        "model_type": "category",
                        "train": True,
                        "optimizer_type": "GD",
                        "learning_rates": 0.01
                    }
                , "evaldata":
                    {
                        "type": "csv",
                        "source_server": "local",
                        "source_sql": "all",
                        "source_path": None,
                        "multi_node_flag": False,
                        "preprocess": "null",
                        "store_path": None,
                        "source_type": "local"

                    }
                , "eval_node":
                    {
                        "type": "category",
                    }

            }
        }
        AutoMlRule().set_graph_type_list('wdnn', conf)

        # set netconf for ML
        conf = {
            "auto": {
                "data_node":
                    {
                        "type": {"type": "sel", "option": ["csv"], "auto": False}
                        , "preprocess": {"type": "sel",
                                         "option": ["null"],
                                         "auto": False}
                        , "source_sql": {"type": "sel", "option": ["all"], "auto": False}
                        , "store_path": {"type": "str", "option": None, "auto": False}
                        , "source_path": {"type": "str", "option": None, "auto": False}
                        , "source_type": {"type": "sel", "option": ["local"], "auto": False}
                        , "predict_path": {"type": "str", "option": None, "auto": False}
                        , "source_server": {"type": "sel", "option": ["local"], "auto": False}
                        , "drop_duplicate": {"type": "sel", "option": ["False"], "auto": False}
                        , "multi_node_flag": {"type": "sel", "option": ["False"], "auto": False}
                        , "max_sentence_len": {"type": "int", "option": 0, "auto": False}
                        , "source_parse": {"type": "str", "option": "raw", "auto": False}
                    }
                , "dataconf_node":
                    {
                        "label": {"type": "str", "option": "LABEL", "auto": False}
                        , "Transformations": {"type": "str", "option": {}, "auto": False}
                        , "cross_cell": {"type": "str", "option": {}, "auto": False}
                        , "cell_feature": {"type": "str", "option": {}, "auto": False}
                        , "extend_cell_feature": {"type": "str", "option": {}, "auto": False}
                        , "cell_feature_unique": {"type": "str", "option": [], "auto": False}
                        , "label_values": {"type": "str", "option": [], "auto": False}
                        , "label_type": {"type": "sel", "option": ["CATEGORYCAL"], "auto": False}
                    }
                , "netconf_node":
                    {
                        "model_path": {"type": "str", "option": None, "auto": False}
                        , "hidden_layers": {"type": "int", "option": None, "auto": [[1, 4, 1], [1, 100, 1]]}
                        , "activation_function": {"type": "sel", "option": ["relu"], "auto": False}
                        , "batch_size": {"type": "int", "option": 1000, "auto": False}
                        , "epoch": {"type": "int", "option": None, "auto": [1, 10, 1]}
                        , "model_type": {"type": "sel", "option": ["category"], "auto": False}
                        , "auto_demension": {"type": "sel", "option": ["False"], "auto": False}
                        , "train": {"type": "sel", "option": ["True"], "auto": False}
                        , "optimizer_type": {"type": "str", "option": [], "auto": ["GD", "Adagrad", "Adam", "PGD", "RMS"]}
                        , "learning_rates": {"type": "int", "option": None, "auto": [0.0001, 0.1, 0.001]}
                    }
                , "evaldata":
                    {
                        "type": {"type": "sel", "option": ["csv"], "auto": False}
                        , "preprocess": {"type": "sel",
                                         "option": ["null"],
                                         "auto": False}
                        , "source_sql": {"type": "sel", "option": ["all"], "auto": False}
                        , "store_path": {"type": "str", "option": None, "auto": False}
                        , "source_path": {"type": "str", "option": None, "auto": False}
                        , "source_type": {"type": "sel", "option": ["local"], "auto": False}
                        , "predict_path": {"type": "str", "option": None, "auto": False}
                        , "source_server": {"type": "sel", "option": ["local"], "auto": False}
                        , "drop_duplicate": {"type": "sel", "option": ["False"], "auto": False}
                        , "multi_node_flag": {"type": "sel", "option": ["False"], "auto": False}
                        , "max_sentence_len": {"type": "int", "option": 0, "auto": False}
                        , "source_parse": {"type": "str", "option": "raw", "auto": False}
                    }
                , "eval_node":
                    {
                        "type": {"type": "sel", "option": ["category"], "auto": False}
                    }
            }, "single": {
                "data_node":
                    {
                        "type": "csv",
                        "source_server": "local",
                        "source_sql": "all",
                        "source_path": None,
                        "multi_node_flag": False,
                        "preprocess": "null",
                        "store_path": None,
                        "source_type": "local"

                    }
                , "dataconf_node":
                    {
                        "label": "LABEL",
                        "Transformations": {},
                        "cross_cell": {},
                        "cell_feature": {},
                        "extend_cell_feature": {},
                        "cell_feature_unique": {},
                        "label_values": [],
                        "label_type": "CATEGORICAL"
                    }
                , "netconf_node":
                    {
                        "model_path": None,
                        "ml_class": "DecisionTreeClassifier",
                        "config": {"max_depth": 5},
                        "model_type" : "category"
                    }
                , "evaldata":
                    {
                        "type": "csv",
                        "source_server": "local",
                        "source_sql": "all",
                        "source_path": None,
                        "multi_node_flag": False,
                        "preprocess": "null",
                        "store_path": None,
                        "source_type": "local"

                    }
                , "eval_node":
                    {
                        "type": "category",
                    }

            }
        }
        AutoMlRule().set_graph_type_list('ml', conf)

        # set auton netconf for dnn
        conf = {
            "auto": {
                "data_node":
                    {
                        "type": {"type": "sel", "option": ["csv"], "auto": False}
                        , "preprocess": {"type": "sel",
                                         "option": ["null"],
                                         "auto": False}
                        , "source_sql": {"type": "sel", "option": ["all"], "auto": False}
                        , "store_path": {"type": "str", "option": None, "auto": False}
                        , "source_path": {"type": "str", "option": None, "auto": False}
                        , "source_type": {"type": "sel", "option": ["local"], "auto": False}
                        , "predict_path": {"type": "str", "option": None, "auto": False}
                        , "source_server": {"type": "sel", "option": ["local"], "auto": False}
                        , "drop_duplicate": {"type": "sel", "option": ["False"], "auto": False}
                        , "multi_node_flag": {"type": "sel", "option": ["False"], "auto": False}
                        , "max_sentence_len": {"type": "int", "option": 0, "auto": False}
                        , "source_parse": {"type": "str", "option": "raw", "auto": False}
                    }
                , "dataconf_node":
                    {
                        "label": {"type": "str", "option": "LABEL", "auto": False}
                        , "Transformations": {"type": "str", "option": {}, "auto": False}
                        , "cross_cell": {"type": "str", "option": {}, "auto": False}
                        , "cell_feature": {"type": "str", "option": {}, "auto": False}
                        , "extend_cell_feature": {"type": "str", "option": {}, "auto": False}
                        , "cell_feature_unique": {"type": "str", "option": [], "auto": False}
                        , "label_values": {"type": "str", "option": [], "auto": False}
                        , "label_type": {"type": "sel", "option": ["CATEGORYCAL"], "auto": False}
                    }
                , "netconf_node":
                    {
                        "model_path": {"type": "str", "option": None, "auto": False}
                        , "hidden_layers": {"type": "int", "option": None, "auto": [[1, 4, 1], [1, 100, 1]]}
                        , "activation_function": {"type": "sel", "option": ["relu"], "auto": False}
                        , "batch_size": {"type": "int", "option": 1000, "auto": False}
                        , "epoch": {"type": "int", "option": None, "auto": [1, 10, 1]}
                        , "model_type": {"type": "str", "option": "deep", "auto": False}
                        , "auto_demension": {"type": "sel", "option": ["False"], "auto": False}
                        , "train": {"type": "sel", "option": ["True"], "auto": False}
                        , "optimizer_type": {"type": "str", "option": [],
                                             "auto": ["GD", "Adagrad", "Adam", "PGD", "RMS"]}
                        , "learning_rates": {"type": "int", "option": None, "auto": [0.0001, 0.1, 0.001]}
                    }
                , "evaldata":
                    {
                        "type": {"type": "sel", "option": ["csv"], "auto": False}
                        , "preprocess": {"type": "sel",
                                         "option": ["null"],
                                         "auto": False}
                        , "source_sql": {"type": "sel", "option": ["all"], "auto": False}
                        , "store_path": {"type": "str", "option": None, "auto": False}
                        , "source_path": {"type": "str", "option": None, "auto": False}
                        , "source_type": {"type": "sel", "option": ["local"], "auto": False}
                        , "predict_path": {"type": "str", "option": None, "auto": False}
                        , "source_server": {"type": "sel", "option": ["local"], "auto": False}
                        , "drop_duplicate": {"type": "sel", "option": ["False"], "auto": False}
                        , "multi_node_flag": {"type": "sel", "option": ["False"], "auto": False}
                        , "max_sentence_len": {"type": "int", "option": 0, "auto": False}
                        , "source_parse": {"type": "str", "option": "raw", "auto": False}
                    }
                , "eval_node":
                    {
                        "type": {"type": "sel", "option": ["category"   ], "auto": False}
                    }
            }, "single": {
                "data_node":
                    {
                        "type": "csv",
                        "source_server": "local",
                        "source_sql": "all",
                        "source_path": None,
                        "multi_node_flag": False,
                        "preprocess": "null",
                        "store_path": None,
                        "source_type": "local"

                    }
                , "dataconf_node":
                    {
                        "label": "LABEL",
                        "Transformations": {},
                        "cross_cell": {},
                        "cell_feature": {},
                        "extend_cell_feature": {},
                        "cell_feature_unique": {},
                        "label_values": [],
                        "label_type": "CATEGORICAL"
                    }
                , "netconf_node":
                    {
                        "model_path": "test",
                        "hidden_layers": [50, 50, 50, 30],
                        "activation_function": "Relu",
                        "batch_size": 500,
                        "epoch": 500,
                        "model_type": "category",
                        "train": True,
                        "optimizer_type": "GD",
                        "learning_rates": 0.01
                    }
                , "evaldata":
                    {
                        "type": "csv",
                        "source_server": "local",
                        "source_sql": "all",
                        "source_path": None,
                        "multi_node_flag": False,
                        "preprocess": "null",
                        "store_path": None,
                        "source_type": "local"

                    }
                , "eval_node":
                    {
                        "type": "category",
                    }
            }
        }
        AutoMlRule().set_graph_type_list('dnn', conf)

        # set single netconf for charcnn
        conf = {

            "auto": {
                "data_node":
                    {
                        "source_type": {"type": "sel", "option": ['local'], "auto": False},
                        "type": {"type": "sel", "option": ['csv'], "auto": False},
                        "source_server": {"type": "sel", "option": ["local"], "auto": False},
                        "source_sql": {"type": "sel", "option": ["all"], "auto": False},
                        "preprocess": {"type": "sel", "option": ["none"], "auto": False},
                    },
                "test_data_node":
                    {
                        "source_type": {"type": "sel", "option": ['local'], "auto": False},
                        "type": {"type": "sel", "option": ['csv'], "auto": False},
                        "source_server": {"type": "sel", "option": ["local"], "auto": False},
                        "source_sql": {"type": "sel", "option": ["all"], "auto": False},
                        "preprocess": {"type": "sel", "option": ["none"], "auto": False},
                    },
                "netconf_node":
                    {
                        "param": {"epoch": {"type": "int", "option": None, "auto": [200, 200, 1]}
                            , "traincnt": {"type": "int", "option": None, "auto": [1, 1, 1]}
                            , "batch_size": {"type": "int", "option": None, "auto": [64, 64, 10]}
                            , "predictcnt": {"type": "int", "option": None, "auto": [10, 10, 10]}
                                  }
                        , "config": {"num_classes": {"type": "int", "option": 6, "auto": False}
                        , "learnrate": {"type": "int", "option": None, "auto": [0.001, 0.001, 0.001]}
                        , "eval_type": {"type": "sel", "option": ["category"], "auto": False}
                        , "optimizer": {"type": "sel", "option": ["AdamOptimizer"], "auto": False}
                                     }
                        , "layers": {"active": {"type": "sel", "option": ["relu"], "auto": False},
                                     "cnnfilter": {"type": "int", "option": [2, 3, 4, 2, 3, 4,5,2, 3, 4, 2, 3, 4,5,2, 3, 4, 2, 3, 4,5], "auto": False},
                                     "droprate": {"type": "int", "option": None, "auto": [0.5, 0.5, 0.1]}
                                     }
                        , "out": {
                        "active": {"type": "sel", "option": ["softmax"], "auto": False},
                        "padding": {"type": "sel", "option": ["SAME"], "auto": False}
                    }
                        , "labels": {"type": "str", "option": [], "auto": False}
                    },
                "pre_feed_test":
                    {
                        "encode_column": {"type": "str", "option": 'encode', "auto": False},
                        "decode_column": {"type": "str", "option": 'decode', "auto": False},
                        "channel": {"type": "sel", "option": 1, "auto": False},
                        "encode_len": {"type": "int", "option": 10, "auto": False},
                        "preprocess": {"type": "sel", "option": ['none'], "auto": False},
                        "vocab_size": {"type": "int", "option": 100, "auto": False},
                        "char_encode": {"type": "sel", "option": False, "auto": [0, 1, 1]},
                        "char_max_len": {"type": "int", "option": 5, "auto": False},
                        "lable_size": {"type": "int", "option": 15, "auto": False},
                        "embed_type": {"type": "sel", "option": ["onehot"], "auto": False},
                    },
                "pre_feed_train":
                    {
                        "encode_column": {"type": "str", "option": 'encode', "auto": False},
                        "decode_column": {"type": "str", "option": 'decode', "auto": False},
                        "channel": {"type": "sel", "option": 1, "auto": False},
                        "encode_len": {"type": "int", "option": 10, "auto": False},
                        "preprocess": {"type": "sel", "option": ['none', 'mecab'], "auto": False},
                        "vocab_size": {"type": "int", "option": 100, "auto": False},
                        "char_encode": {"type": "sel", "option": False, "auto": [0, 1, 1]},
                        "char_max_len": {"type": "int", "option": 5, "auto": False},
                        "lable_size": {"type": "int", "option": 15, "auto": False},
                        "embed_type": {"type": "sel", "option": ["onehot"], "auto": False},
                    },
                "eval_node":
                    {
                        "type": {"type": "sel", "option": ["category"], "auto": False}
                    }
            },
            "single": {
                "data_node":
                    {
                        "source_type": "local",
                        "type": "csv",
                        "source_server": "local",
                        "source_sql": "all",
                        "preprocess": "none",
                    },
                "test_data_node":
                    {
                        "source_type": "local",
                        "type": "csv",
                        "source_server": "local",
                        "source_sql": "all",
                        "preprocess": "none",
                    },
                "netconf_node":
                    {
                        "param": {"epoch": 200
                            , "traincnt": 1
                            , "batch_size": 64
                            , "predictcnt": 10
                                  }
                        , "config": { "num_classes": 6
                                    , "learnrate": 0.001
                                    , "eval_type": "category"
                                    , "optimizer": "AdamOptimizer"
                        }
                        , "layers": {
                            "active": "relu"
                            , "cnnfilter": [2, 3, 4, 2, 3, 4,5,2, 3, 4, 2, 3, 4,5,2, 3, 4, 2, 3, 4, 5]
                            , "droprate": "0.5"
                                     }
                , "out": {
                    "active": "softmax",
                         "padding": "SAME"
                         }
                    , "labels": []
                },
                "pre_feed_test":
                    {
                        "encode_column": 'encode',
                        "decode_column": 'decode',
                        "channel": 1,
                        "encode_len": 15,
                        "preprocess": "",
                        "vocab_size": 100,
                        "char_encode": False,
                        "char_max_len": 5,
                        "lable_size": 6,
                        "embed_type": "onehot",
                    },
                "pre_feed_train":
                    {
                        "encode_column": 'encode',
                        "decode_column": 'decode',
                        "channel": 1,
                        "encode_len": 15,
                        "preprocess": "",
                        "vocab_size": 100,
                        "char_encode": False,
                        "char_max_len": 5,
                        "lable_size": 6,
                        "embed_type": "onehot",
                    },
                "eval_node":
                    {
                        "type": "category"
                    }
            }
        }
        AutoMlRule().set_graph_type_list('wcnn', conf)

        # set single netconf for seq2seq_csv
        conf = {

            "auto": {
                "data_node":
                    {
                        "source_type": {"type": "sel", "option": ['local'], "auto": False},
                        "type": {"type": "sel", "option": ['csv'], "auto": False},
                        "source_server": {"type": "sel", "option": ["local"], "auto": False},
                        "source_sql": {"type": "sel", "option": ["all"], "auto": False},
                        "preprocess": {"type": "sel", "option": ["none"], "auto": False},
                    },
                "test_data_node":
                    {
                        "source_type": {"type": "sel", "option": ['local'], "auto": False},
                        "type": {"type": "sel", "option": ['csv'], "auto": False},
                        "source_server": {"type": "sel", "option": ["local"], "auto": False},
                        "source_sql": {"type": "sel", "option": ["all"], "auto": False},
                        "preprocess": {"type": "sel", "option": ["none"], "auto": False},
                    },
                "netconf_node":
                    {
                        "encode_len": {"type": "int", "option": 10, "auto": False},
                        "encode_len": {"type": "int", "option": 10, "auto": False},
                        "encoder_depth": {"type": "int", "option": 2, "auto": False},
                        "decoder_depth": {"type": "int", "option": 2, "auto": False},
                        "cell_type": {"type": "str", "option": 'lstm', "auto": False},
                        "cell_size": {"type": "int", "option": 500, "auto": False},
                        "drop_out": {"type": "int", "option": 0.8, "auto": False},
                        "word_embed_type": {"type": "str", "option": 'onehot', "auto": False},
                        "word_embed_id": {"type": "str", "option": '', "auto": False},
                        "vocab_size": {"type": "int", "option": 100, "auto": False},
                        "batch_size": {"type": "int", "option": 5, "auto": False},
                        "iter": {"type": "int", "option": 100, "auto": False},
                        "early_stop": {"type": "int", "option": 0.9, "auto": False},
                        "learnrate": {"type": "int", "option": None, "auto": [0.001, 0.001, 0.001]},
            },
                "pre_feed_test":
                    {
                        "encode_column": {"type": "str", "option": 'encode', "auto": False},
                        "decode_column": {"type": "str", "option": 'decode', "auto": False},
                        "encode_len": {"type": "int", "option": 10, "auto": False},
                        "dncode_len": {"type": "int", "option": 10, "auto": False},
                        "preprocess": {"type": "sel", "option": ['none', 'mecab'], "auto": False},
                    },
                "pre_feed_train":
                    {
                        "encode_column": {"type": "str", "option": 'encode', "auto": False},
                        "decode_column": {"type": "str", "option": 'decode', "auto": False},
                        "encode_len": {"type": "int", "option": 10, "auto": False},
                        "dncode_len": {"type": "int", "option": 10, "auto": False},
                        "preprocess": {"type": "sel", "option": ['none', 'mecab'], "auto": False},
                    },
                "eval_node":
                    {
                        "type": {"type": "sel", "option": ["seq2seq"], "auto": False}
                    }
            },
            "single": {
                "data_node":
                    {
                        "source_type": "local",
                        "type": "csv",
                        "source_server": "local",
                        "source_sql": "all",
                        "preprocess": "none",
                    },
                "test_data_node":
                    {
                        "source_type": "local",
                        "type": "csv",
                        "source_server": "local",
                        "source_sql": "all",
                        "preprocess": "none",
                    },
                "netconf_node":
                    {
                        "encode_len": 10,
                        "decode_len": 10,
                        "encoder_depth" : 2,
                        "decoder_depth" : 2,
                        "cell_type" : "lstm",
                        "cell_size" : 500,
                        "drop_out" : 0.8,
                        "word_embed_type" : "onehot",
                        "word_embed_id" : "",
                        "vocab_size" : 100,
                        "batch_size" : 5,
                        "iter" : 100,
                        "early_stop" : 0.9,
                        "learning_rate" : 0.001,
                    },
                "pre_feed_test":
                    {
                        "encode_column": 'encode',
                        "decode_column": 'decode',
                        "encode_len": 10,
                        "decode_len": 10,
                        "preprocess": "mecab",
                    },
                "pre_feed_train":
                    {
                        "encode_column": 'encode',
                        "decode_column": 'decode',
                        "encode_len": 10,
                        "decode_len": 10,
                        "preprocess": "mecab",
                    },
                "eval_node":
                    {
                        "type": "seq2seq"
                    }
            }
        }
        AutoMlRule().set_graph_type_list('seq2seq_csv', conf)

        # set single netconf for ngram_mro
        conf = {
            "auto": {
                "netconf_node":
                    {
                        "standard": {"type": "int", "option": None, "auto": [0.90, 0.99, 0.01]}
                    }
            }, "single": {
                "netconf_node":
                    {
                        'standard': 0.95
                    }
            }
        }
        AutoMlRule().set_graph_type_list('ngram_mro', conf)

        # # not yet implemented
        # AutoMlRule().set_graph_type_list('wdnn_keras', {})
        # AutoMlRule().set_graph_type_list('word2vec', {})
        # AutoMlRule().set_graph_type_list('word2vec_frame', {})
        # AutoMlRule().set_graph_type_list('doc2vec', {})
        # AutoMlRule().set_graph_type_list('seq2seq', {})
        # AutoMlRule().set_graph_type_list('seq2seq_csv', {})
        # AutoMlRule().set_graph_type_list('autoencoder_img', {})
        # AutoMlRule().set_graph_type_list('autoencoder_csv', {})
        # AutoMlRule().set_graph_type_list('bilstmcrf_iob', {})
        # AutoMlRule().set_graph_type_list('fasttext_txt', {})
        # AutoMlRule().set_graph_type_list('dnn_keras', {})
        # AutoMlRule().set_graph_type_list('ml', {})

        return {"automl_netconf" : True}
    except Exception as e:
        return {"automl_netconf" : False}


def set_automl_rule_etc():
    """
    Set automl extra info
    """
    try:
        # set network description
        conf = {
            "cnn" : "CNN (convolutional neural network)은 딥러닝의 한 종류로 앞의 컨볼루셔널 계층을 통해서 입력 받은 특징(Feature)를 추출하게 되고, 이렇게 추출된 특징을 기반으로 기존의 뉴럴 네트워크를 이용하여 분류를 해내게 된다."
            ,"resnet" : "망을 100 layer 이상으로 깊게하면서, 깊이에 따른 학습효과를 얻을 수 있는 Residual Learning을 적용한 network"
            ,"wdnn": "기존에 기억된 결과로만 예측하는 와이드모델과 너무 일반화가 되서 엉뚱한 결과가 나올 수 있는 딥모델의 문제를 해결하기 위해 두 모델을 합친 Wide & Deep 모델"
            ,"wdnn_keras": "wdnn_keras Network Description"
            ,"word2vec": "word2vec Network Description"
            ,"word2vec_frame" : "word2vec_frame Network Description"
            ,"doc2vec" : "doc2vec Network Description"
            ,"wcnn" : "이미지 인식에 쓰이는 CNN을 Word단위로 Classification을 하기 위한 wcnn"
            ,"seq2seq" : "seq2seq Network Description"
            ,"seq2seq_csv" : "seq2seq_csv Network Description"
            ,"autoencoder_img" : "autoencoder_img Network Description"
            ,"autoencoder_csv" : "autoencoder_csv Network Description"
            ,"bilstmcrf_iob" : "bilstmcrf_iob Network Description"
            ,"fasttext_txt" : "fasttext_txt Network Description"
            ,"dnn" : "Multi Layer Perceptron이라고도 하며 가장 기본적인 Deep Neural Network"
            ,"ml" : "Machine Learning"
            ,"inceptionv4":"inceptionv4 Network Description"
            # ,"inception_resnet_v2": "inception_resnet_v2 Network Description"
            ,"ngram_mro":"ngram mro custom"
        }
        AutoMlRule().update_graph_type_list('graph_flow_desc', conf)

        # set network groups (frame, nlp, image, etc)
        conf = {
            "cnn" : "2"
            ,"resnet" : "2"
            ,"wdnn": "1"
            ,"dnn": "1"
            ,"wdnn_keras": "1"
            ,"ml" : "1"
            ,"word2vec" : "3"
            ,"word2vec_frame" : "3"
            ,"doc2vec" :"3"
            ,"wcnn" : "3"
            ,"seq2seq" : "3"
            ,"seq2seq_csv" : "3"
            ,"autoencoder_img" : "2"
            ,"autoencoder_csv" : "3"
            ,"bilstmcrf_iob" : "3"
            ,"fasttext_txt" : "3"
            ,"inceptionv4" : "2"
            # ,"inception_resnet_v2": "2"
            ,"ngram_mro": "4"
        }
        AutoMlRule().update_graph_type_list('graph_flow_group_id', conf)

        # set network sample file path
        conf = {
            "cnn" : "cnn_train.zip"
            , "resnet" : "resnet_train.zip"
            , "wdnn" : "wdnn_train.csv"
            , "dnn" : "dnn_train.csv"
            , "ml" : "ml_train.csv"
            , "wdnn_keras" : "wdnn_keras_train.csv"
            , "word2vec" : "word2vec_train.zip"
            , "word2vec_frame" : "word2vec_frame_train.zip"
            , "doc2vec" : "doc2vec_train.zip"
            , "wcnn" : "wcnn_train.csv"
            , "seq2seq" : "seq2seq_train.csv"
            , "seq2seq_csv" : "seq2seq_csv_train.csv"
            , "autoencoder_img" : "autoencoder_imgsample.csv"
            , "autoencoder_csv" : "autoencoder_csv_train.csv"
            , "bilstmcrf_iob" : "bilstmcrf_iob_train.csv"
            , "fasttext_txt" : "fasttext_txt_train.csv"
            , "inceptionv4" : "inceptionv4_train.zip"
            # , "inception_resnet_v2" : "inception_resnet_v2_train.zip"
            , "ngram_mro": "ngram_mro_train.tsv"
        }
        AutoMlRule().update_graph_type_list('train_file_path', conf)

        # set network sample file path
        conf = {
            "cnn": "cnn_test.zip"
            , "resnet": "resnet_test.zip"
            , "wdnn": "wdnn_test.csv"
            , "dnn": "dnn_test.csv"
            , "ml" : "ml_train.csv"
            , "wdnn_keras": "wdnn_keras_test.csv"
            , "word2vec": "word2vec_test.zip"
            , "word2vec_frame": "word2vec_frame_test.zip"
            , "doc2vec": "doc2vec_test.zip"
            , "wcnn": "wcnn_test.csv"
            , "seq2seq": "seq2seq_test.csv"
            , "seq2seq_csv": "seq2seq_csv_test.csv"
            , "autoencoder_img": "autoencoder_imgsample.csv"
            , "autoencoder_csv": "autoencoder_csv_test.csv"
            , "bilstmcrf_iob": "bilstmcrf_iob_test.csv"
            , "fasttext_txt": "fasttext_txt_test.csv"
            , "inceptionv4":"inceptionv4_test.zip"
            # , "inception_resnet_v2": "inception_resnet_v2_test.zip"
        }
        AutoMlRule().update_graph_type_list('eval_file_path', conf)

        # set network node alias name key
        conf = {
            "cnn" : 1
            , "resnet" : 1
            , "wdnn": 2
            , "dnn" : 2
            , "ml" : 12
            , "wdnn_keras" : 3
            , "word2vec" : 4
            , "word2vec_frame" : 5
            , "doc2vec" : 6
            , "wcnn" : 7
            , "seq2seq" : 8
            , "seq2seq_csv" : 9
            , "autoencoder_img" : 10
            , "autoencoder_csv" : 11
            , "bilstmcrf_iob" : 7
            , "fasttext_txt" : 7
            , "inceptionv4" :1
            # , "inception_resnet_v2": 1
            , "ngram_mro": 2
        }
        AutoMlRule().update_graph_type_list('graph_flow_info_id', conf)

        # set network node alias name key
        conf = {
            "cnn": "Y"
            , "resnet": "Y"
            , "wdnn": "Y"
            , "wdnn_keras": "N"
            , "dnn": "Y"
            , "ml" : "Y"
            , "dnn_keras": "N"
            , "word2vec": "N"
            , "word2vec_frame": "N"
            , "doc2vec": "N"
            , "wcnn": "Y"
            , "seq2seq": "N"
            , "seq2seq_csv": "Y"
            , "autoencoder_img": "N"
            , "autoencoder_csv": "N"
            , "bilstmcrf_iob": "N"
            , "fasttext_txt": "N"
            , "inceptionv4" : "Y"
            # , "inception_resnet_v2": "Y"
            , "ngram_mro": "Y"
        }
        AutoMlRule().update_graph_type_list('active_flag', conf)

        return {"automl_extra_parm" : True}
    except Exception as e:
        return {"automl_extra_parm" : False}