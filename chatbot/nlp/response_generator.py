from chatbot.common.chat_share_data import ShareData

class ResponseGenerator(ShareData):

    def __init__(self,  response_story):
        self.response_story = response_story

    def select_response(self, share_data):
        try:
            response = ""
            if(len(self.response_story) > 0):
                response = ' '.join([share_data.get_story_slot_entity(x)[0] for x in self.response_story[0]['fields']['output_entity']['entity']])
                response += self.response_story[0]['fields']['output_data']
                share_data.set_output_data(response)
            else:
                share_data.set_output_data(self.get_unknown_response())
            return share_data
        except Exception as e:
            raise Exception(e)

    def get_unknown_response(self) :
        return "무슨 말씀인지 잘 모르겠어요"

    def tone_generator(self):
        return None
