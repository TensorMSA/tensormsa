from django.core.serializers.json import json
from rest_framework.response import Response
from rest_framework.views import APIView
import os, signal, coreapi

class CommonServerRestart(APIView):
    """
    
    """
    def post(self, request):
        """
        Request to restart all nginx threads
        ---
        # Class Name : CommonServerRestart

        # Description:
            restart nginx threads via rest api
        """
        try:
            os.kill(os.getppid(), signal.SIGHUP)
            return_data = {"status": "200", "result": "restart uwsgi"}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))
