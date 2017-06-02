from chatbot.common.chat_share_data import ShareData
from konlpy.tag import Kkma
from konlpy.tag import Twitter
from konlpy.tag import Mecab
from chatbot.common.chat_knowledge_data_dict import ChatKnowledgeDataDict

class EntityAnalyzer(ShareData):
    """
    parse raw text to tageed, entity filterd sentence
    ※ Example
    input : I bought a car yesterday
    output : I bought a car [time]
    """

    def __init__(self, key_list, entity_types):
        """
        init global variables
        """
        self.entity_key_list = key_list
        self.entity = {}       # key : [values]
        self._load_entity_data(key_list, entity_types)

    def _load_entity_data(self, key_list, temp_entitiy):
        """
        load entity lists
        :return:
        """
        if (len(key_list) == 0) :
            raise Exception ("")

        for key in key_list :
            if key in temp_entitiy :
                self.entity[key] = temp_entitiy[key]
            else :
                self.entity[key] = []

    def parse(self, share_data):
        """
        parse input with entity list
        :param share_data:
        :return:
        """
        if (share_data.get_request_type() == 'image') :
            pass
        else:
            input_data = share_data.get_request_data()
            pos_tags = self._pos_tagger(input_data)
            print ("■■■■■■■■■■ 형태소 분석 결과 : " + str(pos_tags))
            return_msg = ""
            for i in range(0, len(pos_tags)):
                if(pos_tags[i][1] in ['NNG','NNP']):
                    if(self._extract_name_entity(pos_tags[i][0]) == True):
                        pos_tags[i] = (''.join(['[이름]']), '')
                    else:
                        for key in self.entity_key_list:
                            for val in self.entity[key]:
                                word = pos_tags[i][0]
                                if(word == val):
                                    pos_tags[i] = (''.join(['[' , key, ']']), '')
                                    share_data.set_story_entity(key, val)
                                    break
                return_msg = ''.join([return_msg, ' ' , pos_tags[i][0]])
            print ("■■■■■■■■■■ Entity 분석 결과 : " + return_msg)
            share_data.set_convert_data(return_msg)
        return share_data

    def _pos_tagger(self, input, type ='mecab'):
        """

        :param input:
        :return:
        """
        if(type == 'mecab') :
            mecab = Mecab('/usr/local/lib/mecab/dic/mecab-ko-dic')
            return mecab.pos(str(input))

        elif(type == 'kkma') :
            kkma = Kkma()
            return kkma.pos(str(input))

        elif(type == 'twitter') :
            twitter = Twitter(jvmpath=None)
            return twitter.pos(str(input))

    def _extract_name_entity(self, value):
        exist = False
        input_file = open('/home/dev/hoyai/demo/data/name.txt', 'r')
        for line in input_file:
            if(line.strip() == value):
                exist = True
                break
        input_file.close()
        return exist