from chatbot.renponse.response_selection import ResponseSelection

class ResponseGenerator(ResponseSelection):
    """

    """
    def tone_generator(self):
        return None

    def grammar_generator(self):
        return None

    def final_generator(self):
        response = 'Hi I am Bot'
        return response