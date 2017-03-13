from chatbot.contexanalyzer.disintegrate_sentence import disintegrate_sentence

#first step to classifier
class SentenceClassifier():
    def classify_domain(self, QuestionString):
        disintegrate_sentence(QuestionString)
        print(QuestionString)
        return None

    def callSyntaxnet(self,text):

        return

