import json
from rest_framework.response import Response
from rest_framework.views import APIView
import coreapi

class WorkFlowDataReuse(APIView):

    coreapi_fields = (
        coreapi.Field(
            name='node_id',
            required=True,
            type='string',
        ),
    )
    def post(self, request, nnid):
        """
        This API is for set node parameters \n
        This node is for data extraction \n
        This node especially handles reuse type data \n
        You can set source server by set up parameters \n
        ---
        # Class Name : WorkFlowDataReuse

        # Description:
            Set params which data node to reuse
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def get(self, request, nnid):
        """
        This API is for set node parameters \n
        This node is for data extraction \n
        This node especially handles reuse type data \n
        You can set source server by set up parameters \n
        ---
        # Class Name : WorkFlowDataReuse

        # Description:
            You can see how the dataset looks like (use datamanager instead)
            this will show youj reused data node id only
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

