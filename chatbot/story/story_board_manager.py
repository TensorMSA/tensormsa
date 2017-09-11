from chatbot.common.chat_share_data import ShareData
from chatbot.nlp.response_generator import ResponseGenerator

class StoryBoardManager(ShareData):

    def __init__(self,  response_story):
        self.response_story = response_story

    def run(self, share_data):
        try:
            if (len(self.response_story) > 0 and self.response_story[0]['fields']['response_type'] == 'entity'):
                share_data = ResponseGenerator(self.response_story).select_response(share_data)
            else:
                share_data.set_output_data(self.response_story[0]['fields']['output_data'])
            return share_data
        except Exception as e:
            raise Exception(e)



