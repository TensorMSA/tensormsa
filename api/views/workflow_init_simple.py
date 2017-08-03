import json
from rest_framework.response import Response
from rest_framework.views import APIView
from master.workflow.init.workflow_init_simple import WorkFlowSimpleManager
import coreapi
from master.network.nn_common_manager import NNCommonManager

class WorkFlowInitSimple(APIView) :
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
    def post(self, request, nnid, wfver):
        """
        - desc : insert data
        """
        try:
            return_data = WorkFlowSimpleManager().create_workflow(nnid, wfver, request.data['type'])
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def get(self, request, nnid, wfver, desc):
        """
        - desc : get data
        """
        try:
            return_data = NNCommonManager().get_nn_node_info(nnid, wfver, desc)
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def put(self, request, nnid, wfver):
        """
        - desc ; update data
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def delete(self, request, nnid, wfver):
        """
        - desc : delete  data
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))
