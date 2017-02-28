import json
from rest_framework.response import Response
from rest_framework.views import APIView
from master.workflow.data.workflow_data_image import WorkFlowDataImage


class WorkFlowDataImgSourceLocal(APIView):
    """
    """
    def post(self, request, nnid, ver):
        """
        - desc : insert cnn configuration data
        """
        try:
            input_data = json.loads(str(request.body, 'utf-8'))
            return_data = WorkFlowDataImage().put_step_source(nnid, ver,input_data)
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def get(self, request, nnid, ver):
        """
        - desc : get cnn configuration data
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def put(self, request, nnid, ver):
        """
        - desc ; update cnn configuration data
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def delete(self, request, nnid, ver):
        """
        - desc : delete cnn configuration data
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))
