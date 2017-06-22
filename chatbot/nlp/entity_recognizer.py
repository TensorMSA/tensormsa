from chatbot.common.chat_share_data import ShareData
from cluster.service.service_predict_bilstmcrf import PredictNetBiLstmCrf

class EntityRecognizer(ShareData):

    def __init__(self, cb_id, ner_model_id):
        """
        init global variables
        """
        self.cb_id = cb_id
        self.ner_model_id = ner_model_id
        self.bilstmcrf_model = PredictNetBiLstmCrf()

    def parse(self, share_data):
        print("■■■■■■■■■■ NER 분석 전 : " + str(share_data.get_morphed_data()))
        ner_data = self._get_ner_data(''.join(share_data.get_morphed_data()))
        print("■■■■■■■■■■ NER 분석 결과 : " + str(ner_data))
        self._add_ner_slot(share_data.get_morphed_data(), ner_data, share_data.get_story_slot_entity())
        convert_data = self._convert_ner_slot(share_data.get_convert_dict_data(), ner_data)
        share_data.set_convert_data(convert_data)
        return share_data

    # TODO : get BIO Tag from sentence
    def _get_ner_data(self, input_sentence):
        #result = self.bilstmcrf_model.run(self.ner_model_id, {"input_data": input_sentence, "num": 0, "clean_ans": False})
        result = ['B-DEPT','B-DEPT', 'B-PERSON', 'B-DEPT', 'O', 'NAME', 'RANK', 'O', 'O']
        return result

    def _add_ner_slot(self, morphed_data, ner_data, slot_entity):
        get_ner_list = []
        #key_list = self.proper_key_list
        return slot_entity

    def _convert_ner_slot(self, convert_dict_data, ner_data):

        if(len(convert_dict_data) != len(ner_data)):
            print("■■■■■■■■■■ 길이 차이로 NER 처리 불가 ■■■■■■■■■■")
        else:
            for i in range(len(convert_dict_data)):
                if(ner_data[i].find("B-COMPANY") > -1 and convert_dict_data[i].find("[회사]") > -1):
                    pass
                # not Dict but NER
                elif(ner_data[i].find("B-") > -1 and convert_dict_data[i].find("[") == -1):
                    if(ner_data[i] == "B-PERSON"):
                        convert_dict_data[i] = "[이름]"
                    elif(ner_data[i] == "B-LOCATION"):
                        convert_dict_data[i] = "[장소]"
                    elif(ner_data[i] == "B-DEPT"):
                        convert_dict_data[i] = "[부서]"
                # Delete Same Entity from dictionary
                elif(ner_data[i].find("I-") > -1 and convert_dict_data[i].find("[") > -1):
                    # Compare Prior Entity
                    if(i > 0 and convert_dict_data[i] != convert_dict_data[i-1]):
                       del convert_dict_data[i]
                else: # Out Case
                    pass
        # Remove Distinct
        convert_data = ' '.join(sorted(set(convert_dict_data), key = convert_dict_data.index))
        print("■■■■■■■■■■ NER 변화 결과 : " + str(convert_data))
        return convert_data