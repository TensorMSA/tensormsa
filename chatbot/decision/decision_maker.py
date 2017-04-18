from chatbot.common.chat_share_data import ShareData
from chatbot.story.story_board_manager import StoryBoardManager

class DecisionMaker(ShareData):
    """
    (1) check intend is clear , if not return intend select list
    (2) check intend service type (story board, ontology and etc)
    """
    def run(self, share_data):
        """

        :param share_data:
        :return:
        """
        try :
            self.__dict__ = share_data.__dict__
            #Story Exist
            if (self.story_board_id != "") :
                StoryBoardManager(share_data.get_story_id()).run(share_data)
            #First Story
            else :
                share_data = self._get_story_board(share_data)

            return share_data
        except Exception as e:
            raise Exception(e)

    def _get_story_board(self, share_data) :
        try :
            # TODO : Intent and Story ID is in DB
            if(self.intent_id == "1") :
                share_data.set_story_id("1")
                StoryBoardManager(share_data.get_story_id()).run(share_data)
                share_data.set_service_type("find_info")
            elif(self.intent_id == "3") :
                share_data.set_story_id("3")
                StoryBoardManager(share_data.get_story_id()).run(share_data)
                share_data.set_service_type("find_leader")
            elif(self.intent_id == "4") :
                share_data.set_story_id("4")
                StoryBoardManager(share_data.get_story_id()).run(share_data)
                share_data.set_service_type("find_image")
            else :
                share_data.set_output_data("무슨 말씀인지 잘 모르겠어요")
            return share_data
        except Exception as e:
            raise Exception(e)