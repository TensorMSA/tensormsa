from cluster.service.service_predict_cnn import PredictNetCnn
from chatbot.common.chat_conf_manager import ChatBotConfManager
from chatbot.common.chat_share_data import ShareData
from chatbot.nlp.entity_analyzer import EntityAnalyzer
from chatbot.nlp.intend_analyzer import IntendAnalyzer
from chatbot.services.service_provider import ServiceProvider
from chatbot.story.story_board_manager import StoryBoardManager
from chatbot.decision.decision_maker import DecisionMaker
from chatbot.nlp.response_generator import ResponseGenerator
from chatbot.nlp.syntax_analyzer import Syntaxanalyzer
from chatbot.ontology.ontology_manager import OntologyManager
import json

class ServiceManager:
    """
    This is the class where all the chatbot service start
    """
    def __init__(self, cb_id):
        """
        initialze chatbot servic with id
        :param cb_id:
        """
        # TODO : need to use cache for better rsponse time
        self.cb_id = cb_id
        self.chatbot_conf = ChatBotConfManager(cb_id)
        self.chat_share_data = ShareData()
        self.entity_analyzer = EntityAnalyzer(self.chatbot_conf.get_entity_list())
        self.intent_analyzer = IntendAnalyzer(self.chatbot_conf.get_intent_model())
        self.decision_maker = DecisionMaker()
        self.service_provider = ServiceProvider()
        self.story_board = StoryBoardManager(self.chatbot_conf.get_story_board())

    def run_chatbot(self, req_ctx):
        """
        execute chatbot as api mode
        :return:
        """
        try :
            print("■■■■■■■■■■ 챗봇 시작 ■■■■■■■■■■")

            # 1. set parms from client
            share_ctx = self.chat_share_data.load_json(req_ctx)

            # 2. nlp process
            # TODO : kim seung woo
            share_ctx = self.entity_analyzer.parse(share_ctx)
            share_ctx = self.intent_analyzer.parse(share_ctx)

            # 3. decision maker
            # TODO : kim su sang
            share_ctx = self.decision_maker.run(share_ctx)
            print("■■■■■■■■■■ 챗봇 끝 ■■■■■■■■■■")
            # 4. return result as json
            return share_ctx.to_json()
        except Exception as e :
            raise Exception (e)


    def run_chatbot_with_file(self, req_ctx):
        """
        uplaod files
        :return:
        """
        PredictNetCnn().run("", "", req_ctx)
