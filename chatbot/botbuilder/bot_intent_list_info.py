from chatbot import serializers


class BotIntentListInfo:

    def run_intent_builder(self, data):
        """
        insert nn_info version data
        :param req:
        :return:
        """
        try:
            serializer_intent = serializers.CB_INTENT_LIST_INFO_Serializer(data=data)

            if serializer_intent.is_valid():
                serializer_intent.save()
            else:
                return serializer_intent.is_valid(raise_exception=True)

            return data["cb_id"]

        except Exception as e:
            raise Exception(e)
