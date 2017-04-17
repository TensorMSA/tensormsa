from chatbot.renponse.response_selection import ResponseSelection

class MakeDecision:

    def get_story_board(self, intend, entity, service_param):
        service_exist = False
        if (intend == " 1"):
            service_exist = True
            if ('이미지' in entity):
                response = ResponseSelection().get_image_response()
        else :
            response = ResponseSelection().select_response(intend)

        return service_exist