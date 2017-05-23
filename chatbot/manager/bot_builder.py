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
            serializer_def = serializers.CB_DEF_LIST_INFO_Serializer(data=data)
            serializer_intent = serializers.CB_INTENT_LIST_INFO_Serializer(data=data)


            if serializer_def.is_valid():
                serializer_def.save()
            else :
                return serializer_def.is_valid(raise_exception=True)

            if serializer_intent.is_valid():
                serializer_intent.save()
            else :
                return serializer_intent.is_valid(raise_exception=True)
            return data["cb_id"]
        except Exception as e:
            raise Exception(e)
