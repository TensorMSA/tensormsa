import json
from rest_framework.response import Response
from rest_framework.views import APIView
from master.network.nn_common_manager import NNCommonManager

class CommonNNInfoVersion(APIView):
    """
    """
    def post(self, request, nnid):
        """
        - desc : insert cnn configuration data
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
        - desc : get cnn configuration data
        """
        try:
            return_data = NNCommonManager().get_nn_wf_info(nnid)
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def put(self, request, nnid):
        """
        - desc ; update cnn configuration data
        """
        try:
            return_data = NNCommonManager().update_nn_wf_info(nnid, request.data)
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def delete(self, request, nnid):
        """
        - desc : delete cnn configuration data
        """
        try:

            return_data = NNCommonManager().delete_nn_wf_info(request.data)
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))
