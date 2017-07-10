from chatbot import models
from django.core import serializers as serial
import json
from chatbot.common.chat_knowledge_mem_dict import ChatKnowledgeMemDict

class ChatKnowledgeDataDict:

    def __init__(self, cb_id):
        self.cb_id = cb_id

    def get_entity(self):
        query_set = models.CB_ENTITY_LIST_INFO.objects.filter(cb_id = self.cb_id)
        query_set = serial.serialize("json", query_set)
        return json.loads(query_set)

    def get_entity_key(self, intent_id):
        query_set = models.CB_ENTITY_LIST_INFO.objects.filter(cb_id = self.cb_id,
                                                              intent_id_id = intent_id)
        query_set = serial.serialize("json", query_set)
        query_set = json.loads(query_set)[0]['fields']['entity_list']
        return query_set.get('key')

    def get_entity_extra(self, intent_id):
        query_set = models.CB_ENTITY_LIST_INFO.objects.filter(cb_id = self.cb_id,
                                                              intent_id_id = intent_id)
        query_set = serial.serialize("json", query_set)
        query_set = json.loads(query_set)[0]['fields']['entity_list']
        return query_set.get('extra')

    def get_proper_tagging(self, type='dict'):
        query_set = models.CB_TAGGING_INFO.objects.filter(cb_id = self.cb_id,
                                                          pos_type = type)
        query_set = serial.serialize("json", query_set)
        return json.loads(query_set)[0]['fields']['proper_noun'] #JSON Type

    def get_intent_conf(self):
        query_set = models.CB_INTENT_LIST_INFO.objects.filter(cb_id = self.cb_id)
        query_set = serial.serialize("json", query_set)
        return json.loads(query_set)

    #TODO:add similar word
    def initialize(self, cb_id, type='ngram'):
        """
        initialize ChatKnowlodgeMemdict Class 
        :return: none
        """
        try :
            if(self.check_dict(cb_id)) :
                query_set = self.get_proper_tagging(type=type)
                self.proper_key_list = sorted(query_set.keys(),
                                              key=lambda x: query_set[x][0],
                                              reverse=False)
                self.proper_noun = query_set
                ChatKnowledgeMemDict.data[cb_id] = {}
                for key in self.proper_key_list:
                    ChatKnowledgeMemDict.data[cb_id][key] = self._get_entity_values(key)

                ChatKnowledgeMemDict.synonym[cb_id] = {}
                ChatKnowledgeMemDict.synonym[cb_id] = self._get_synonym_value()

        except Exception as e :
            raise Exception ("error on chatbot dict init : {0}".format(e))

    def check_dict(self, cb_id):
        """
        check if data is already loaded 
        :return: boolean
        """
        if(len(list(ChatKnowledgeMemDict.data.keys())) <= 0 ):
            return True
        if(cb_id in ChatKnowledgeMemDict.data.keys()) :
            return False
        else:
            return True

    def _get_entity_values(self, key):
        try :
            values = []
            with open(self.proper_noun.get(key)[1], 'r') as input_file :
                if(input_file is not None):
                    for line in input_file.read().splitlines():
                        values.append(line)
            return values
        except Exception as e :
            raise Exception (e)

    def get_intent_uuid(self):
        query_set = models.CB_INTENT_LIST_INFO.objects.filter(cb_id = self.cb_id)
        query_set = serial.serialize("json", query_set)
        return json.loads(query_set)

    def get_entity_uuid(self):
        query_set = models.CB_ENTITY_RELATION_INFO.objects.filter(cb_id = self.cb_id)
        query_set = serial.serialize("json", query_set)
        return json.loads(query_set)

    def get_intent_uuid(self):
        query_set = models.CB_INTENT_LIST_INFO.objects.filter(cb_id = self.cb_id)
        query_set = serial.serialize("json", query_set)
        return json.loads(query_set)

    def _get_synonym_value(self):
        query_set = models.CB_ENTITY_SYNONYM_LIST.objects.filter(cb_id = self.cb_id)
        query_set = serial.serialize("json", query_set)
        return json.loads(query_set)