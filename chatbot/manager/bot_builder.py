from chatbot import serializers
from rest_framework.views import APIView

class BotBuilder(APIView):

    def run_builder(self, data):
        """
        insert nn_info version data
        :param req:
        :return:
        """
        try:
            serializer = serializers.CB_DEF_LIST_INFO_Serializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return data["cb_id"]
            else :
                return serializer.is_valid(raise_exception=True)
        except Exception as e:
            raise Exception(e)
