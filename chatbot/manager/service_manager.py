from cluster.service.service_predict_cnn import PredictNetCnn
from chatbot.common.chat_conf_manager import ChatBotConfManager
from chatbot.common.chat_share_data import ShareData
from chatbot.nlp.entity_synonym import EntitySynonym
from chatbot.common.chat_knowledge_data_dict import ChatKnowledgeDataDict
from chatbot.nlp.entity_analyzer import EntityAnalyzer
from chatbot.nlp.rule_intent_analyzer import RuleIntentAnalyzer
from chatbot.nlp.intend_analyzer import IntendAnalyzer
from chatbot.nlp.entity_recognizer import EntityRecognizer
from chatbot.manager.service_mapper import ServiceMapper
from chatbot.decision.summrize_result import SummrizeResult
import threading, logging
from chatbot.decision.decision_maker import DecisionMaker
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
        try :
            self.cb_id = cb_id
            self.chatbot_conf = ChatBotConfManager(cb_id)
            self.chat_knowledge_data_dict = ChatKnowledgeDataDict(cb_id)
            self.chat_knowledge_data_dict.initialize(cb_id)
            self.chat_share_data = ShareData()
            self.entity_synonym = EntitySynonym(cb_id)
            self.entity_analyzer = EntityAnalyzer(cb_id)
            self.rule_intent_analyzer = RuleIntentAnalyzer(self.chat_knowledge_data_dict.get_intent_conf("custom"))
            self.entity_recognizer = EntityRecognizer(cb_id,self.chatbot_conf.get_ner_model())
            self.intent_analyzer_rule = IntendAnalyzer(cb_id,self.chatbot_conf.get_intent_model())
            self.intent_analyzer_ner = IntendAnalyzer(cb_id,self.chatbot_conf.get_pattern_intent_model())
            self.decision_maker = DecisionMaker(self.chat_knowledge_data_dict)
            self.service_mapper = ServiceMapper(cb_id, self.entity_synonym)
            self.summrize_result = SummrizeResult(self.chat_knowledge_data_dict)
        except Exception as e :
            raise Exception ("error on ChatBot ServiceManager init process : {0}".format(e))

    class ThreadCls(threading.Thread) :
        def __init__(self, input, func, type):
            threading.Thread.__init__(self)
            self.input = input
            self.ret = None
            self.func = func
            self.type = type

        def run(self):
            self.ret = self.func(self.input, self.type)

        def join(self):
            threading.Thread.join(self)
            return self.ret


    def run_chatbot(self, req_ctx, mode='none'):
        """
        execute chatbot as api mode
        :return:
        """
        try :
            logging.info("■■■■■■■■■■ 챗봇 시작 ■■■■■■■■■■")
            ### UUID mapping ###

            ### set parms from client ###
            share_ctx = self.chat_share_data.load_json(req_ctx)

            ### get rule intent ###
            rule_intent = self.rule_intent_analyzer.parse(share_ctx)

            ### nlp process ###
            if(not rule_intent):
                share_ctx = self.entity_analyzer.parse(share_ctx)
                share_ctx = self.entity_recognizer.parse(share_ctx)

                if(mode == 'thread'):
                    logging.info("■■■■■■■■■■ Thread Mode ■■■■■■■■■■")
                    job_list = [
                                self.ThreadCls(share_ctx, self.intent_analyzer_rule.parse, 'Rule'),
                                self.ThreadCls(share_ctx, self.intent_analyzer_ner.parse, 'NER')]
                    for job in job_list:
                        job.start()

                    for job in job_list:
                        share_ctx.__dict__.update(job.join().__dict__)
                else :
                    logging.info("■■■■■■■■■■ None Thread Mode ■■■■■■■■■■")
                    share_ctx = self.intent_analyzer_rule.parse(share_ctx, 'Rule')
                    share_ctx = self.intent_analyzer_ner.parse(share_ctx, 'NER')

                ### summrize result ###
                share_ctx = self.summrize_result.parse(share_ctx)

            share_ctx.add_test_client_data()

            ### decision maker ###
            share_ctx = self.decision_maker.run(share_ctx)

            ### UUID mapping ###
            share_ctx = self.service_mapper.run(share_ctx)

            logging.info("■■■■■■■■■■ 챗봇 끝 ■■■■■■■■■■")
            ### 4. return result as json ###
            share_ctx = share_ctx.add_extra_client_data()
            return share_ctx.to_json()
        except Exception as e:
            raise Exception (e)


    def run_chatbot_with_file(self, req_ctx):
        """
        uplaod files
        :return:
        """
        PredictNetCnn().run("", "", req_ctx)
