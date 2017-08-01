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
            name='parm1',
            required=True,
            schema=str,
        ),
        coreapi.Field(
            name='parm2',
            required=True,
            schema=str,
        ),
    )

    def post(self, request, nnid, ver, node):
        """
        - desc : insert data
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
        - desc : get data
        """
        try:
            logging.info("RunManager get...........................")
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
