from chatbot.common.chat_share_data import ShareData
from chatbot.common.chat_knowledge_data_dict import ChatKnowledgeDataDict

class EntityRecognizer(ShareData):

    def __init__(self, cb_id):
        """
        init global variables
        """
        self.cb_id = cb_id

    # TODO : call entity using by seq2seq (나는 식당에 간다 -> [나] [식당] )
    def parse(self, share_data):

        slot_key = ChatKnowledgeDataDict(self.cb_id).get_essential_entity(share_data.get_intent_id())
        share_data.set_story_key_entity(slot_key)
        #share_data.story_slot_entity(slot_key,"김수상")
        return share_data

    def _make_slot_entity(self, share_data):

        return share_data

    # TODO : get BIO Tag from sentence
    def _get_NER_data(self, share_data):
        pass