import json
from rest_framework.response import Response
from rest_framework.views import APIView
from chatbot.manager.bot_builder import BotBuilder
import coreapi

class ChatbotBuildManager(APIView):
    """
    """
    # TODO:add document sample for swagger (need to update)
    coreapi_fields = (
        coreapi.Field(
            name='parm1',
            required=True,
            schema=coreapi.Field(name='parm3',
                                 required=True,
                                 description='haha',
                                 type=str)
        ),
        coreapi.Field(
            name='parm2',
            required=True,
            type='string',
        ),
    )
    def post(self, request,type):
        """
        ChatBot Build API
        ---
        # Class Name : ChatbotBuildManager

        # Description:
            Build chatbot process include create chatbotId, StoryBoard, NeuralNet IDS (used on chatbot process)
            This is a necessary step to use chatbot, you have to define all parms for chatbot before use it
        """
        try:
            result = BotBuilder().run_builder(request.data,type=type)
            return Response(json.dumps(result))

        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def put(self, request):
        """
        Your docs
        ---
        # Class Name (must be separated by `---`)

        # Description:
            - name: name
              description: Foobar long description goes here
        """
        try:
            result = BotBuilder().run_chatbot(request.data)
            return Response(json.dumps(result))

        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))