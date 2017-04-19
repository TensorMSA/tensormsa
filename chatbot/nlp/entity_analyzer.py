from chatbot.common.chat_share_data import ShareData
from konlpy.tag import Kkma
from konlpy.tag import Twitter
from konlpy.tag import Mecab

class EntityAnalyzer(ShareData):
    """
    parse raw text to tageed, entity filterd sentence
    ※ Example
    input : I bought a car yesterday
    output : I bought a car [time]
    """

    def __init__(self, key_list):
        """
        init global variables
        """
        self.entity_key_list = key_list
        self.entity = {}       # key : [values]
        self._load_entity_data(key_list)

    def _load_entity_data(self, key_list):
        """
        load entity lists
        :return:
        """
        if (len(key_list) == 0) :
            raise Exception ("")

        #TODO : need to get data from db or cache
        #['이름', '직급', '직책', '근태코드', '실', 'Grade', '그룹', '근무조', '부', '지역']
        temp_entitiy = {}
        temp_entitiy['이름'] = ['김승우', '김수상']
        temp_entitiy['직책'] = ['팀장', '일반']
        temp_entitiy['직급'] = ['사원', '대리', '과장', '차장' , '부장']
        temp_entitiy['근태코드'] = ['휴가', '연차', '반차']
        temp_entitiy['Grade'] = ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9']
        temp_entitiy['그룹'] = ['']
        temp_entitiy['근무조'] = ['']
        temp_entitiy['부'] = ['']
        temp_entitiy['지역'] = ['서울', '판교', '포항', '광양']

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
            return share_data

        input_data = share_data.get_request_data()
        pos_tags = self._pos_tagger(input_data)
        return_msg = ""

        for i in range(0, len(pos_tags)):
            for key in self.entity_key_list:
                for val in self.entity[key] :
                    word = pos_tags[i][0]
                    if(word == val) :
                        pos_tags[i] = (''.join(['[' , key, ']']), '')
                        share_data.set_story_entity(key, val)
                        break
            return_msg = ''.join([return_msg, ' ' , pos_tags[i][0]])
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
