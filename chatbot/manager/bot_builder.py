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
            serializer_story = serializers.CB_STORYBOARD_LIST_INFO_Serializer(data=data)
            serializer_entity = serializers.CB_ENTITY_LIST_INFO_Serializer(data=data)
            serializer_tagging = serializers.CB_TAGGING_INFO_Serializer(data=data)
            serializer_model = serializers.CB_MODEL_LIST_INFO_Serializer(data=data)

            if serializer_def.is_valid():
                serializer_def.save()
            else :
                return serializer_def.is_valid(raise_exception=True)

            if serializer_intent.is_valid():
                serializer_intent.save()
            else :
                return serializer_intent.is_valid(raise_exception=True)

            if serializer_story.is_valid():
                serializer_story.save()
            else :
                return serializer_story.is_valid(raise_exception=True)

            if serializer_entity.is_valid():
                serializer_entity.save()
            else :
                return serializer_def.is_valid(raise_exception=True)

            if serializer_tagging.is_valid():
                serializer_tagging.save()
            else :
                return serializer_tagging.is_valid(raise_exception=True)

            if serializer_model.is_valid():
                serializer_model.save()
            else :
                return serializer_model.is_valid(raise_exception=True)
            return data["cb_id"]

        except Exception as e:
            raise Exception(e)
