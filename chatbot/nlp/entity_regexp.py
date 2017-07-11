from chatbot.common.chat_share_data import ShareData
from chatbot.common.chat_knowledge_mem_dict import ChatKnowledgeMemDict

class EntityRegex(ShareData):

    def __init__(self, cb_id):
        self.cb_id = cb_id

    def parse(self, data):
        pass