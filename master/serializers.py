from rest_framework import serializers
from master import models


class NN_DEF_LIST_INFO_Serializer(serializers.ModelSerializer):
    """
    Table : store Neural Network base information
    """
    class Meta:
        model = models.NN_DEF_LIST_INFO
        fields = ('nn_id', 'biz_cate', 'biz_sub_cate', 'nn_title', 'nn_desc', 'use_flag', 'dir', 'config')