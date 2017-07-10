from chatbot.common.chat_share_data import ShareData
# from konlpy.tag import Kkma
# from konlpy.tag import Twitter
from konlpy.tag import Mecab
from cluster.service.service_predict_bilstmcrf import PredictNetBiLstmCrf
import logging

class EntityAnalyzer(ShareData):
    """
    parse raw text to tageed, entity filterd sentence
    ※ Example
    input : I bought a car yesterday
    output : I bought a car [time]
    """

    def __init__(self, proper_noun):
        """
        init global variables
        """
        self.proper_key_list = sorted(proper_noun.keys(), key=lambda x : proper_noun[x][0], reverse=False) #Sorted Key Priority
        self.proper_noun = proper_noun     # key : [values]
        #self._load_proper_noun(proper_noun.keys(), proper_noun)
        #self.bilstmcrf_model = PredictNetBiLstmCrf()

    # Compare load all file and Step by Step (Step is faster
    # def _load_proper_noun(self, key_list, proper_noun):
    #     """
    #     load entity lists
    #     :return:
    #     """
    #     if (len(key_list) == 0) :
    #         raise Exception ("")
    #
    #     for key in key_list :
    #         if key in proper_noun :
    #             self.peoper_noun_values[key] = proper_noun[key]
    #             #compare file r/w
    #             #self._load_proper_file(key, proper_noun[key])
    #         else :
    #             self.peoper_noun_values[key] = []
    #
    # def _load_proper_file(self, key, path):
    #     input_file = open(path, 'r')
    #     noun_values=[]
    #     for line in input_file:
    #         noun_values.append(line)
    #     self.peoper_noun_values[key] = noun_values
    #     input_file.close()

    def parse(self, share_data):
        """
        parse input with entity list
        :param share_data:
        :return:
        """
        try :
            # TODO : Add Intent and NER divide call from service_type
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

    #Custom Case : ex)안녕 and len < 3
    def _preprocess_data(self, share_data, pos_tags):
        #except meaningless
        convert_dict_data = pos_tags[0]
        if (pos_tags[1] in ['SY','EC','EP','VA','VX','XSV+EC','VX+EC','VX+EF','SF']):
            return "",""
        elif (pos_tags[1] in ['NNG', 'NNP','SL'] and len(pos_tags[0]) > 1): #Check only Noun
            key_check = list(filter(lambda x : self._extract_proper_entity(pos_tags[0], x), self.proper_key_list))
            if(key_check == []):
                pass
            else: #proper noun priority
                key_slot = pos_tags[0]
                # except duplicated
                if(self.proper_noun[key_check[0]][2]):
                    key_slot = share_data.get_story_slot_entity(key_check[0])[0] + pos_tags[0] if share_data.get_story_slot_entity(key_check[0]) is not None else "" + pos_tags[0]
                share_data.set_story_slot_entity(key_check[0], [key_slot])
                convert_dict_data = key_check[0]

        return pos_tags[0], convert_dict_data

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
        #input_file = open('/home/dev/hoyai/demo/data/name.txt', 'r')
        input_file = open(self.proper_noun.get(key)[1], 'r')
        if(input_file is not None):
            for line in input_file:
                if(self.proper_noun.get(key)[2] and line.strip().find(value) > -1):
                    exist = True
                    break
                elif(line.strip() == value):
                    exist = True
                    break
            input_file.close()
        return exist
