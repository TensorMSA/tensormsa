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

        intent_rule = ""
        for row in self.intent_conf:
            if(row['fields']['nn_type'] == 'start'):
                if(len(list(filter(lambda x: input_data.startswith(x) ,row["fields"]["rule_value"]["key"]))) == 1):
                    intent_rule = row["pk"]
                    for key in row["fields"]["rule_value"]["key"]:
                        if (input_data.count(key) > 0):
                            input_data = input_data.replace(key, '').strip()
                            break
                    share_data.set_story_slot_entity(row["fields"]["rule_value"]["tag"], [input_data])
                    break
            elif (row['fields']['nn_type'] == 'like'):
                if(len(list(filter(lambda x: input_data.find(x)>-1 ,row["fields"]["rule_value"]["key"]))) == 1):
                    intent_rule = row["pk"]
                    for key in row["fields"]["rule_value"]["key"]:
                        if (input_data.startswith(key) is True):
                            input_data = input_data.replace(key, '').strip()
                            break
                        elif (input_data.count(key) > 0):
                            input_data = input_data[0:input_data.index(key)].strip()
                            break
                    share_data.set_story_slot_entity(row["fields"]["rule_value"]["tag"], [input_data])
                    break
            else:
                intent_rule = ""
                pass

        return intent_rule