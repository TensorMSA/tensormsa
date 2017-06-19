from chatbot.common.chat_share_data import ShareData
# from konlpy.tag import Kkma
# from konlpy.tag import Twitter
from konlpy.tag import Mecab
from cluster.service.service_predict_bilstmcrf import PredictNetBiLstmCrf

class EntityAnalyzer(ShareData):
    """
    parse raw text to tageed, entity filterd sentence
    ※ Example
    input : I bought a car yesterday
    output : I bought a car [time]
    """

    def __init__(self, proper_noun, ner_model_id):
        """
        init global variables
        """
        self.ner_model_id = ner_model_id
        self.proper_key_list = list(proper_noun.keys()) #Python 3+ return not list but dict_Keys
        self.proper_noun = proper_noun     # key : [values]
        #self._load_proper_noun(proper_noun.keys(), proper_noun)
        self.bilstmcrf_model = PredictNetBiLstmCrf()

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
        # TODO : Add Intent and NER divide call from service_type 
        input_data = share_data.get_request_data()
        pos_tags = self._pos_tagger(input_data)
        print ("■■■■■■■■■■ 형태소 분석 결과 : " + str(pos_tags))
        result = list(map(lambda x : self._preprocess_data(share_data,x), pos_tags))
        convert_dict_data = list(map(lambda x : x[1].strip() ,result))
        morphed_data = list(map(lambda x : x[0].strip() ,result))
        print ("■■■■■■■■■■ Entity 분석 결과 : " + str(convert_dict_data))
        ner_data = self._get_ner_data(''.join(morphed_data))
        print("■■■■■■■■■■ NER 분석 결과 : " + str(ner_data))
        self._add_ner_slot(morphed_data, ner_data, share_data.get_story_slot_entity())
        convert_data = self._convert_ner_slot(convert_dict_data, ner_data)
        share_data.set_convert_data(convert_data)
        return share_data

    #Custom Case : ex)안녕 and len < 3
    def _preprocess_data(self, share_data, pos_tags):
        #except meaningless
        convert_dict_data = ""
        morphed_data = ""
        if (pos_tags[1] in ['SY', 'SF']):
            pass
        elif (pos_tags[1] in ['NNG', 'NNP']): #Check only Noun
            morphed_data = ''.join([morphed_data, ' ', pos_tags[0]])
            key_check = list(filter(lambda x : self._extract_proper_entity(pos_tags[0], x), self.proper_key_list))
            if(key_check == []):
                pass
            else: #proper noun priority
                share_data.set_story_slot_entity(key_check[0], pos_tags[0])
                pos_tags = (''.join(['['+ key_check[0] +']']), '')
            convert_dict_data = ''.join([convert_dict_data, ' ' , pos_tags[0]])
        else:
            morphed_data = ''.join([morphed_data, ' ', pos_tags[0]])
            convert_dict_data = ''.join([convert_dict_data, ' ', pos_tags[0]])
        return morphed_data, convert_dict_data

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

    # TODO : get nlp DB
    def _extract_proper_entity(self, value, key):
        exist = False
        #input_file = open('/home/dev/hoyai/demo/data/name.txt', 'r')
        input_file = open(self.proper_noun.get(key)[1], 'r')
        if(input_file is not None):
            for line in input_file:
                if(line.strip().find(value) > -1):
                    exist = True
                    break
            input_file.close()
        return exist

    # TODO : get BIO Tag from sentence
    def _get_ner_data(self, input_sentence):
        #result = self.bilstmcrf_model.run(self.ner_model_id, {"input_data": input_sentence, "num": 0, "clean_ans": False})
        result = ['company', 'O', 'name', 'O', 'O', 'rank', 'O', 'O', 'O', 'rank', 'O']
        return result

    def _add_ner_slot(self, morphed_data, ner_data, slot_entity):
        get_ner_list = []
        key_list = self.proper_key_list
        return slot_entity

    def _convert_ner_slot(self, convert_dict_data, ner_data):
        for i in range(len(convert_dict_data)):
            if(ner_data[i].find("company") > -1 and convert_dict_data[i].find("[회사]") > -1):
                pass
            elif(ner_data[i].find("B-") > -1 and convert_dict_data[i].find("[") > -1):
                if(ner_data[i] == "B-PERSON"):
                    convert_dict_data[i] = "[이름]"
                elif(ner_data[i] == "B-LOCATION"):
                    convert_dict_data[i] = "[장소]"
            # Delete Same Entity from dictionary
            elif(ner_data[i].find("I-") > -1 and convert_dict_data[i].find("[") > -1):
                # Compare Prior Entity
                if(i > 0 and convert_dict_data[i] != convert_dict_data[i-1]):
                   del convert_dict_data[i]
            else: # Out Case
                pass
        convert_data = ' '.join(convert_dict_data)
        return convert_data