from chatbot import serializers
from chatbot import models

class BotModelListInfo:

    def run_model_builder(self, data):
        """
        insert nn_info version data
        :param req:
        :return:
        """
        try:
            serializer = serializers.CB_MODEL_LIST_INFO_Serializer(data=data)

            if serializer.is_valid():
                serializer.save()
            else:
                #딥러닝 테스트를 위해 모델ID만 업데이트로 진행
                def_list = models.CB_MODEL_LIST_INFO.objects.get(cb_id=data["cb_id"], nn_purpose=data["nn_purpose"])
                def_list.nn_id = data["nn_id"]
                def_list.save()
                return serializer.is_valid(raise_exception=True)

            return data["cb_id"]

        except Exception as e:
            raise Exception(e)
