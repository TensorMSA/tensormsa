from chatbot.common.chat_share_data import ShareData
from chatbot.nlp.response_generator import ResponseGenerator
from cluster.service.service_predict_cnn import PredictNetCnn
from django.http.request import MultiValueDict
from django.core.files.uploadedfile import InMemoryUploadedFile
import base64, io

class ServiceProvider(ShareData):

    def __init__(self, service_story):
        self.service_story = service_story
    """
    class handle service models
    """
    def run(self, share_data):
        """
        run service based on decision
        :param share_data:
        :return:
        """
        print("■■■■■■■■■■ 서비스 호출 대상 판단 : " + share_data.get_story_id() )
        #Call Image Reconize
        if(share_data.get_service_type() == "find_image") :
            share_data = self._internal_service_call(share_data)
        #Exist Story Response
        elif(share_data.get_story_id() != '99') :
            share_data = ResponseGenerator().select_response(share_data)
        return share_data

    def _external_service_call(self, share_data) :
        try:
            service_type = ShareData.get_service_type()
            if(service_type):
                return share_data
            elif(service_type):
                return share_data
            #TODO : api call to external rest service and return
            return None
        except Exception as e:
            raise Exception(e)

    def _internal_service_call(self, share_data) :
        try:
            # internal : IMAGE
            print("■■■■■■■■■■ 이미지 분석 결과 분석 시작 ■■■■■■■■■■ ")

            temp = {}
            request_type = share_data.get_request_type()
            decode_text = base64.decodebytes(str.encode(share_data.get_request_data()))
            temp['test'] = [InMemoryUploadedFile(io.BytesIO(decode_text), None, 'test.jpg', 'image/jpeg', len(decode_text), None)]
            ml = MultiValueDict(temp)
            # fp = open("/hoya_src_root/nn00004/1/test1.jpg", 'wb')
            # fp.write(decode_text)
            # fp.close()
            # CNN Prediction
            if(request_type == "image"):
                return_val = PredictNetCnn().run('nn00004', None, ml )
                name_tag = {"KYJ" : "김영재", "KSW" : "김승우", "LTY" : "이태영", "LSH" : "이상현", "PJH" : "백지현", "KSS" : "김수상", "PSC" : "박성찬"}
                print("■■■■■■■■■■ 이미지 분석 결과 분석 결과 : " + return_val['test.jpg']['key'][0])
                share_data.set_output_data(name_tag[return_val['test.jpg']['key'][0]] + "인거 같은데 맞나요?")
            else :
                share_data.set_output_data("이미지 분석 결과가 없습니다")

            return share_data
        except Exception as e:
            raise Exception(e)
