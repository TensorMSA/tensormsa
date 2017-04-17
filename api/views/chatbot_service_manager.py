import json
from rest_framework.response import Response
from rest_framework.views import APIView
from chatbot.manager.service_manager import ServiceManager

class ChatbotServiceManager(APIView):
    """
    """
    def post(self, request):

        try:
            #TODO: request prediction with files (swkim)
            #Get Cache
            result = ServiceManager().run_chatbot_with_file()
            return Response(json.dumps(result))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def put(self, request):

        try:
            #TODO:request prediction with text data (swkim)
            #Get Cache
            result = ServiceManager().run_chatbot()
            return Response(json.dumps(result))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def get(self, request):
        try:
            #TODO:local test (sskim)
            print("◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆ 1) 챗봇 서비스 시작")
            #Get Cache
            result = ServiceManager().run_console()
            return Response(json.dumps(result))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))