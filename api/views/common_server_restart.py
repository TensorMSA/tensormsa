from django.core.serializers.json import json
from rest_framework.response import Response
from rest_framework.views import APIView
import os, signal, coreapi

class CommonServerRestart(APIView):
    """
    
    """
    #TODO:add document sample for swagger (need to update)
    coreapi_fields = (
        coreapi.Field(
            name='parm1',
            required=True,
            schema=str,
        ),
        coreapi.Field(
            name='parm2',
            required=True,
            schema=str,
        ),
    )
    def post(self, request):
        """
        Your docs
        ---
        # Class Name (must be separated by `---`)

        # Description:
            - name: name
              description: Foobar long description goes here
        """
        try:
            os.kill(os.getppid(), signal.SIGHUP)
            return_data = {"status": "200", "result": "restart uwsgi"}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))
