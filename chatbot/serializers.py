from rest_framework import serializers
from chatbot import models


class CB_DEF_LIST_INFO_Serializer(serializers.ModelSerializer):
    """
    Table : CB_DEF_LIST_INFO
    """
    class Meta:
        model = models.CB_DEF_LIST_INFO
        fields = ('cb_id', 'chat_cate', 'chat_sub_cate', 'cb_title', 'cb_desc', 'creation_date','last_update_date', 'created_by', 'last_updated_by')

class CB_INTENT_LIST_INFO_Serializer(serializers.ModelSerializer):
    """
    Table : CB_INTENT_LIST_INFO
    """
    class Meta:
        model = models.CB_INTENT_LIST_INFO
        fields = ('cb_id', 'intent_id', 'intent_type', 'intent_desc', 'nn_id', 'nn_type')

class CB_STORYBOARD_LIST_INFO_Serializer(serializers.ModelSerializer):
    """
    Table : CB_STORYBOARD_LIST_INFO
    """
    class Meta:
        model = models.CB_STORYBOARD_LIST_INFO
        fields = ('intent_id', 'story_id', 'story_desc')

class CB_ENTITY_LIST_INFO_Serializer(serializers.ModelSerializer):
    """
    Table : CB_STORYBOARD_LIST_INFO
    """
    class Meta:
        model = models.CB_ENTITY_LIST_INFO
        fields = ('story_id', 'entity_type', 'entity_list')