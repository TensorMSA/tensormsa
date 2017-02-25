from rest_framework import serializers
from master import models


class NN_DEF_LIST_INFO_Serializer(serializers.ModelSerializer):
    """
    Table : store Neural Network base information
    """
    class Meta:
        model = models.NN_DEF_LIST_INFO
        fields = ('nn_id', 'biz_cate', 'biz_sub_cate', 'nn_title', 'nn_desc', 'use_flag', 'dir', 'config')

class NN_VER_WFLIST_INFO_Serializer(serializers.ModelSerializer):
    """
    Table : store Neural Network Workflow version info
    """
    class Meta:
        model = models.NN_VER_WFLIST_INFO
        fields = ('nn_wf_ver_id', 'nn_def_list_info_nn_id', 'nn_wf_ver_info', 'condition', 'active_flag', 'nn_id')
