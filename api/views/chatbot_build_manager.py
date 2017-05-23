import json
from rest_framework.response import Response
from rest_framework.views import APIView
from chatbot.manager.bot_builder import BotBuilder

class ChatbotBuildManager(APIView):
    """
    """
    def post(self, request):

        try:
            result = BotBuilder().run_builder(request.data)
            return Response(json.dumps(result))

        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def put(self, request):

        try:
            result = BotBuilder().run_chatbot(request.data)
            return Response(json.dumps(result))

        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))