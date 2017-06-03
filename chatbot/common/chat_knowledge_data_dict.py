from chatbot import models
from django.core import serializers as serial
import json

class ChatKnowledgeDataDict:

    def __init__(self, cb_id):
        pass

    def get_entity_keys(self, cb_id):
        query_set = models.CB_ENTITY_LIST_INFO.objects.filter(story_id='7', entity_type = 'key')
        query_set = serial.serialize("json", query_set)
        return json.loads(query_set)[0]['fields']['entity_list']['key'] # list type

    def get_entity_values(self, cb_id):
        #TODO : need to get data from cache
        query_set = models.CB_ENTITY_LIST_INFO.objects.filter(story_id='7', entity_type = 'values')
        query_set = serial.serialize("json", query_set)
        return json.loads(query_set)[0]['fields']['entity_list'] # list type

    def get_essential_entity(self, story_id):

        query_set = models.CB_ENTITY_LIST_INFO.objects.filter(story_id = '7', entity_type = 'essential')
        query_set = serial.serialize("json", query_set)
        return json.loads(query_set)[0]['fields']['entity_list']['essential']  # list type


