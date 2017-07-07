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
            pattern_intent_id = share_data.get_pattern_intent_id()
            share_data = self.check_result(pattern_intent_id, intent_id, share_data)
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
        if (temp == []):
            return "",""
        else:
            return temp[0]['fields']['entity_list']['key'], temp[0]['fields']['entity_list']['extra']

    def get_intent_candidate(self, ner_keys):
        """
        get all intent ids matchs with ner anal result 
        :param intent: 
        :return: 
        """
        temp = list(filter(lambda x: len(list(set(x['fields']['entity_list']['key']) - set(ner_keys))) == 0, self.intent_info))
        return list(map(lambda x : x['fields']['intent_id'], temp))

    def check_result(self, pattern_intent_id, intent_id, share_data):
        """
        check all preprocessed result and make final result 
        :param intent_id: 
        :return: 
        """
        try :
            # get all factors already preprocessed
            self.dict_obj = share_data.get_story_slot_entity()
            self.ner_obj = share_data.get_story_ner_entity()
            self.dict_keys = list(self.dict_obj.keys())
            self.ner_keys = list(self.ner_obj.keys())
            essence, extra = self.get_entity_name(intent_id)
            p_essence, p_extra =  self.get_entity_name(pattern_intent_id)
            self.common_keys = list(set(self.dict_keys).intersection(self.ner_keys))

            # get each intent's score
            share_data1, score1 = self.get_score(essence, extra, share_data, intent_id)
            share_data2, score2 = self.get_score(p_essence, p_extra, share_data, pattern_intent_id)

            # use higher score intent
            if(score1 > score2) :
                share_data = share_data1
            else :
                share_data = share_data2
        except Exception as e :
            logging.info("Error : Error on summerize result")
            share_data.set_intent_id("-1")
        finally:
            return share_data

    def get_score(self, essence, extra, share_data, intent_id):
        """
        
        :return: 
        """
        score = 0
        share_data.set_intent_id(intent_id)

        # case0 : if there is no intent essential parms
        if (len(list(set(essence))) == 0):
            logging.info("Case0 : cannot understand intent")
            share_data.set_intent_id("-1")
            score = -1

        # case1 : best case, predicted intent and common ner anal result sync well
        if (len(list(set(essence) - set(self.common_keys))) == 0):
            # trim entities fit to intent slot
            logging.info("Case1 : perfect case all matches!")
            del_keys = set(self.common_keys) - set(essence) - set(extra)
            for key in list(del_keys):
                del self.ner_obj[key]
            share_data.replace_story_slot_entity(self.ner_obj)
            score = 10 + len(essence)

        # case2 : intent and dict result matches
        elif (len(list(set(essence) - set(self.dict_keys))) == 0):
            # trim entities fit to intent slot
            logging.info("Case2 : intent and dict result matches")
            del_keys = set(self.dict_keys) - set(essence) - set(extra)
            for key in list(del_keys):
                del self.dict_obj[key]
            share_data.replace_story_slot_entity(self.dict_obj)
            score = 7 + len(essence)

        # case3 : predicted intent and bilstm anal matches
        elif (len(list(set(essence) - set(self.ner_keys))) == 0):
            # trim entities fit to intent slot
            logging.info("Case3 : intent and ner result matches")
            del_keys = set(self.common_keys.keys()) - set(essence) - set(extra)
            for key in list(del_keys):
                del self.ner_obj[key]
            share_data.replace_story_slot_entity(self.ner_obj)
            score = 8 + len(essence)

        # case4 : predicted intent and ner result do not match but common ner exists
        elif (len(self.common_keys) > 0):
            # get multiple intent which matches with ner result
            logging.info("Case4 : intent do not match but ner matches")
            c_intent_id = self.get_intent_candidate(self.common_keys)
            share_data.set_intent_id(c_intent_id)
            score = 5

        # case5 : error
        else:
            logging.info("Case5 : cannot understand input at all")
            share_data.set_intent_id("-1")
            score = -1

        return share_data, score