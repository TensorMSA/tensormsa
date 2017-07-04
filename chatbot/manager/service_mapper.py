from chatbot.common.chat_share_data import ShareData

class ServiceMapper(ShareData):

    def __init__(self, cb_id, entity_uuid):
        self.cb_id = cb_id
        self.entity_uuid = entity_uuid

    def run(self, share_data):
        #share_data.get_story_slot_entity()
        return share_data

    def replace_intent_uuid(self):
        pass

    def replace_entity_uuid(self):
        pass
