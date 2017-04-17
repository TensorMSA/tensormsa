from chatbot.decisionmaker.make_decision import MakeDecision
from chatbot.contexanalyzer.sentence_classifier import SentenceClassifier
from chatbot.contexanalyzer.analyze_sentence import AnalyzeSentence
from chatbot.services.task_manager import TaskManager
from chatbot.renponse.response_selection import ResponseSelection
from chatbot.manager.configurate_setting import ConfigureSetting
from chatbot.decisionmaker.make_decision import MakeDecision
import json
#first step to classifier
class ServiceManager:

    def run_console(self):

        try:
            print("◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆ 2) 챗봇 실행 ◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆  ")
            response ="Finished Chatbot"
            while (True):
                question = "테스트값 있을때"
                question = input("Q:")
                print(question)
                if(question == "end") :
                     break

                #Get Entiiy
                #TODO:swkim
                entity = AnalyzeSentence().get_entity_value(question)
                get_prefix = ConfigureSetting().prefix_type()
                get_model_list = ConfigureSetting().get_model_list('c00001')
                intend = SentenceClassifier().classify_domain(question)

                #TODO:sskim
                wordEmbedding = SentenceClassifier().word_embedding(question)
                service_param = "Image Path"
                service_exist = MakeDecision().get_story_board(intend, entity, service_param)
                #response = ResponseSelection().select_response(intend)
                if(service_exist == True) :
                    service = TaskManager().serviceCall(intend, entity)
                    break

            print("◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆ 6) End Chat Bot")
            return response

        except Exception as e:
            raise Exception(e)

    def run_chatbot(self):
        """
        execute chatbot as api mode
        :return:
        """
        pass

    def run_chatbot_with_file(self):
        """
        uplaod files
        :return:
        """
        pass
