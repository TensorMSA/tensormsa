import json
from rest_framework.response import Response
from rest_framework.views import APIView
from master.workflow.netconf.workflow_netconf_cnn import WorkFlowNetConfCNN

class WorkFlowNetConfCnn(APIView) :
    """

    """
    def post(self, request, nodeid):
        """
        - desc : insert data
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def get(self, request, nodeid):
        """
        - desc : get data
        """
        try:
            input_data = json.loads(str(request.body, 'utf-8'))
            return_data = WorkFlowNetConfCNN().get_view_obj(nodeid)
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def put(self, request, nodeid):
        """
        - desc ; update data
        """
        try:
            input_data = json.loads(str(request.body, 'utf-8'))
            return_data = WorkFlowNetConfCNN().set_view_obj(input_data)
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def delete(self, request, nodeid):
        """
        - desc : delete  data
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))
