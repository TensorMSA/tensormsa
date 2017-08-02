import json
from rest_framework.response import Response
from rest_framework.views import APIView
from master.workflow.common.workflow_state_menu import WorkFlowStateMenu
import coreapi

class WorkFlowSubMenuManager(APIView) :
    # TODO:add document sample for swagger (need to update)
    coreapi_fields = (
        coreapi.Field(
            name='parm1',
            required=True,
            type='string',
        ),
        coreapi.Field(
            name='parm2',
            required=True,
            type='string',
        ),
    )
    def post(self, request, menu):
        """
        - desc : insert data
        """
        try:
            input_data = request.data
            input_data['wf_task_menu_id'] = menu
            return_data = WorkFlowStateMenu().put_submenu_info(input_data)
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def get(self, request, menu):
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

    def put(self, request, menu):
        """
        - desc ; update data
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def delete(self, request, menu):
        """
        - desc : delete  data
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))
