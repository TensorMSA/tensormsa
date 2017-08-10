from chatbot.common.chat_share_data import ShareData
from chatbot.story.story_board_manager import StoryBoardManager
import logging, copy
from functools import reduce

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
        try:
            intent_id = share_data.get_intent_id()
            pattern_intent_id = share_data.get_pattern_intent_id()
            #Rule intent is exist then pass
            if(intent_id is not "" and pattern_intent_id is ""):
                pass
            else:
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
        temp = list(filter(lambda x: x['fields']['intent_id'] == intent_id[0], self.intent_info))
        if (temp == []):
            return [],[]
        else:
            return temp[0]['fields']['entity_list']['key'], temp[0]['fields']['entity_list']['extra']

    def get_intent_candidate(self, ner_keys):
        """
        get all intent ids matchs with ner anal result 
        :param intent: 
        :return: 
        """
        temp = list(filter(lambda x: len(list(set(ner_keys) - set(
            x['fields']['entity_list']['key'] if 'key' in x['fields']['entity_list'] else []))) == 0, self.intent_info))
        return list(map(lambda x : x['fields']['intent_id'], temp))

    def get_intent_match(self, keys):
        """
        get all intent ids matchs with ner anal result 
        :param intent: 
        :return: 
        """
        temp = list(filter(lambda x: len(list(set(keys)
                                              - set(x['fields']['entity_list']['key'])
                                              - set(x['fields']['entity_list']['extra']))) == 0
                                     , self.intent_info))
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
            share_data1, score1 = self.get_score(essence, extra, copy.deepcopy(share_data), intent_id)
            share_data2, score2 = self.get_score(p_essence, p_extra, copy.deepcopy(share_data), pattern_intent_id)

            # use higher score intent
            if(score1 > score2) :
                share_data = share_data1
                return share_data
            else :
                share_data = share_data2
                return share_data
        except Exception as e :
            logging.info("Error : Error on summerize result")
            share_data.set_intent_id("-1")

    def get_score(self, essence, extra, share_data, intent_id):
        """
        calculate score with share_data and intent slots 
        :return: 
        """
        try :
            score = 0
            share_data.set_intent_id(intent_id)
            ner_obj = self.ner_obj.copy()
            dict_obj = self.dict_obj.copy()

            # case0 : if there is no intent essential parms
            if(len(list(set(essence))) == 0):
                logging.info("Case0 : cannot understand intent")
                score = -1
                essence.append("dummy")

            # case1 : best case, predicted intent and common ner anal result sync well
            if(len(list(set(essence) - set(self.common_keys))) == 0):
                # trim entities fit to intent slot
                logging.info("Case1 : perfect case all matches!")
                del_ner_keys = set(self.ner_keys) - set(essence) - set(extra)
                for key in list(del_ner_keys):
                    del ner_obj[key]
                del_dict_keys = set(self.dict_keys) - set(essence) - set(extra)
                for key in list(del_dict_keys):
                    del dict_obj[key]
                if(len(list(ner_obj.keys())) >= len(list(dict_obj.keys()))) :
                    extra_score = len(list(ner_obj.keys()))
                    len_score = reduce(lambda x,y : x + y, list(map(lambda x : len(self.ner_obj[x][0]), ner_obj.keys())))
                    share_data.replace_story_slot_entity(ner_obj)
                else :
                    extra_score = len(list(dict_obj.keys()))
                    len_score = reduce(lambda x, y: x + y, list(map(lambda x: len(self.dict_obj[x][0]), dict_obj.keys())))
                    share_data.replace_story_slot_entity(dict_obj)
                score = 9.6 + len(essence) + extra_score * 0.3 + len_score * 0.001

            # case2 : intent and dict result matches
            elif(len(list(set(essence) - set(self.dict_keys))) == 0):
                # trim entities fit to intent slot
                logging.info("Case2 : intent and dict result matches")
                del_keys = set(self.dict_keys) - set(essence) - set(extra)
                for key in list(del_keys):
                    del dict_obj[key]
                extra_score = len(list(dict_obj.keys()))
                len_score = reduce(lambda x, y: x + y, list(map(lambda x: len(self.dict_obj[x][0]), dict_obj.keys())))
                share_data.replace_story_slot_entity(dict_obj)
                score = 9.5 + len(essence)  + extra_score * 0.3 + len_score * 0.001

            # case3 : predicted intent and bilstm anal matches
            elif(len(list(set(essence) - set(self.ner_keys))) == 0):
                # trim entities fit to intent slot
                logging.info("Case3 : intent and ner result matches")
                del_keys = set(self.ner_keys) - set(essence) - set(extra)
                for key in list(del_keys):
                    del ner_obj[key]
                share_data.replace_story_slot_entity(ner_obj)
                len_score = reduce(lambda x, y: x + y, list(map(lambda x: len(self.ner_obj[x][0]), ner_obj.keys())))
                extra_score = len(list(ner_obj.keys()))
                score = 9.5 + len(essence)  + extra_score * 0.3 + len_score * 0.001

            # case5 : check dict key matching intent
            elif (len(self.dict_keys) > 0 and (len(self.dict_keys) > len(self.ner_keys))):
                # get multiple intent which matches with ner result
                logging.info("Case5 : find intent with ner keys ")
                c_intent_id = self.get_intent_match(self.dict_keys)
                share_data.set_intent_id(list(set(c_intent_id + intent_id)))

                # delete unnecessary keys
                del_dict_keys = set(self.dict_keys) - set(essence)
                for key in list(del_dict_keys):
                    del dict_obj[key]
                share_data.replace_story_slot_entity(dict_obj)

                # set -1 when there is no alternative option
                if (len(share_data.get_intent_id()) == 0):
                    share_data.set_intent_id(["-1"])
                score = 5 + len(self.dict_keys)

            # case6 : check ner key matching intent
            elif (len(self.ner_keys) > 0 and (len(self.ner_keys) > len(self.dict_keys))):
                # get multiple intent which matches with ner result
                logging.info("Case6 : find intent with ner keys ")
                c_intent_id = self.get_intent_match(self.ner_keys)
                share_data.set_intent_id(list(set(c_intent_id + intent_id)))

                #delete unnecessary keys
                del_ner_keys = set(self.ner_keys) - set(essence)
                for key in list(del_ner_keys):
                    del ner_obj[key]
                share_data.replace_story_slot_entity(ner_obj)

                # set -1 when there is no alternative option
                if (len(share_data.get_intent_id()) == 0):
                    share_data.set_intent_id(["-1"])
                score = 5 + len(self.ner_keys)

            # case8 : make combine key with dict result and ner result
            elif ((str(self.dict_keys) != str(self.ner_keys))):
                # get multiple intent which matches with ner result
                logging.info("Case8 : find intent with combined keys ")
                comb_keys = list(set(self.ner_keys + self.dict_keys))
                comb_obj = {}
                for key in comb_keys :
                    if (dict_obj.get(key) == None and ner_obj.get(key) == None) :
                        break
                    elif (dict_obj.get(key) == None):
                        comb_obj[key] = ner_obj[key]
                    elif (ner_obj.get(key) == None):
                        comb_obj[key] = dict_obj[key]
                    elif (ner_obj.get(key) == dict_obj.get(key)):
                        comb_obj[key] = dict_obj[key]
                    elif (len(ner_obj.get(key)) >= len(dict_obj.get(key))):
                        comb_obj[key] = ner_obj[key]
                    elif (len(dict_obj.get(key)) >= len(ner_obj.get(key))):
                        comb_obj[key] = dict_obj[key]

                if (len(list(set(essence) - set(comb_keys))) == 0):
                    # trim entities fit to intent slot
                    del_keys = set(comb_keys) - set(essence)
                    for key in list(del_keys):
                        del comb_obj[key]
                    share_data.replace_story_slot_entity(comb_obj)
                    len_score = reduce(lambda x, y: x + y, list(map(lambda x: len(comb_obj[x][0]), comb_obj.keys())))
                    extra_score = len(list(comb_obj.keys()))
                    score = 9.5 + len(essence)  + extra_score * 0.3 + len_score * 0.001

            # case7 : predicted intent and ner result do not match but common ner exists
            elif (len(self.common_keys) > 0):
                # get multiple intent which matches with ner result
                logging.info("Case7 : intent do not match but ner matches")
                c_intent_id = self.get_intent_match(self.common_keys)
                share_data.set_intent_id(c_intent_id)

                del_keys = set(self.ner_keys) - set(self.common_keys)
                for key in list(del_keys):
                    del ner_obj[key]
                share_data.replace_story_slot_entity(ner_obj)

                if (len(share_data.get_intent_id()) == 0):
                    share_data.set_intent_id(["-1"])
                score = 5.1 + len(self.common_keys)

            # case9 : error
            else:
                logging.info("Case8 : cannot understand input at all")
                share_data.set_intent_id(["-1"])
                score = -1

            return share_data, score
        except Exception as e :
            raise Exception ("error on scoring {0}".format(e))