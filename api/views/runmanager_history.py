import json
from rest_framework.response import Response
from rest_framework.views import APIView
import coreapi

class RunManagerHistory(APIView):

    def post(self, request, nnid):
        """
        Check History of models
        ---
        # Class Name : RunManagerHistory

        # Description:
            manage history of training results
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def get(self, request, nnid):
        """
        Check History of models
        ---
        # Class Name : RunManagerHistory

        # Description:
            manage history of training results
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def put(self, request, nnid):
        """
        Check History of models
        ---
        # Class Name : RunManagerHistory

        # Description:
            manage history of training results
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def delete(self, request, nnid):
        """
        Check History of models
        ---
        # Class Name : RunManagerHistory

        # Description:
            manage history of training results
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))
