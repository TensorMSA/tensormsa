from chatbot.common.chat_conf_manager import ChatBotConfManager
import json

class ShareData(ChatBotConfManager):
    """
    share data class is data component which includes json2object and object2json maethod
    the purpose of this class is mainly on keep conversation data on thread
    beacuse this api works on rest api we need some info like cookie that where we were on
    the last convrsation
    """
    def __init__(self):
        """

        :return:
        """
        # self.unique_id = ""             # mobile device unique id
        # self.package_id = ""            # mobile app package id
        self.input_data = None            # prediction requested data
        self.convert_data = None          # convert data
        self.output_data = None           # output data
        self.edit_history = []            # data change history (preprocess -> tag -> NER)
        self.intent_history = []          # intent change history (changes on intent model)
        self.request_type = ""            # text, image, voice
        self.intent_id = ""               # current intent id
        # self.intent_name = ""           # current intent name
        self.service_type = ""            # I:Intent, N:NER
        self.story_board_id = ""          # current working story board
        self.story_key_entity = []        # required key list
        self.story_slot_entity = {}       # key : val
        self.story_ner_entity = {}        # key : val
        self.morphed_data = []
        self.convert_dict_data =[]
        self.pattern_intent_id = ""
        self.test_intent_id = ""
        self.test_slot_entity = {}

        # self.opt_sel_list = {}          # intent option list when intent anl result is not clear
        # self.ontology_id = ""           # current working ontology id
        # self.ontology_req_parms = {}    # key : val
        # self.ontology_set_parms = {}    # key : val

    def to_json(self):
        """
        convert data object to json
        :return:
        """
        return json.dumps(self.__dict__, ensure_ascii=False)

    def load_json(self, object):
        """
        load josn object to data object
        :param object:
        :return:
        """
        object = self._check_json_validation(object)
        self.__dict__.update(object)
        return self

    def _check_json_validation(self, object):
        """
        check json format is right
        :param object:
        :return:
        """
        # Check Essential Input
        for key in ['input_data', 'intent_id']:
            if key not in object :
                raise Exception (''.join([key, ' not exist!']))

        #Check Length of String
        self._check_string_length(object.get("input_data"))

        for key in ['story_slot_entity', 'story_ner_entity', 'test_slot_entity'] :
            if key in list(object.keys()) :
                object[key] = {}
        return object

    def _check_string_length(self, input_data):
        if(len(input_data) > 50):
            raise Exception('Input Data is too long')

    def merge_share_data(self, output_share_data):
        """
        simply update all info on this class to output_share_data
        :param input_share_data:
        :return:
        """
        pass

    def _clear_conv_data(self):
        """
        clear story board, clear ontology data
        :return:
        """
        pass

    # def set_device_id(self, data):
    #     """
    #
    #     :param data:
    #     :return:
    #     """
    #     self.unique_id = data
    #
    # def get_device_id(self):
    #     """
    #
    #     :param data:
    #     :return:
    #     """
    #     return self.unique_id

    # def set_package_id(self, data):
    #     """
    #
    #     :param data:
    #     :return:
    #     """
    #     self.package_id = data
    #
    # def get_package_id(self):
    #     """
    #
    #     :param data:
    #     :return:
    #     """
    #     return self.package_id

    def set_chatbot_id(self, data):
        """

        :param data:
        :return:
        """
        self.chatbot_id = data

    def get_chatbot_id(self):
        """

        :param data:
        :return:
        """
        return self.chatbot_id

    def set_intent_id(self, data):
        """

        :param data:
        :return:
        """
        self.intent_id = data

    def get_intent_id(self):
        """

        :param data:
        :return:
        """
        return self.intent_id

    def set_pattern_intent_id(self, data):
        """

        :param data:
        :return:
        """
        self.pattern_intent_id = data

    def get_pattern_intent_id(self):
        """

        :param data:
        :return:
        """
        return self.pattern_intent_id

    # def set_intent_name(self, data):
    #     """
    #
    #     :param data:
    #     :return:
    #     """
    #     self.intent_name = data
    #
    # def get_intent_name(self):
    #     """
    #
    #     :param data:
    #     :return:
    #     """
    #     return self.intent_name

    def set_input_data(self, data):
        """

        :param data:
        :return:
        """
        self.input_data = data

    def get_input_data(self):
        """

        :param data:
        :return:
        """
        return self.input_data

    def set_request_data(self, data):
        """
        intent id
        :param intent_id:
        :return:
        """
        self.input_data = data

    def get_request_data(self):
        """
        intent id
        :param intent_id:
        :return:
        """
        return self.input_data

    def set_convert_data(self, data):
        """
        intent id
        :param intent_id:
        :return:
        """
        self.convert_data = data

    def get_convert_data(self):
        """
        intent id
        :param intent_id:
        :return:
        """
        return self.convert_data

    def set_output_data(self, data):
        """
        intent id
        :param intent_id:
        :return:
        """
        self.output_data = data

    def get_output_data(self):
        """
        intent id
        :param intent_id:
        :return:
        """
        return self.output_data

    def set_edit_history(self, edit_type):
        """
        intent id
        :param intent_id:
        :return:
        """
        self.edit_history.append(edit_type)

    def get_edit_history(self):
        """
        intent id
        :param intent_id:
        :return:
        """
        return self.edit_history

    def set_intent_history(self, intent_id):
        """
        intent id
        :param intent_id:
        :return:
        """
        self.intent_history.append(intent_id)

    def get_intent_history(self):
        """
        intent id
        :param intent_id:
        :return:
        """
        return self.intent_history

    def set_request_type(self, data):
        """
        manage request type
        :param data:
        :return:
        """
        self.request_type = data

    def get_request_type(self):
        """
        manage request type
        :param data:
        :return:
        """
        return self.request_type

    def set_service_type(self, data):
        """

        :param data:
        :return:
        """
        self.service_type = data

    def get_service_type(self):
        """

        :param data:
        :return:
        """
        return self.service_type

    def set_story_id(self, data):
        """

        :param data:
        :return:
        """
        self.story_board_id = data

    def get_story_id(self):
        """

        :param data:
        :return:
        """
        return self.story_board_id

    def set_story_key_entity(self, data):
        """

        :param data:
        :return:
        """
        self.story_key_entity = data

    def get_story_key_entity(self):
        """

        :param data:
        :return:
        """
        return self.story_key_entity

    def set_morphed_data(self, data):
        """

        :param data:
        :return:
        """
        self.morphed_data = data

    def get_morphed_data(self):
        """

        :param data:
        :return:
        """
        return self.morphed_data

    def set_convert_dict_data(self, data):
        """

        :param data:
        :return:
        """
        self.convert_dict_data = data

    def get_convert_dict_data(self):
        """

        :param data:
        :return:
        """
        return self.convert_dict_data

    def set_story_slot_entity(self, key, val):
        """

        :param data:
        :return:
        """
        self.story_slot_entity[key] = val

    def replace_story_slot_entity(self, obj):
        """
        manage result of ner(bilstmcrf algoritm) result 
        :param data:
        :return:
        """
        self.story_slot_entity = obj

    def update_story_slot_entity(self, key, val):
        """

        :param data:
        :return:
        """
        if(key not in list(self.story_slot_entity.keys())) :
            self.story_slot_entity[key] = val

    def get_story_slot_entity(self, key = None):
        """

        :param data:
        :return:
        """
        if(key) :
            return self.story_slot_entity.get(key)
        else :
            return self.story_slot_entity

    def initialize_story_entity(self):
        self.story_slot_entity = {}

    def initialize_story(self):
        self.story_slot_entity = {}
        self.set_story_id("")
        self.set_intent_id("")
        self.set_request_data("")
        self.initialize_story_entity()
        self.set_request_type("")

    def get_story_ner_entity(self):
        """
        manage result of ner(bilstmcrf algoritm) result 
        :param data:
        :return:
        """
        return self.story_ner_entity

    def set_story_ner_entity(self, key, val):
        """
        manage result of ner(bilstmcrf algoritm) result 
        :param data:
        :return:
        """
        self.story_ner_entity[key] = val

    def replace_story_ner_entity(self, obj):
        """
        manage result of ner(bilstmcrf algoritm) result 
        :param data:
        :return:
        """
        self.story_ner_entity = obj


    def add_extra_client_data(self):
        """
        add extra data for client 
        :return: 
        """
        self.story_slot_entity = self.convert_to_list_shape(self.story_slot_entity)
        self.story_ner_entity = self.convert_to_list_shape(self.story_ner_entity)
        self.test_slot_entity = self.convert_to_list_shape(self.test_slot_entity)
        return self

    def add_test_client_data(self):
        """
        add unchanged info for client test
        :return: 
        """
        self.intent_id = list(set(self.intent_id))
        self.test_intent_id = self.intent_id.copy()
        self.test_slot_entity = self.story_slot_entity.copy()
        return self

    def convert_to_list_shape(self, input):
        """
        convert dict to list-dict (client developer request) 
        :param input: 
        :return: 
        """
        buffer = []
        for key in input.keys() :
            buffer.append({"key" : key, "val" :input[key]})
        return buffer