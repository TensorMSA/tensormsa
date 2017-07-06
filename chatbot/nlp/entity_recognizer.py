from chatbot.common.chat_share_data import ShareData
from cluster.service.service_predict_bilstmcrf import PredictNetBiLstmCrf
import ngram
from chatbot.common.chat_knowledge_mem_dict import ChatKnowledgeMemDict
from collections import Counter

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
        ner_data = self._get_ner_data(' '.join(share_data.get_morphed_data()))
        share_data = self._match_ngram_dict(share_data , share_data.get_morphed_data(), ner_data)
        self._get_convert_data(ner_data, share_data)
        print("■■■■■■■■■■ NER 분석 결과 : " + str(ner_data))
        return share_data

    def _get_convert_data(self, ner_data, share_data):
        """
        make sentence for charn cnn intent prediction 
        :param ner_data: 
        :param share_data: 
        :return: 
        """
        buff_list = []
        for val_a, val_b in zip(ner_data, share_data.get_morphed_data()) :
            if(val_a == 'O') :
                buff_list.append(val_b)
            else :
                buff_list.append(val_a)
        share_data.set_convert_data(sorted(set(buff_list), key=lambda x: buff_list.index(x)))

    def _get_ner_data(self, input_sentence):
        result = self.bilstmcrf_model.run(self.ner_model_id, {"input_data": input_sentence, "num": 0, "clean_ans": False})
        return result

    def _match_ngram_dict(self, share_data, input_sentence, ner_data):
        """
        match ngram dict with ner analized 
        :return: 
        """
        try :
            result = {}
            if (len(input_sentence) != len(ner_data)):
                print("■■■■■■■■■■ 길이 차이로 NER 처리 불가 ■■■■■■■■■■")
                pass

            if(ChatKnowledgeMemDict.ngram.get(self.cb_id) == None) :
                cb_data = ChatKnowledgeMemDict.data.get(self.cb_id)
                dist_keys = dict(Counter(ner_data))
                for key, val in zip(ner_data, input_sentence) :
                    if (key == 'O') :
                        continue
                    model = ngram.NGram(cb_data.get(key))
                    if(dist_keys.get(key) > 1) :
                        ner_conv = ' '.join(list(map(lambda x : x[0], list(filter(lambda x : x[1] == key, zip(input_sentence,ner_data))))))
                        result[key] = list(map(lambda x : x[0], model.search(ner_conv, threshold=1.0)))
                        if(len(result[key]) == 0) :
                            result[key] = list(map(lambda x : x[0], model.search(ner_conv, threshold=0.2)))[0:4]
                    else :
                        result[key] = list(map(lambda x: x[0], model.search(val, threshold=1.0)))
                        if (len(result[key]) == 0):
                            result[key] = list(map(lambda x : x[0], model.search(val, threshold=0.2)))[0:4]
                    if(len(result[key]) == 0) :
                        del result[key]
                    else :
                        share_data.set_story_ner_entity(key, result[key])
            return share_data
        except Exception as e :
            raise Exception ("Error on matching ngram afger bilstm crf : {0}".format(e))