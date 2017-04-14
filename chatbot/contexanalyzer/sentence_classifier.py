from chatbot.contexanalyzer.intend_analyzer import IntendAnalyzer
from cluster.service.service_predict_w2v import PredictNetW2V

#first step to classifier
class SentenceClassifier:

    def classify_domain(self, sentence):

        try:
            print ("◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆  3) 연관 업무 분류")
            intend = IntendAnalyzer().intend_analyzer(sentence)
            return intend

        except Exception as e:
            raise Exception(e)

    def word_embedding(self, sentence):
        try:
            return_data = "회의"
            simular_data = PredictNetW2V().run("nn00002", {
                "type": "sim",
                "val_1": ["회장"],
                "val_2": [""]
            })
            print("◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆ Word Embedding 결과 출력 {0}".format(simular_data))
            return simular_data
        except Exception as e:
         raise Exception(e)