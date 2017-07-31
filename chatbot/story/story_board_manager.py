from chatbot.common.chat_share_data import ShareData
from chatbot.services.service_provider import ServiceProvider

class StoryBoardManager(ShareData):

    def __init__(self,  response_story):
        self.response_story = response_story

    def run(self, share_data):
        try:
            if (share_data.get_service_type() == "find_image") :
                share_data = self._call_service_provider(share_data)
            else :
                if (share_data.get_output_data() == ""):
                    share_data = share_data.set_output_data("자세히 말씀해 주세요")
                    #share_data._initailize_story()
            return share_data
        except Exception as e:
            raise Exception(e)

    def _call_service_provider(self, share_data):
        share_data = ServiceProvider().run(share_data)
        return share_data


