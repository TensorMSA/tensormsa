import json
from rest_framework.response import Response
from rest_framework.views import APIView
import coreapi

class WorkFlowInitCustom(APIView) :

    def post(self, request, nnid):
        """
        [Still on development]
        This will allow you to design your own graph path
        ---
        # Class Name : WorkFlowInitCustom

        # Description:
            still on development
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def get(self, request, nnid):
        """
        [Still on development]
        This will allow you to design your own graph path
        ---
        # Class Name : WorkFlowInitCustom

        # Description:
            still on development
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def put(self, request, nnid):
        """
        [Still on development]
        This will allow you to design your own graph path
        ---
        # Class Name : WorkFlowInitCustom

        # Description:
            still on development
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def delete(self, request, nnid):
        """
        [Still on development]
        This will allow you to design your own graph path
        ---
        # Class Name : WorkFlowInitCustom

        # Description:
            still on development
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))
