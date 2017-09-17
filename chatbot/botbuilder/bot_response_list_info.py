from chatbot import serializers


class BotResponseListInfo:

    def run_response_builder(self, data):
        """
        insert nn_info version data
        :param req:
        :return:
        """
        try:
            serializer_response = serializers.CB_RESPONSE_LIST_INFO_Serializer(data=data)

            if serializer_response.is_valid():
                serializer_response.save()
            else:
                return serializer_response.is_valid(raise_exception=True)

            return data["story_id"]

        except Exception as e:
            raise Exception(e)
