from chatbot.common.chat_share_data import ShareData
import logging

class RuleIntentAnalyzer(ShareData):
    def __init__(self, intent_conf):
        self.intent_conf = intent_conf

    def parse(self, share_data):
        if (share_data.get_intent_id() != ""):
            logging.info("■■■■■■■■■■ 의도 존재  : " + share_data.get_intent_id())
        else :
            rule_exist = False
            intent_rule = self.get_rule_intent(share_data.get_request_data(), share_data)
            logging.info("■■■■■■■■■■ 의도 분석 결과(Rule) : " + str(intent_rule))
            if(intent_rule != ""):
                share_data.set_intent_id([intent_rule])
                share_data.set_intent_history(intent_rule)
                rule_exist = True
        return rule_exist

    def get_rule_intent(self, input_data, share_data):
        intent_list = list(filter(lambda x: list(filter(lambda key: input_data.startswith(key), x["fields"]["rule_value"]["key"])), self.intent_conf))
        # custom intent is only one
        if(len(intent_list) > 0):
            intent_rule = intent_list[0]["pk"]
            for key in intent_list[0]["fields"]["rule_value"]["key"]:
                if(input_data.count(key) > 0):
                    input_data = input_data.replace( key, '').strip()
            share_data.set_story_slot_entity(intent_list[0]["fields"]["rule_value"]["tag"], [input_data])
        else:
            intent_rule = ""
        return intent_rule