from chatbot.common.chat_share_data import ShareData
from chatbot.story.story_board_manager import StoryBoardManager
import logging

class SummrizeResult():
    """
    summrize all preprocessed data into final result 
    """
    def __init__(self, dict_conf):
        self.dict_conf = dict_conf
        self.intent_info = self.dict_conf.get_entity()

    def parse(self, share_data):
        """
        summrize all preprocessed data into final result 
        :param share_data:
        :return:
        """
        try :
            intent_id = share_data.get_intent_id()
            share_data = self.check_result(intent_id, share_data)
            return share_data
        except Exception as e:
            raise Exception(e)

    def get_entity_name(self, intent_id):
        """
        get prime entity key and extra key with intent id 
        :param intent: 
        :return: 
        """
        temp = list(filter(lambda x: x['fields']['intent_id'] == intent_id, self.intent_info))
        return temp[0]['fields']['entity_list']['key'], temp[0]['fields']['entity_list']['extra']

    def get_intent_candidate(self, ner_keys):
        """
        get all intent ids matchs with ner anal result 
        :param intent: 
        :return: 
        """
        temp = list(filter(lambda x: len(list(set(x['fields']['entity_list']['key']) - set(ner_keys))) == 0, self.intent_info))
        return list(map(lambda x : x['fields']['intent_id'], temp))

    def check_result(self, intent_id, share_data):
        """
        check all preprocessed result and make final result 
        :param intent_id: 
        :return: 
        """
        ner_keys = list(share_data.get_story_slot_entity().keys())
        essence, extra = self.get_entity_name(intent_id)

        if(len(list(set(essence) - set(ner_keys))) > 0 ) :
            logging.info("### 분석된 의도에서 요구하는 필수 파라메터를 충족하지 못함 ###")
            share_data.set_intent_id("-1")

        if (len(list((set(ner_keys)) - set(essence) - set(extra))) > 0) :
            logging.info("### 분석된 의도에서 요구하는 파라메터 외의 Entitiy 추출 ###")
            share_data.set_intent_id(self.get_intent_candidate(ner_keys))

        return share_data

