from chatbot import serializers


class BotEntityListInfo:

    def run_entity_builder(self, data):
        """
        insert nn_info version data
        :param req:
        :return:
        """
        try:
            serializer = serializers.CB_ENTITY_LIST_INFO_Serializer(data=data)

            if serializer.is_valid():
                serializer.save()
            else:
                return serializer.is_valid(raise_exception=True)

            return data["cb_id"]

        except Exception as e:
            raise Exception(e)
