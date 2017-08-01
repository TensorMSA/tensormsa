from chatbot.common.chat_share_data import ShareData
from chatbot.services.service_provider import ServiceProvider

class StoryBoardManager(ShareData):

    def __init__(self,  response_story):
        self.response_story = response_story

    def run(self, share_data):
        try:
            if (len(self.response_story) > 0):
                share_data.set_output_data(self.response_story[0]['fields']['output_data'])
            return share_data
        except Exception as e:
            raise Exception(e)



