import json
from rest_framework.response import Response
from rest_framework.views import APIView
import coreapi

class RunManagerWorkFlow(APIView):

    def post(self, request, nnid):
        """
        CRUD of workflow information
        ---
        # Class Name : RunManagerWorkFlow

        # Description:
            CRUD of workflow information (not implemented yet)
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def get(self, request, nnid):
        """
        CRUD of workflow information
        ---
        # Class Name : RunManagerWorkFlow

        # Description:
            CRUD of workflow information (not implemented yet)
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def put(self, request, nnid):
        """
        CRUD of workflow information
        ---
        # Class Name : RunManagerWorkFlow

        # Description:
            CRUD of workflow information (not implemented yet)
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def delete(self, request, nnid):
        """
        CRUD of workflow information
        ---
        # Class Name : RunManagerWorkFlow

        # Description:
            CRUD of workflow information (not implemented yet)
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))
