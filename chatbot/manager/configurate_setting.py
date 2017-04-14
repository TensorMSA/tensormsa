class ConfigureSetting:

    def prefix_type(self):
        SENTENCES_PREFIX = ['Q: ', 'A: ']
        return SENTENCES_PREFIX

    def get_model_list(self, chat_id):
        model_list = ['nn00004', 'nn00002']
        return model_list
