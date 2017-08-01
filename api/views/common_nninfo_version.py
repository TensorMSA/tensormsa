import json
from rest_framework.response import Response
from rest_framework.views import APIView
from master.network.nn_common_manager import NNCommonManager
import coreapi

class CommonNNInfoVersion(APIView):
    """
    """
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
    def post(self, request, nnid):
        """
        Your docs
        ---
        # Class Name (must be separated by `---`)

        # Description:
            - name: name
              description: Foobar long description goes here
        """
        try:
            input_data = request.data
            input_data['nn_id'] = nnid
            nnManager = NNCommonManager()
            nn_wf_ver_id = nnManager.get_nn_max_ver(nnid) + 1
            input_data['nn_wf_ver_id'] = nn_wf_ver_id
            return_data = nnManager.insert_nn_wf_info(input_data)
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def get(self, request, nnid):
        """
        Your docs
        ---
        # Class Name (must be separated by `---`)

        # Description:
            - name: name
              description: Foobar long description goes here
        """
        try:
            return_data = NNCommonManager().get_nn_wf_info(nnid)
            conv = []
            for row in return_data:
                conv.append(row['fields'])
            return Response(json.dumps(conv))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def put(self, request, nnid):
        """
        Your docs
        ---
        # Class Name (must be separated by `---`)

        # Description:
            - name: name
              description: Foobar long description goes here
        """
        try:
            return_data = NNCommonManager().update_nn_wf_info(nnid, request.data)
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def delete(self, request, nnid):
        """
        Your docs
        ---
        # Class Name (must be separated by `---`)

        # Description:
            - name: name
              description: Foobar long description goes here
        """
        try:

            return_data = NNCommonManager().delete_nn_wf_info(request.data)
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))
