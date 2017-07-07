import json
from rest_framework.response import Response
from rest_framework.views import APIView
from chatbot.manager.service_manager import ServiceManager
from common.utils import *
import datetime

class ChatbotServiceManager(APIView):
    """
    """
    def post(self, request, cbid):

        try:
            #TODO: request prediction with files (swkim)
            #Get Cache
            result = ServiceManager(cbid).run_chatbot_with_file(request.FILES)
            return Response(json.dumps(result))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def put(self, request, cbid):

        try:
            self.init_time = datetime.datetime.now()
            print("Start:" + str((datetime.datetime.now() - self.init_time).total_seconds() * 1000))
            result = ServiceManager(cbid).run_chatbot(request.data)
            print("Done:" + str((datetime.datetime.now() - self.init_time).total_seconds() * 1000))
            return Response(json.loads(result))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))