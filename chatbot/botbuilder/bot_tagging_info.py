from chatbot import serializers


class BotTaggingInfo:

    def run_tagging_builder(self, data):
        """
        insert nn_info version data
        :param req:
        :return:
        """
        try:
            serializer = serializers.CB_TAGGING_INFO_Serializer(data=data)

            if serializer.is_valid():
                serializer.save()
            else:
                return serializer.is_valid(raise_exception=True)

            return data["cb_id"]

        except Exception as e:
            raise Exception(e)
