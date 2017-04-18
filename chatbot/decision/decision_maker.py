from chatbot.common.chat_share_data import ShareData

class DecisionMaker(ShareData):
    """
    (1) check intend is clear , if not return intend select list
    (2) check intend service type (story board, ontology and etc)
    """
    def run(self, share_data, story_board, service_provider):
        """

        :param share_data:
        :return:
        """
        self.__dict__ = share_data.__dict__
        return share_data

    def _get_story_board(self, intend, entity, service_param):
        """

        :param intend:
        :param entity:
        :param service_param:
        :return:
        """
        pass