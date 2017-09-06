import json
from rest_framework.response import Response
from rest_framework.views import APIView
import coreapi

class ConfServerData(APIView):
    """
    """
    def post(self, request, nnid):
        """
        Manage Server info (master, slave, service and data servers)
        ---
        # Class Name : ConfServerData

        # Description:
            create, remove, update, delete server info via rest api
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def get(self, request, nnid):
        """
        Manage Server info (master, slave, service and data servers)
        ---
        # Class Name : ConfServerData

        # Description:
            create, remove, update, delete server info via rest api
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def put(self, request, nnid):
        """
        Manage Server info (master, slave, service and data servers)
        ---
        # Class Name : ConfServerData

        # Description:
            create, remove, update, delete server info via rest api
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def delete(self, request, nnid):
        """
        Manage Server info (master, slave, service and data servers)
        ---
        # Class Name : ConfServerData

        # Description:
            create, remove, update, delete server info via rest api
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))
