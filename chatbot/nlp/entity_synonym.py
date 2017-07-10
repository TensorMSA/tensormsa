from chatbot.common.chat_share_data import ShareData
from chatbot.common.chat_knowledge_mem_dict import ChatKnowledgeMemDict

class EntitySynonym(ShareData):

    def __init__(self, cb_id):
        self.cb_id = cb_id

    def make_represent(self, share_data, key, synonym):
        synonym_list = ChatKnowledgeMemDict.synonym.get(self.cb_id)
        represent_value = list(filter(lambda x: x["fields"]["synonym_value"] == synonym ,synonym_list))
        share_data.set_story_slot_entity(key, represent_value[0]["fields"]["slot_type"])
        return represent_value[0]["fields"]["represent_value"]

    def get_synonym_key(self, key, synonym):
        exist = False
        synonym_list = ChatKnowledgeMemDict.synonym.get(self.cb_id)
        key_list = list(filter(lambda x: x["fields"]["entity_id"] == key and x["fields"]["synonym_value"] == synonym , synonym_list))
        if(len(key_list) > 0 ):
            exist = True
        return exist