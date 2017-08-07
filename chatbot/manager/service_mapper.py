from chatbot.common.chat_share_data import ShareData
from chatbot.common.chat_knowledge_mem_dict import ChatKnowledgeMemDict

import logging

class ServiceMapper(ShareData):

    def __init__(self, cb_id, entity_synonym):
        self.cb_id = cb_id
        self.entity_synonym = entity_synonym
        self.intent_uuid_list = ChatKnowledgeMemDict.conf.get(self.cb_id).get('intent_uuid')
        self.entity_uuid_list = ChatKnowledgeMemDict.conf.get(self.cb_id).get('entity_uuid')

    def run(self, share_data):
        story_slot = share_data.get_story_slot_entity()
        if(len(list(filter(lambda x : self.entity_synonym.convert_synonym_value(share_data, x, story_slot.get(x)) , sorted(story_slot.keys())))) > 0):
            logging.info("■■■■■■■■■■ 유의어 변화 결과 : " + str(list(story_slot.values())))

        logging.info("■■■■■■■■■■ 의도 최종 결과 : " + str(share_data.get_intent_id()))
        logging.info("■■■■■■■■■■ Slot 최종 결과 : " + str(story_slot))
        self._store_train_data(share_data)

        self._replace_intent_uuid(share_data)
        self._replace_entity_uuid(story_slot)
        return share_data

    def _replace_intent_uuid(self, share_data):
        intent_uuid = []
        for intent_id in share_data.get_intent_id() :
            intent_uuid = intent_uuid + list(filter(lambda x: x["pk"] == str(intent_id), self.intent_uuid_list))
        intent_uuid =  list(map(lambda x : x['fields']['intent_uuid'], intent_uuid))
        share_data.set_intent_id(intent_uuid)

    def _replace_entity_uuid(self, story_slot):
        slot_key_list = list(story_slot.keys())
        for key in slot_key_list:
            entity_uuid = list(filter(lambda x: x["fields"]["entity_id"] == key, self.entity_uuid_list))
            story_slot[entity_uuid[0]['fields']['entity_uuid']] = story_slot.pop(key)

    def _store_train_data(self,share_data):
        file = open("/hoya_data_root/log/log.txt", 'a')
        data = "[%s , %s , %s , %s]\n"  % ( str(share_data.get_request_data()), str(share_data.get_story_slot_entity())
                                            , str(share_data.get_intent_id()), str(share_data.get_intent_history()))
        file.write(data)
        file.close()