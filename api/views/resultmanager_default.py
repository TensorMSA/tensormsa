import json
from rest_framework.response import Response
from rest_framework.views import APIView
from master.result.result_manager_default import ResultManagerDefault as result_man


class ResultManagerDefault(APIView):
    """
    """
    def post(self, request, nnid, ver):
        """
        - desc : insert cnn configuration data
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def get(self, request, nnid, ver):
        """
        - desc : get cnn configuration data  {nnid}/ver/{ver}/
        """
        try:
            return_data = result_man.get_view_obj(self,nnid,ver)
            #result_man
            #return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def put(self, request, nnid, ver):
        """
        - desc ; update cnn configuration data
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def delete(self, request, nnid, ver):
        """
        - desc : delete cnn configuration data
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))
