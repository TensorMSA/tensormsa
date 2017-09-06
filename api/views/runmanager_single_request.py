import json
from rest_framework.response import Response
from rest_framework.views import APIView
from cluster.service.service_single_task import WorkFlowSingleTask
from cluster.service.service_single_task import single_run
from common.utils import *
import traceback
import coreapi

class RunManagerSingleRequest(APIView):
    # TODO:add document sample for swagger (need to update)
    coreapi_fields = (
        coreapi.Field(
            name='flag',
            required=True,
            type='string',
        ),
    )

    def post(self, request, nnid, ver, node):
        """
        We can execute single node with this api
        you must specify nnid, ver and node name for that purpose
        ---
        # Class Name : RunManagerSingleRequest

        # Description:
            request single node to be executed
        """
        try:
            #result = single_run.delay(nnid, ver, node)
            result = single_run(nnid, ver, node)
            return Response(json.dumps(result))
        except Exception as e:
            traceback.print_exc()
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def get(self, request, nnid, ver, node):
        """
        We can execute single node with this api
        you must specify nnid, ver and node name for that purpose
        ---
        # Class Name : RunManagerSingleRequest

        # Description:
            get status of single node (run, wait, done.. etc)
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def put(self, request, nnid, ver, node):
        """
        We can execute single node with this api
        you must specify nnid, ver and node name for that purpose
        ---
        # Class Name : RunManagerSingleRequest

        # Description:
            edit status of single node
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))
