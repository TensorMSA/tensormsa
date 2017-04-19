from chatbot.common.chat_share_data import ShareData
from chatbot.services.service_provider import ServiceProvider

class StoryBoardManager(ShareData):
    """

    """

    def __init__(self, story_board_id):
        """
        init global variables
        """
        self.story_board_id = story_board_id

    def run(self, share_data):
        try:
            #Check Essential Entity
            if (share_data.get_service_type() == "find_image") :
                share_data = self._call_service_provider(share_data)
                #initailize after service called
                share_data = self._initailize_story(share_data)
            elif (self._check_essential_entity(share_data.get_story_entity().keys(), share_data)) :
                share_data = self._call_service_provider(share_data)
                #initailize after service called
                #share_data = self._initailize_story(share_data)
            else :
                if (share_data.get_output_data() == ""):
                    share_data = share_data.set_output_data("자세히 말씀해 주세요")
                    share_data = self._initailize_story(share_data)
            return share_data
        except Exception as e:
            raise Exception(e)

    def _initailize_story(self, share_data):

        if(share_data != None) :
            share_data.set_story_id("")
            share_data.set_intent_id("")
            share_data.set_request_data("")
            share_data.initialize_story_entity()
        return share_data

    def _call_service_provider(self, share_data):
        share_data = ServiceProvider().run(share_data)
        return share_data

    def _check_essential_entity(self, entity_list, share_data):
        essential_entity = self._get_essential_entity()
        check_value = True
        for entity in essential_entity :
            #if(list(entity_list).count(entity) == 0) :
            if (entity in entity_list):
                pass
            else :
                share_data.set_output_data(entity + " 값을 입력해 주세요")
                check_value = False
                break

        return check_value

    def _get_essential_entity(self):
        essential_entity = []
        if(self.story_board_id == '2') :
            essential_entity = ["이름"]
        elif(self.story_board_id == '3') :
            essential_entity = ["업무"]
        elif(self.story_board_id == '4') :
            essential_entity = ["날짜", "이름"]

        return essential_entity

