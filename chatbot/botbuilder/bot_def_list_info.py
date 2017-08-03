from chatbot import serializers


class BotDefListInfo:

    def run_def_builder(self, data):
        """
        insert nn_info version data
        :param req:
        :return:
        """
        try:
            serializer_def = serializers.CB_DEF_LIST_INFO_Serializer(data=data)

            if serializer_def.is_valid():
                serializer_def.save()
            else:
                return serializer_def.is_valid(raise_exception=True)

            return data["cb_id"]

        except Exception as e:
            raise Exception(e)
