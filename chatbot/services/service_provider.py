from chatbot.common.chat_share_data import ShareData

class ServiceProvider(ShareData):
    """
    class handle service models
    """
    def run(self, share_data):
        """
        run service based on decision
        :param share_data:
        :return:
        """

        return share_data

    def _external_service_call(self, share_data) :

        try:
            #TODO : api call to external rest service and return
            return None
        except Exception as e:
            raise Exception(e)

    def _internal_service_call(self, share_data) :

        try:
            #TODO : internal service like image prediction using cnn
            return None
        except Exception as e:
            raise Exception(e)