from chatbot import models
from django.core import serializers as serial
import json

class ChatBotConfManager:
    """
    class which handle chabot conf include nlp, stroyboard, entity and service
    (1) on prepare time : set confs for chat bot
    (2) on run time : get confs from db and provide getter for essential values
    """

    def __init__(self, cb_id):
        """
        init global variables
        """
        self.pos_type = ""
        self.entity_key_list = []
        self.word_embed_model = ""
        self.intent_analyze_model = ""
        self.ner_analyze_model = ""
        self.resp_gen_model = ""
        self.ton_gen_model = ""
        self.stroy_board = []     #available story_board lists
        self._restore_conf(cb_id)

    def _restore_conf(self, cb_id):
        """
        restore conf data from db
        :param cb_id:
        :return:
        """
        #TODO:need to get data from cache server and chatbot model DB
        self.pos_type = "mecab"
        self.word_embed_model = "nn00002"
        self.pattern_intent_analyze_model = self.get_model_conf(cb_id, 'PIntent')['nn_id']
        self.intent_analyze_model = self.get_model_conf(cb_id, 'Intent')['nn_id']
        self.ner_analyze_model = self.get_model_conf(cb_id, 'NER')['nn_id']
        self.resp_gen_model = ""
        self.ton_gen_model = ""
        self.stroy_board = []

    def get_model_conf(self, cb_id, purpose):
        try :
            query_set = models.CB_MODEL_LIST_INFO.objects.filter(cb_id = cb_id, nn_purpose = purpose)
            query_set = serial.serialize("json", query_set)
            return json.loads(query_set)[0]['fields']
        except Exception as e :
            raise Exception ("Model for {0} is required : {1}".format(purpose, e))

    def get_pattern_intent_model(self):
        """
        tag type mecab, twitter, etc
        :param data:
        :return:
        """
        return self.pattern_intent_analyze_model

    def get_intent_model(self):
        """
        tag type mecab, twitter, etc
        :param data:
        :return:
        """
        return self.intent_analyze_model

    def _save_conf(self, cb_id):
        """
        restore conf data from db
        :param cb_id:
        :return:
        """
        #TODO:need to save conf data into db
        pass

    def _set_cache(self, conf_data):
        """
        set conf data on cache server
        :param data_conf:
        :return:
        """
        pass

    def set_entity_list(self, data):
        """
        set entity list to use
        :param data:
        :return:
        """
        self.entity_key_list.append(data)

    def get_entity_list(self):
        """
        get entity list to use
        :param data:
        :return:
        """
        return self.entity_key_list

    def set_word_embed_model(self, data):
        """
        set word embed model (w2v.. )
        :param data:
        :return:
        """
        self.word_embed_model = data

    def get_word_embed_model(self):
        """
        get word embed model (w2v.. )
        :param data:
        :return:
        """
        return self.word_embed_model

    def set_pos_type(self, data):
        """
        tag type mecab, twitter, etc
        :param data:
        :return:
        """
        self.pos_type = data

    def get_pos_type(self):
        """
        tag type mecab, twitter, etc
        :param data:
        :return:
        """
        return self.pos_type

    def set_ner_model(self, data):
        """
        net id pretrained on hoyai
        :param data:
        :return:
        """
        self.ner_analyze_model = data

    def get_ner_model(self):
        """
        net id pretrained on hoyai
        :param data:
        :return:
        """
        return self.ner_analyze_model

    def set_resp_model(self, data):
        """
        net id pretrained on hoyai
        :param data:
        :return:
        """
        self.resp_gen_model = data

    def get_resp_model(self):
        """
        net id pretrained on hoyai
        :param data:
        :return:
        """
        return self.resp_gen_model

    def set_ton_model(self, data):
        """
        net id pretrained on hoyai
        :param data:
        :return:
        """
        self.ton_gen_model = data

    def get_ton_model(self):
        """
        net id pretrained on hoyai
        :param data:
        :return:
        """
        return self.ton_gen_model

    def set_story_board(self, data):
        """
        net id pretrained on hoyai
        :param data:
        :return:
        """
        self.stroy_board = data

    def get_story_board(self):
        """
        net id pretrained on hoyai
        :param data:
        :return:
        """
        return self.stroy_board