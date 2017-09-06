import json
from rest_framework.response import Response
from rest_framework.views import APIView
from master.workflow.init.workflow_init_simple import WorkFlowSimpleManager
import coreapi
from master.network.nn_common_manager import NNCommonManager

class WorkFlowInitSimple(APIView) :

    coreapi_fields = (
        coreapi.Field(
            name='type',
            required=True,
            type='string',
        ),
    )
    def post(self, request, nnid, wfver):
        """
        Simply initialize fixed graph flow which is preefined \n
        You can choose process with network id and data type \n
        There are several processes already designed \n
        ---
        # Class Name : WorkFlowInitSimple

        # Description:
            Set graph flow with given name and data type
        """
        try:
            return_data = WorkFlowSimpleManager().create_workflow(nnid, wfver, request.data['type'])
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def get(self, request, nnid, wfver, desc):
        """
        Simply initialize fixed graph flow which is preefined \n
        You can choose process with network id and data type \n
        There are several processes already designed \n
        ---
        # Class Name : WorkFlowInitSimple

        # Description:
            Get graph flow information with given network id
        """
        try:
            return_data = NNCommonManager().get_nn_node_info(nnid, wfver, desc)
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def delete(self, request, nnid, wfver):
        """
        Simply initialize fixed graph flow which is preefined \n
        You can choose process with network id and data type \n
        There are several processes already designed \n
        ---
        # Class Name : WorkFlowInitSimple

        # Description:
            Delete all graph flow and relate information
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))
