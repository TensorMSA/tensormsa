from chatbot.common.chat_share_data import ShareData

class EntityRecognizer(ShareData):

    def __init__(self, nn_id):
        """
        init global variables
        """
        self.nn_id = nn_id

    # TODO : call entity using by seq2seq (나는 식당에 간다 -> [나] [식당] )
    def parse(self, share_data):

        return share_data
