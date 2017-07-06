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

    def check_result(self, intent_id, share_data):
        """
        check all preprocessed result and make final result 
        :param intent_id: 
        :return: 
        """
        try :
            dict_obj = share_data.get_story_slot_entity()
            ner_obj = share_data.get_story_ner_entity()
            dict_keys = list(dict_obj.keys())
            ner_keys = list(ner_obj.keys())
            essence, extra = self.get_entity_name(intent_id)
            common_keys = list(set(dict_keys).intersection(ner_keys))

            # case0 : if there is no intent essential parms
            if (len(list(set(essence))) == 0):
                logging.info("Case0 : cannot understand intent")
                share_data.set_intent_id("-1")

            # case1 : best case, predicted intent and common ner anal result sync well
            if (len(list(set(essence) - set(common_keys))) == 0):
                # trim entities fit to intent slot
                logging.info("Case1 : perfect case all matches!")
                del_keys = set(common_keys) - set(essence) - set(extra)
                for key in list(del_keys):
                    del ner_obj[key]
                share_data.replace_story_slot_entity(ner_obj)

            # case2 : intent and dict result matches
            elif (len(list(set(essence) - set(dict_keys))) == 0):
                # trim entities fit to intent slot
                logging.info("Case2 : intent and dict result matches")
                del_keys = set(dict_keys) - set(essence) - set(extra)
                for key in list(del_keys):
                    del dict_obj[key]
                share_data.replace_story_slot_entity(dict_obj)

            # case3 : predicted intent and bilstm anal matches
            elif (len(list(set(essence) - set(ner_keys))) == 0):
                # trim entities fit to intent slot
                logging.info("Case3 : intent and ner result matches")
                del_keys = set(common_keys.keys()) - set(essence) - set(extra)
                for key in list(del_keys):
                    del ner_obj[key]
                share_data.replace_story_slot_entity(ner_obj)

            # case4 : predicted intent and ner result do not match but common ner exists
            elif (len(common_keys) > 0):
                # get multiple intent which matches with ner result
                logging.info("Case4 : intent do not match but ner matches")
                c_intent_id = self.get_intent_candidate(common_keys)
                share_data.set_intent_id(c_intent_id)

            # case5 : error
            else :
                logging.info("Case5 : cannot understand input at all")
                share_data.set_intent_id("-1")
        except Exception as e :
            logging.info("Error : Error on summerize result")
            share_data.set_intent_id("-1")
        finally:
            return share_data
