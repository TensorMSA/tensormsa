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

    #Custom Case : ex)안녕 and len < 3
    def _preprocess_data(self, share_data, pos_tags):
        #except meaningless
        return_msg = ""
        if (pos_tags[1] in ['SY', 'SF']):
            pass
        elif (pos_tags[1] in ['NNG', 'NNP']):
            if (self._extract_proper_entity(pos_tags[0]) == True):
                share_data.set_story_slot_entity('이름', pos_tags[0])
                pos_tags = (''.join(['[이름]']), '')
            return_msg = ''.join([return_msg, ' ' , pos_tags[0]])
        else:
            return_msg = ''.join([return_msg, ' ', pos_tags[0]])
        return return_msg

    def parse(self, share_data):
        """
        parse input with entity list
        :param share_data:
        :return:
        """
        input_data = share_data.get_request_data()
        pos_tags = self._pos_tagger(input_data)
        print ("■■■■■■■■■■ 형태소 분석 결과 : " + str(pos_tags))
        return_msg = ""
        for i in range(0, len(pos_tags)):
            return_msg += self._preprocess_data(share_data, pos_tags[i])
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

    # TODO : get nlp DB
    def _extract_proper_entity(self, value):
        exist = False
        input_file = open('/home/dev/hoyai/demo/data/name.txt', 'r')
        for line in input_file:
            if(line.strip().find(value)):
                exist = True
                break
        input_file.close()
        return exist