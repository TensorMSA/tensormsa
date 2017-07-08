#from cluster.service.service_predict_seq2seq import PredictNetSeq2Seq
from cluster.service.service_predict_wcnn import PredictNetWcnn
from chatbot.common.chat_share_data import ShareData
import logging

class PatternIntendAnalyzer(ShareData):

    """
    parse raw text to tageed, entity filterd sentence
    ※ Example
    input : I bought a car yesterday
    output : I bought a car [time]
    """

    def __init__(self, cb_id, nn_id, intent_conf):
        """
        init global variables
        """
        self.cb_id = cb_id
        self.nn_id = nn_id
        self.intent_conf = intent_conf
        #self.seq2seq_model = PredictNetSeq2Seq()
        self.wcnn_model = PredictNetWcnn()

    def parse(self, share_data):
        """
        run intent analyzer
        :param context:
        :return:
        """
        if (share_data.get_intent_id() != ""):
            logging.info("■■■■■■■■■■ 의도 존재  : " + share_data.get_intent_id())
        else :
            convert_data = share_data.get_convert_dict_data()
            intent_model = self.get_intent_model(' '.join(convert_data))
            logging.info("■■■■■■■■■■ Pattern 의도 분석 결과(Model) : " + intent_model)

            # intent_rule = self.get_rule_value(convert_data)
            # logging.info("■■■■■■■■■■ 의도 분석 결과(Rule) : " + str(intent_rule))
            #
            # if(intent_model == -1):
            #     intent_model = intent_rule
            #
            # share_data.set_pattern_intent_id(intent_model)
            # share_data.set_intent_history(intent_model)

        return share_data

    def get_intent_model(self, convert_data):
        # result = self.seq2seq_model.run(self.nn_id , {"input_data": convert_data, "num": 0, "clean_ans": False})[0][1][0]
        intent_model = str(self.wcnn_model.run(self.nn_id, {"input_data": convert_data, "num": 0, "clean_ans": False})[0])
        return intent_model

    # def get_rule_value(self, convert_data):
    #     intent_list = list(filter(lambda x: x["fields"]["intent_type"] == "custom" and any(
    #         key in convert_data for key in x["fields"]["rule_value"]["value"]), self.intent_conf))
    #     intent_list = list(map(lambda x : x["fields"]["intent_id"], intent_list))
    #     #custom intent is only one
    #     intent_rule = intent_list[0] if len(intent_list) > 0 else "-1"
    #     return intent_rule