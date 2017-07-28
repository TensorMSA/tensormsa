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
        fields = ('cb_id', 'intent_id', 'intent_type', 'rule_value', 'intent_desc', 'nn_type')

class CB_STORYBOARD_LIST_INFO_Serializer(serializers.ModelSerializer):
    """
    Table : CB_STORYBOARD_LIST_INFO
    """
    class Meta:
        model = models.CB_STORYBOARD_LIST_INFO
        fields = ('intent_id', 'story_id', 'story_desc', 'story_type')

class CB_RESPONSE_LIST_INFO_Serializer(serializers.ModelSerializer):
    """
    Table : CB_RESPONSE_LIST_INFO
    """
    class Meta:
        model = models.CB_RESPONSE_LIST_INFO
        fields = ('story_id', 'response_type', 'output_entity', 'output_data', 'nn_id')

class CB_SERVICE_LIST_INFO_Serializer(serializers.ModelSerializer):
    """
    Table : CB_SERVICE_LIST_INFO
    """
    class Meta:
        model = models.CB_SERVICE_LIST_INFO
        fields = ('story_id', 'service_name', 'service_type', 'url')

class CB_ENTITY_LIST_INFO_Serializer(serializers.ModelSerializer):
    """
    Table : CB_STORYBOARD_LIST_INFO
    """
    class Meta:
        model = models.CB_ENTITY_LIST_INFO
        fields = ('cb_id', 'intent_id', 'entity_type', 'entity_list')


class CB_TAGGING_INFO_Serializer(serializers.ModelSerializer):
    """
    Table : CB_TAGGING_INFO
    """
    class Meta:
        model = models.CB_TAGGING_INFO
        fields = ('cb_id', 'pos_type', 'proper_noun')

class CB_MODEL_LIST_INFO_Serializer(serializers.ModelSerializer):
    """
    Table : CB_MODEL_LIST_INFO
    """
    class Meta:
        model = models.CB_MODEL_LIST_INFO
        fields = ('cb_id', 'nn_id', 'nn_purpose','nn_type','nn_label_data','nn_desc')

class CB_ENTITY_RELATION_INFO_Serializer(serializers.ModelSerializer):
    """
    Table : CB_ENTITY_RELATION_INFO
    """
    class Meta:
        model = models.CB_ENTITY_RELATION_INFO
        fields = ('cb_id', 'entity_id', 'entity_uuid', 'entity_desc')
