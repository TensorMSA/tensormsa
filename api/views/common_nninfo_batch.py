from rest_framework.views import APIView
from master.network.nn_common_manager import NNCommonManager
from rest_framework.response import Response
import json
import coreapi

class CommonNNInfoBatch(APIView):
    """
    
    """
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
    def get(self, request, nnid, ver):
        """
        Your docs
        ---
        # Class Name (must be separated by `---`)

        # Description:
            - name: name
              description: Foobar long description goes here
        """
        try:
            return_data = NNCommonManager().get_nn_batch_info(nnid, ver)
            conv = []
            for row in return_data:
                row['fields']['nn_batch_ver_id'] = row['pk']
                conv.append(row['fields'])
            return Response(json.dumps(conv))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))