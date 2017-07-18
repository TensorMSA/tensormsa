from chatbot.common.chat_share_data import ShareData
from chatbot.common.chat_knowledge_mem_dict import ChatKnowledgeMemDict

class EntitySynonym(ShareData):

    def __init__(self, cb_id):
        self.cb_id = cb_id

    def make_represent(self, share_data, synonym):
        synonym_list = ChatKnowledgeMemDict.synonym.get(self.cb_id)
        represent_value = list(filter(lambda x: x["fields"]["synonym_value"] in synonym ,synonym_list))
        share_data.set_story_slot_entity(represent_value[0]["fields"]["entity_id"], [represent_value[0]["fields"]["represent_value"]])
        return represent_value[0]["fields"]["entity_id"]

    def convert_synonym_value(self, share_data, key, synonym):
        exist = False
        synonym_list = ChatKnowledgeMemDict.synonym.get(self.cb_id)
        key_list = list(filter(lambda x: x["fields"]["entity_id"] == key and x["fields"]["synonym_value"] in synonym , synonym_list))

        for i, syn in enumerate(synonym) :
            for key in key_list :
                if (syn == key['fields']['synonym_value']) :
                    synonym[i] = key['fields']['represent_value']

        if(len(key_list) > 0):
            share_data.set_story_slot_entity(key_list[0]["fields"]["entity_id"], synonym)
            exist = True
        return exist