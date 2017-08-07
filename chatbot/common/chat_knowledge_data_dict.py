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

    def _get_proper_tagging(self, type='dict'):
        query_set = models.CB_TAGGING_INFO.objects.filter(cb_id = self.cb_id,
                                                          pos_type = type)
        query_set = serial.serialize("json", query_set)
        return json.loads(query_set)[0]['fields']['proper_noun'] #JSON Type

    def get_intent_conf(self, type):
        query_set = models.CB_INTENT_LIST_INFO.objects.filter(cb_id = self.cb_id, intent_type = type)
        query_set = serial.serialize("json", query_set)
        return json.loads(query_set)

    #TODO:add similar word
    def initialize(self, cb_id):
        """
        initialize ChatKnowlodgeMemdict Class 
        :return: none
        """
        try :
            if(self.check_dict(cb_id)):
                # set dict
                query_set = self._get_proper_tagging(type='dict')
                proper_key_list = sorted(query_set.keys(),key=lambda x: query_set[x][0],reverse=False)
                ChatKnowledgeMemDict.data[cb_id] = {}
                ChatKnowledgeMemDict.data_order[cb_id] = []
                ChatKnowledgeMemDict.data_order[cb_id] = proper_key_list
                for key in proper_key_list:
                    ChatKnowledgeMemDict.data[cb_id][key] = self._get_entity_values(key, query_set)
                ChatKnowledgeMemDict.data[cb_id]["proper_noun"] = query_set

            if (self.check_ngram(cb_id)):
                # set ngram
                ngram_set = self._get_proper_tagging(type='ngram')
                ngram_key_list = sorted(ngram_set.keys(),key=lambda x: ngram_set[x][0],reverse=False)
                ChatKnowledgeMemDict.ngram[cb_id] = {}
                ChatKnowledgeMemDict.ngram_conf[cb_id] = {}
                ChatKnowledgeMemDict.ngram_order[cb_id] = []
                ChatKnowledgeMemDict.ngram_order[cb_id] = ngram_key_list
                for key in ngram_key_list:
                    ChatKnowledgeMemDict.ngram[cb_id][key] = self._get_entity_values(key, ngram_set)
                    ChatKnowledgeMemDict.ngram_conf[cb_id][key] = self._get_entity_conf(key, ngram_set)

            if (self.check_synonym(cb_id)) :
                ChatKnowledgeMemDict.synonym[cb_id] = {}
                ChatKnowledgeMemDict.synonym[cb_id] = self._get_synonym_value()

            if (self.check_conf(cb_id)):
                ChatKnowledgeMemDict.conf[cb_id] = {}
                ChatKnowledgeMemDict.conf[cb_id]['intent_uuid'] = self._get_intent_uuid()
                ChatKnowledgeMemDict.conf[cb_id]['entity_uuid'] = self._get_entity_uuid()
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

    def check_ngram(self, cb_id):
        """
        check if data is already loaded 
        :return: boolean
        """
        if(len(list(ChatKnowledgeMemDict.ngram.keys())) <= 0 ):
            return True
        if(cb_id in ChatKnowledgeMemDict.ngram.keys()) :
            return False
        else:
            return True

    def check_conf(self, cb_id):
        """
        check if data is already loaded 
        :return: boolean
        """
        if(len(list(ChatKnowledgeMemDict.conf.keys())) <= 0 ):
            return True
        if(cb_id in ChatKnowledgeMemDict.conf.keys()) :
            return False
        else:
            return True

    def check_synonym(self, cb_id):
        """
        check if data is already loaded 
        :return: boolean
        """
        if(len(list(ChatKnowledgeMemDict.synonym.keys())) <= 0 ):
            return True
        if(cb_id in ChatKnowledgeMemDict.synonym.keys()) :
            return False
        else:
            return True

    def _get_entity_conf(self, key, query_set):
        try :
            if(query_set.get(key)[2] != None and type(query_set.get(key)[2]) == float) :
                return query_set.get(key)[2]
            else :
                return 0.4
        except Exception as e:
            raise Exception (e)

    def _get_entity_values(self, key, query_set):
        try :
            values = []
            with open(query_set.get(key)[1], 'r') as input_file :
                if(input_file is not None):
                    for line in input_file.read().splitlines():
                        values.append(line)
            return values
        except Exception as e:
            raise Exception (e)

    def _get_entity_order(self, key, query_set):
        try :
            return query_set.get(key)[0]
        except Exception as e :
            raise Exception (e)

    def _get_intent_uuid(self):
        query_set = models.CB_INTENT_LIST_INFO.objects.filter(cb_id = self.cb_id)
        query_set = serial.serialize("json", query_set)
        return json.loads(query_set)

    def _get_entity_uuid(self):
        query_set = models.CB_ENTITY_RELATION_INFO.objects.filter(cb_id = self.cb_id)
        query_set = serial.serialize("json", query_set)
        return json.loads(query_set)

    def _get_synonym_value(self):
        query_set = models.CB_ENTITY_SYNONYM_LIST.objects.filter(cb_id = self.cb_id)
        query_set = serial.serialize("json", query_set)
        return json.loads(query_set)