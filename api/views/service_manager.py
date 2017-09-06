import json
from rest_framework.response import Response
from rest_framework.views import APIView
import coreapi

class ServiceManager(APIView):

    def post(self, request, nnid):
        """
        Set configurations for predict service
        ---
        # Class Name : ServiceManager

        # Description:
            Set configurations for predict service (not implemented yet)
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def get(self, request, nnid):
        """
        Set configurations for predict service
        ---
        # Class Name : ServiceManager

        # Description:
            Set configurations for predict service (not implemented yet)
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def put(self, request, nnid):
        """
        Set configurations for predict service
        ---
        # Class Name : ServiceManager

        # Description:
            Set configurations for predict service (not implemented yet)
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def delete(self, request, nnid):
        """
        Set configurations for predict service
        ---
        # Class Name : ServiceManager

        # Description:
            Set configurations for predict service (not implemented yet)
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))
