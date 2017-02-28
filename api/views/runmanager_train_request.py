import json
from rest_framework.response import Response
from rest_framework.views import APIView
from cluster.service.workflow_train_task import WorkFlowTrainTask
from cluster.service.workflow_train_task import train
from common.utils import *

class RunManagerTrainRequest(APIView):
    """
    """
    def post(self, request, nnid, ver, node):
        """
        - desc : insert data
        """
        try:
            # result = train.delay(nnid, ver)
            input_data = json.loads(str(request.body, 'utf-8'))
            result = train(input_data)
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

    def put(self, request, nnid, ver):
        """
        - desc ; update data
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def delete(self, request, nnid, ver):
        """
        - desc : delete data
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))
