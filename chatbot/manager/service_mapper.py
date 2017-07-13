from chatbot.common.chat_share_data import ShareData
import logging

class ServiceMapper(ShareData):

    def __init__(self, cb_id, entity_synonym, entity_uuid_list, intent_uuid_list):
        self.cb_id = cb_id
        self.entity_synonym = entity_synonym
        self.entity_uuid_list = entity_uuid_list
        self.intent_uuid_list = intent_uuid_list

    def run(self, share_data):
        story_slot = share_data.get_story_slot_entity()
        if(len(list(filter(lambda x : self.entity_synonym.convert_synonym_value(share_data, x, story_slot.get(x)) , sorted(story_slot.keys())))) > 0):
            logging.info("■■■■■■■■■■ 유의어 변화 결과 : " + str(list(story_slot.values())))
        #if (self.entity_synonym.get_synonym_key(key_slot)): sorted(share_data.get_story_slot_entity())
        #    convert_dict_data = self.entity_synonym.make_represent(share_data, key_slot)

        logging.info("■■■■■■■■■■ 의도 최종 결과 : " + str(share_data.get_intent_id()))
        logging.info("■■■■■■■■■■ Slot 최종 결과 : " + str(list(story_slot)))

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
