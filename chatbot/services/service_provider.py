from chatbot.common.chat_share_data import ShareData
from cluster.service.service_predict_cnn import PredictNetCnn
from django.http.request import MultiValueDict
import base64

class ServiceProvider(ShareData):
    """
    class handle service models
    """
    def run(self, share_data):
        """
        run service based on decision
        :param share_data:
        :return:
        """
        return share_data

    def _external_service_call(self, share_data) :
        service_type = ShareData.get_service_type()

        if(service_type):

            return None
        elif(service_type):
            return None

        try:
            #TODO : api call to external rest service and return
            return None
        except Exception as e:
            raise Exception(e)

    def _internal_service_call(self, share_data) :
        # internal : IMAGE
        temp = {}


        request_type = ShareData.get_request_type()

        decode_text = base64.decodebytes(ShareData.get_input_data())
        temp['aaa'] = decode_text
        ml = MultiValueDict(temp)

        # CNN Prediction


        try:
            #TODO : internal service like image prediction using cnn
            if(request_type == "image"):
                PredictNetCnn.run(self,'0', '0',ml)
#            elif(ShareData.request_type == "voice"):
#                PredictNetCnn(share_data)
            return None
        except Exception as e:
            raise Exception(e)
