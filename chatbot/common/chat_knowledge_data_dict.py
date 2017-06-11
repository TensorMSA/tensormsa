from chatbot import models
from django.core import serializers as serial
import json

class ChatKnowledgeDataDict:

    def __init__(self, cb_id):
        self.cb_id = cb_id
        #TODO : need to get data from cache
    def get_intent_entity_keys(self):
        query_set = models.CB_ENTITY_LIST_INFO.objects.filter(cb_id = self.cb_id, entity_type = 'key')
        query_set = serial.serialize("json", query_set)
        return json.loads(query_set)[0]['fields']['entity_list']['key'] # list type

    def get_entity_values(self):
        query_set = models.CB_ENTITY_LIST_INFO.objects.filter(cb_id = self.cb_id, entity_type = 'key_values')
        query_set = serial.serialize("json", query_set)
        return json.loads(query_set)[0]['fields']['entity_list'] # json type

    def get_essential_entity(self, intent):
        query_set = models.CB_ENTITY_LIST_INFO.objects.filter(cb_id = self.cb_id,intent_id = intent, entity_type = 'essential')
        if (query_set == '[]'):
            return None
        else:
            query_set = serial.serialize("json", query_set)
            return json.loads(query_set)[0]['fields']['entity_list']['essential']  # list type

    def get_custom_entity(self):
        query_set = models.CB_ENTITY_LIST_INFO.objects.filter(cb_id = self.cb_id, entity_type = 'custom')
        query_set = serial.serialize("json", query_set)
        return json.loads(query_set)[0]['fields']['entity_list']['custom']  # list type

    def get_proper_tagging(self):
        query_set = models.CB_TAGGING_INFO.objects.filter(cb_id = self.cb_id)
        query_set = serial.serialize("json", query_set)
        return json.loads(query_set)[0]['fields']['proper_noun'] #JSON Type
