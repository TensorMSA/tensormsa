from chatbot.common.chat_share_data import ShareData

class ResponseGenerator(ShareData):
    """

    """
    def tone_generator(self):
        return None

    def grammar_generator(self):
        return None

    def final_generator(self):
        response = 'Hi I am Bot'
        return response