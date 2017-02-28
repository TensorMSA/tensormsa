from rest_framework import serializers
from master import models


class NN_DEF_LIST_INFO_Serializer(serializers.ModelSerializer):
    """
    Table : NN_DEF_LIST_INFO
    """
    class Meta:
        model = models.NN_DEF_LIST_INFO
        fields = ('nn_id', 'biz_cate', 'biz_sub_cate', 'nn_title', 'nn_desc', 'use_flag', 'dir', 'config')

class NN_VER_WFLIST_INFO_Serializer(serializers.ModelSerializer):
    """
    Table : NN_VER_WFLIST_INFO
    """
    class Meta:
        model = models.NN_VER_WFLIST_INFO
        fields = ('nn_wf_ver_id', 'nn_def_list_info_nn_id', 'nn_wf_ver_info', 'condition', 'active_flag', 'nn_id')

class NN_WF_NODE_INFO_Serializer(serializers.ModelSerializer):
    """
    Table : NN_WF_NODE_INFO
    """
    class Meta:
        model = models.NN_WF_NODE_INFO
        fields = ('nn_wf_node_id', 'nn_wf_node_name', 'wf_state_id', 'wf_task_submenu_id', 'wf_node_status',
                  'node_config_data', 'node_draw_x', 'node_draw_y')

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
                  'wf_node_class_name', 'wf_task_menu_id')


class NN_WF_NODE_RELATION_Serializer(serializers.ModelSerializer):
    """
    Table : NN_WF_STATE_INFO
    """
    class Meta:
        model = models.NN_WF_NODE_RELATION
        fields = ('wf_state_id', 'nn_wf_node_id_1', 'nn_wf_node_id_2')