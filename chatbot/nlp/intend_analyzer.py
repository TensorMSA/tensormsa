from cluster.service.service_predict_seq2seq import PredictNetSeq2Seq
from cluster.service.service_predict_wcnn import PredictNetWcnn
from chatbot.common.chat_share_data import ShareData
from chatbot.common.chat_knowledge_data_dict import ChatKnowledgeDataDict

class IntendAnalyzer(ShareData):

    """
    parse raw text to tageed, entity filterd sentence
    ※ Example
    input : I bought a car yesterday
    output : I bought a car [time]
    """

    def __init__(self, cb_id, nn_id):
        """
        init global variables
        """
        self.cb_id = cb_id
        self.nn_id = nn_id
        self.seq2seq_model = PredictNetSeq2Seq()
        self.wcnn_model = PredictNetWcnn()

    def parse(self, share_data):
        """
        run intent analyzer
        :param context:
        :return:
        """
        if (share_data.get_intent_id() != ""):
            print("■■■■■■■■■■ 의도 존재  : " + share_data.get_intent_id())
        else :
            convert_data =  share_data.get_convert_data()
            intent_model = self.get_intent_model(convert_data)
            print ("■■■■■■■■■■ 의도 분석 결과 : " + intent_model)

            intent_rule = self.get_rule_value(convert_data)


            share_data.set_intent_id(intent_model)
            share_data.set_intent_history(intent_model)

            # slot_key = ChatKnowledgeDataDict(self.cb_id).get_essential_entity(share_data.get_intent_id())
            # share_data.set_story_key_entity(slot_key)
        return share_data

    def get_intent_model(self, convert_data):
        # result = self.seq2seq_model.run(self.nn_id , {"input_data": convert_data, "num": 0, "clean_ans": False})[0][1][0]
        intent_model = str(self.wcnn_model.run(self.nn_id, {"input_data": convert_data, "num": 0, "clean_ans": False})[0])
        return intent_model

    def get_rule_value(self, convert_data):
        result = ""
        return result