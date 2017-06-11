from chatbot.common.chat_share_data import ShareData
# from konlpy.tag import Kkma
# from konlpy.tag import Twitter
from konlpy.tag import Mecab

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
        self.entity_key_list = proper_noun.keys()
        self.peoper_noun_values = {}       # key : [values]
        self._load_proper_noun(proper_noun.keys(), proper_noun)

    def _load_proper_noun(self, key_list, proper_noun):
        """
        load entity lists
        :return:
        """
        if (len(key_list) == 0) :
            raise Exception ("")

        for key in key_list :
            if key in proper_noun :
                self.peoper_noun_values[key] = proper_noun[key]
                #compare file r/w
                #self._load_proper_file(key, proper_noun[key])
            else :
                self.peoper_noun_values[key] = []

    def _load_proper_file(self, key, path):
        input_file = open(path, 'r')
        noun_values=[]
        for line in input_file:
            noun_values.append(line)
        self.peoper_noun_values[key] = noun_values
        input_file.close()

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
        # TODO : Add Intent and NER divide call from service_type 
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
            if(line.strip().find(value) == 0):
                exist = True
                break
        input_file.close()
        return exist