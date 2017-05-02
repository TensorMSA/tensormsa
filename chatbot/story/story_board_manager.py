from chatbot.common.chat_share_data import ShareData
from chatbot.services.service_provider import ServiceProvider
from chatbot.common.chat_knowledge_data_dict import ChatKnowledgeDataDict

class StoryBoardManager(ShareData):
    """

    """

    def __init__(self, cb_id,  story_board_id):
        """
        init global variables
        """
        self.story_board_id = story_board_id
        self.essential_entity = ChatKnowledgeDataDict(cb_id).get_essential_entity(self.story_board_id)

    def run(self, share_data):
        try:
            if (share_data.get_service_type() == "find_image") :
                share_data = self._call_service_provider(share_data)
                #initailize after service called
                #share_data.initailize_story()
            #Check Essential Entity
            elif (self._check_essential_entity(share_data.get_story_entity().keys(), share_data)) :
                share_data = self._call_service_provider(share_data)
            elif (self.story_board_id  == "99"):
                return share_data
            else :
                if (share_data.get_output_data() == ""):
                    share_data = share_data.set_output_data("자세히 말씀해 주세요")
                    share_data._initailize_story()
            return share_data
        except Exception as e:
            raise Exception(e)

    def _call_service_provider(self, share_data):
        share_data = ServiceProvider().run(share_data)
        return share_data

    def _check_essential_entity(self, entity_list, share_data):
        check_value = True
        for entity in self.essential_entity :
            #if(list(entity_list).count(entity) == 0) :
            if (entity in entity_list):
                pass
            else :
                share_data.set_output_data(entity + " 값을 입력해 주세요")
                check_value = False
                break

        return check_value
