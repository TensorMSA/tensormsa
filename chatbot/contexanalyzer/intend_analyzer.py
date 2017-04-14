from cluster.service.service_predict_seq2seq import PredictNetSeq2Seq

#second step to find intend
class IntendAnalyzer:

    def intend_analyzer(self, sentence):
        print("◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆  4) 의도 분석")
        predict_class = PredictNetSeq2Seq()
        intend = predict_class.run("nn000998", {"input_data" : sentence })
        print("◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆  5) 의도 분석 결과 출력 {0}".format(intend))
        return intend

    def intend_classifier(self, sentence):
        sentence_temp = sentence
        return None