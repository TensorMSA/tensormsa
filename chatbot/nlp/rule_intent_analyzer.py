from chatbot.common.chat_share_data import ShareData
import logging

class RuleIntentAnalyzer(ShareData):
    def __init__(self, intent_conf):
        self.intent_conf = intent_conf

    def parse(self, share_data):
        if (share_data.get_intent_id() != ""):
            logging.info("■■■■■■■■■■ 의도 존재  : " + share_data.get_intent_id())
        else :
            intent_rule = self.get_rule_intent(share_data.get_morphed_data(), share_data)
            logging.info("■■■■■■■■■■ 의도 분석 결과(Rule) : " + str(intent_rule))
            share_data.set_intent_id(intent_rule)
            share_data.set_intent_history(intent_rule)
        return share_data

    def get_rule_intent(self, morphed_data, share_data):
        intent_list = list(filter(lambda x: x["fields"]["intent_type"] == "custom" and any(
            key in morphed_data for key in x["fields"]["rule_value"]["key"]), self.intent_conf))
        # custom intent is only one
        if(len(intent_list) > 0):
            intent_rule = intent_list[0]["pk"]
            for key in intent_list[0]["fields"]["rule_value"]["key"]:
                if(morphed_data.count(key)>0):
                    morphed_data.remove(key)
            share_data.set_story_slot_entity(intent_list[0]["fields"]["rule_value"]["key"][0], ''.join(morphed_data))
        else:
            intent_rule = ""
        return intent_rule