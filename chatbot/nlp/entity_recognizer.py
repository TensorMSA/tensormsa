from chatbot.common.chat_share_data import ShareData
from chatbot.common.chat_knowledge_data_dict import ChatKnowledgeDataDict
from cluster.service.service_predict_bilstmcrf import PredictNetBiLstmCrf

class EntityRecognizer(ShareData):

    def __init__(self, cb_id):
        """
        init global variables
        """
        self.cb_id = cb_id
        self.bilstmcrf_model = PredictNetBiLstmCrf()

    # TODO : call entity using by seq2seq (나는 식당에 간다 -> [나] [식당] )
    def parse(self, share_data):
        input_sentence = share_data.get_input_data()
        NER_data = self._get_NER_data(self, input_sentence)
        slot_key = ChatKnowledgeDataDict(self.cb_id).get_essential_entity(share_data.get_intent_id())
        share_data.set_story_key_entity(slot_key)
        return share_data

    def _make_slot_entity(self, share_data):

        return share_data

    # TODO : get BIO Tag from sentence
    def _get_NER_data(self, input_sentence):
        result = self.bilstmcrf_model.run('lstmcrf025', {"input_data": input_sentence, "num": 0, "clean_ans": False})
        return result