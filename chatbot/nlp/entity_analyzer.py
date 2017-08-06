from chatbot.common.chat_share_data import ShareData
# from konlpy.tag import Kkma
# from konlpy.tag import Twitter
from chatbot.common.chat_knowledge_mem_dict import ChatKnowledgeMemDict
from konlpy.tag import Mecab
import logging

class EntityAnalyzer(ShareData):
    """
    parse raw text to tageed, entity filterd sentence
    ※ Example
    input : I bought a car yesterday
    output : I bought a car [time]
    """

    def __init__(self, cb_id):
        """
        init global variables
        """
        #self.proper_key_list = sorted(proper_noun.keys(), key=lambda x : proper_noun[x][0], reverse=False) #Sorted Key Priority
        self.cb_id = cb_id
        self.proper_key_list = ChatKnowledgeMemDict.data_order.get(self.cb_id)
        self.proper_noun = ChatKnowledgeMemDict.data.get(self.cb_id).get('proper_noun')     # key : [values]

    def parse(self, share_data):
        """
        parse input with entity list
        :param share_data:
        :return:
        """
        try :
            input_data = share_data.get_request_data()
            pos_tags = self._pos_tagger(input_data)
            logging.info("■■■■■■■■■■ 형태소 분석 결과 : " + str(pos_tags))
            result = list(map(lambda x : self._preprocess_data(share_data,x), pos_tags))
            # Remove preposition
            result = list(filter(lambda x : x[0] != "", result))
            convert_dict_data = list(map(lambda x : x[1] ,result))
            morphed_data = list(map(lambda x : x[0] ,result))
            share_data.set_convert_dict_data(convert_dict_data)
            share_data.set_morphed_data(morphed_data)
            logging.info("■■■■■■■■■■ Entity 분석 결과 : " + str(convert_dict_data))
            return share_data
        except Exception as e :
            raise Exception ("error on entity anal : {0}".format(e))

    #Custom Case : ex)"hi and hello" and len < 3
    def _preprocess_data(self, share_data, pos_tags):
        #except meaningless
        convert_dict_data = pos_tags[0]
        pos_tags_0 = pos_tags[0]
        if (pos_tags[1] in ['NNG', 'NNP','SL'] and len(pos_tags[0]) > 1): #Check only Noun
            key_slot = pos_tags[0]
            key_check = list(filter(lambda x : self._extract_proper_entity(pos_tags[0], x), self.proper_key_list))
            if(key_check == []):
                pass
            else: #proper noun priority
                # except duplicated
                if(self.proper_noun[key_check[0]][2]):
                    key_slot = share_data.get_story_slot_entity(key_check[0])[0] + " " + pos_tags[0] if share_data.get_story_slot_entity(key_check[0]) is not None else "" + pos_tags[0]
                share_data.set_story_slot_entity(key_check[0], [key_slot])
                convert_dict_data = key_check[0]
        elif (pos_tags[1] in ['SY', 'EC', 'EP', 'VA', 'VX', 'XSV+EC', 'VX+EC', 'VX+EF', 'SF', 'VCP+EF', 'ETN', 'ETM', 'JKO', 'EF','VCP+EC','SSO','SSC','EP+EF']):
            return "",""
        return pos_tags_0, convert_dict_data

    def _pos_tagger(self, input, type ='mecab'):
        """

        :param input:
        :return:
        """
        if(type == 'mecab') :
            mecab = Mecab('/usr/local/lib/mecab/dic/mecab-ko-dic')
            return mecab.pos(str(input))
        # elif(type == 'kkma') :
        #     kkma = Kkma()
        #     return kkma.pos(str(input))
        #
        # elif(type == 'twitter') :
        #     twitter = Twitter(jvmpath=None)
        #     return twitter.pos(str(input))

    def _extract_proper_entity(self, value, key):
        exist = False
        value = value.lower()
        input_file = ChatKnowledgeMemDict.data.get(self.cb_id).get(key)
        if(input_file is not None):
            for line in input_file:
                if(self.proper_noun.get(key)[2] and line.lower().strip().find(value) > -1):
                    exist = True
                    break
                elif(line.lower().strip() == value):
                    exist = True
                    break
        return exist