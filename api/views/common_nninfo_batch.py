from rest_framework.views import APIView
from master.network.nn_common_manager import NNCommonManager
from rest_framework.response import Response
import json

class CommonNNInfoBatch(APIView):
    def get(self, request, nnid, ver):
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