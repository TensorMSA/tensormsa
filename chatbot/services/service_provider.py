from chatbot.common.chat_share_data import ShareData
from cluster.service.service_predict_cnn import PredictNetCnn
from django.http.request import MultiValueDict
from django.core.files.uploadedfile import InMemoryUploadedFile
import base64, io

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
        if(share_data.get_service_type() =='find_image') :
            self._internal_service_call(share_data)
            return share_data

    def _external_service_call(self, share_data) :
        service_type = ShareData.get_service_type()

        if(service_type):

            return None
        elif(service_type):
            return None

        # service_type
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
        try:
            # internal : IMAGE
            temp = {}
            request_type = share_data.get_request_type()
            decode_text = base64.decodebytes(str.encode(share_data.get_request_data()))
            temp['test'] = [InMemoryUploadedFile(io.BytesIO(decode_text), None, 'test.jpg', 'image/jpeg', len(decode_text), None)]
            ml = MultiValueDict(temp)

            # CNN Prediction
            if(request_type == "image"):
                return_val = PredictNetCnn().run('nn00004', '0',ml)
                share_data.set_output_data(return_val['test.jpg']['key'][0])
            return share_data
        except Exception as e:
            raise Exception(e)
