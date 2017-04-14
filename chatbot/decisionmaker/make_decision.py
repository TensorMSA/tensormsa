from chatbot.renponse.response_generator import ResponseGenerator

class MakeDecision:

    def make_response(self):
        return ResponseGenerator().final_generator()