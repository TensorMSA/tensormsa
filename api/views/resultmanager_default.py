import json
from rest_framework.response import Response
from rest_framework.views import APIView
from master.result.result_manager_default import ResultManagerDefault as result_man
import coreapi

class ResultManagerDefault(APIView):

    def get(self, request, nnid, ver):
        """
        Trained model test result
        ---
        # Class Name : ResultManagerDefault

        # Description:
            train result management (accuracy, loss, test result and etc)
        """
        try:
            return_data = result_man.get_view_obj(self,nnid,ver)
            convert_data = return_data[0].get('fields').get('result_info')
            return Response(json.dumps(convert_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))
