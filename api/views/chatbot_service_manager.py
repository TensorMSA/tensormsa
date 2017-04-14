import json
from rest_framework.response import Response
from rest_framework.views import APIView
from chatbot.manager.service_manager import ServiceManager

class ChatbotServiceManager(APIView):
    """
    """
    def post(self, request):

        try:
            print("◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆ 1) 챗봇 서비스 시작")
            #Get Cache
            result = ServiceManager().run_chatbot()
            return Response(json.dumps(result))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))