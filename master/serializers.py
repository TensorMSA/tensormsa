from rest_framework import serializers
from master import models


class NN_DEF_LIST_INFO_Serializer(serializers.ModelSerializer):
    """
    Table : NN_DEF_LIST_INFO
    """
    class Meta:
        model = models.NN_DEF_LIST_INFO
        fields = ('nn_id', 'biz_cate', 'biz_sub_cate', 'nn_title', 'nn_desc', 'use_flag', 'dir', 'config',
                  'automl_parms', 'automl_runtime', 'automl_stat')

class NN_DEF_LIST_ID_INFO_Serializer(serializers.ModelSerializer):
    """
    Table : NN_DEF_LIST_ID_INFO
    """
    class Meta:
        model = models.NN_DEF_LIST_ID_INFO
        fields = ('id', 'nn_id')

class NN_VER_WFLIST_INFO_Serializer(serializers.ModelSerializer):
    """
    Table : NN_VER_WFLIST_INFO
    """
    class Meta:
        model = models.NN_VER_WFLIST_INFO
        fields = ('nn_wf_ver_id', 'automl_gen', 'nn_def_list_info_nn_id', 'nn_wf_ver_desc', 'condition', 'active_flag', 'nn_id')

class NN_WF_NODE_INFO_Serializer(serializers.ModelSerializer):
    """
    Table : NN_WF_NODE_INFO
    """
    class Meta:
        model = models.NN_WF_NODE_INFO
        fields = ('nn_wf_node_id', 'nn_wf_node_name', 'wf_state_id', 'wf_task_submenu_id', 'wf_node_status',
                  'node_config_data', 'node_draw_x', 'node_draw_y', 'nn_wf_node_desc')

class NN_WF_STATE_INFO_Serializer(serializers.ModelSerializer):
    """
    Table : NN_WF_STATE_INFO
    """
    class Meta:
        model = models.NN_WF_STATE_INFO
        fields = ('wf_state_id', 'nn_id', 'nn_wf_ver_id')


class WF_TASK_MENU_RULE_Serializer(serializers.ModelSerializer):
    """
    Table : NN_WF_STATE_INFO
    """
    class Meta:
        model = models.WF_TASK_MENU_RULE
        fields = ('wf_task_menu_id', 'wf_task_menu_name', 'wf_task_menu_desc', 'visible_flag', )

class WF_TASK_SUBMENU_RULE_Serializer(serializers.ModelSerializer):
    """
    Table : NN_WF_STATE_INFO
    """
    class Meta:
        model = models.WF_TASK_SUBMENU_RULE
        fields = ('wf_task_submenu_id', 'wf_task_submenu_name', 'wf_task_submenu_desc',
                  'wf_node_class_path', 'wf_node_class_name', 'wf_task_menu_id')


class NN_WF_NODE_RELATION_Serializer(serializers.ModelSerializer):
    """
    Table : NN_WF_STATE_INFO
    """
    class Meta:
        model = models.NN_WF_NODE_RELATION
        fields = ('wf_state_id', 'nn_wf_node_id_1', 'nn_wf_node_id_2')

class TRAIN_SUMMARY_RESULT_INFO_Serializer(serializers.ModelSerializer):
    """
    Table : TRAIN_SUMMARY_RESULT_INFO
    """
    class Meta:
        model = models.TRAIN_SUMMARY_RESULT_INFO
        fields = ('nn_id', 'nn_wf_ver_id', 'nn_batch_ver_id', 'result_info')

class TRAIN_SUMMARY_ACCLOSS_INFO_Serializer(serializers.ModelSerializer):
    """
    Table : TRAIN_SUMMARY_ACCLOSS_INFO
    """
    class Meta:
        model = models.TRAIN_SUMMARY_ACCLOSS_INFO
        fields = ('nn_id', 'nn_wf_ver_id', 'nn_batch_ver_id', 'acc_info', 'loss_info')

class NN_VER_BATCHLIST_INFO_Serializer(serializers.ModelSerializer):
    """
    Table : NN_VER_BATCHLIST_INFO
    """
    class Meta:
        model = models.NN_VER_BATCHLIST_INFO
        fields = ('nn_batch_ver_id', 'active_flag', 'nn_wf_ver_id')

class AUTO_ML_RULE_Serializer(serializers.ModelSerializer):
    """
    Table : AUTO_ML_RULE
    """
    class Meta:
        model = models.AUTO_ML_RULE
        fields = ('graph_flow_id', 'graph_flow_data')