import json
from rest_framework.response import Response
from rest_framework.views import APIView
from cluster.service.service_single_task import WorkFlowSingleTask
from cluster.service.service_single_task import single_run
from common.utils import *

class RunManagerSingleRequest(APIView):
    """
    """

    def post(self, request, nnid, ver, node):
        """
        - desc : insert data
        """
        try:
            result = single_run.delay(nnid, ver, node)
            return Response(json.dumps(result.get()))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def get(self, request, nnid, ver, node):
        """
        - desc : get data
        """
        try:
            println("RunManager get...........................")
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def put(self, request, nnid, ver, node):
        """
        - desc ; update data
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def delete(self, request, nnid, ver, node):
        """
        - desc : delete data
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))
