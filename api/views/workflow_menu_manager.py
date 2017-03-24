import json
from rest_framework.response import Response
from rest_framework.views import APIView
from master.workflow.common.workflow_state_menu import WorkFlowStateMenu


class WorkFlowMenuManager(APIView) :
    """

    """
    def post(self, request):
        """
        - desc : insert data
        """
        try:
            return_data = WorkFlowStateMenu().put_menu_info(request.data)
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def get(self, request):
        """
        - desc : get data
        """
        try:
            return_data = ""
            WorkFlowStateMenu().get_menu_info()
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def put(self, request):
        """
        - desc ; update data
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def delete(self, request):
        """
        - desc : delete  data
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))
