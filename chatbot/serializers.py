from rest_framework import serializers
from chatbot import models


class CB_DEF_LIST_INFO_Serializer(serializers.ModelSerializer):
    """
    Table : CB_DEF_LIST_INFO
    """
    class Meta:
        model = models.CB_DEF_LIST_INFO
        fields = ('cb_id', 'chat_cate', 'chat_sub_cate', 'cb_title', 'cb_desc', 'creation_date','last_update_date', 'created_by', 'last_updated_by')
