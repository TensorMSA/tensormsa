import json
from rest_framework.response import Response
from rest_framework.views import APIView
from cluster.service.service_predict_w2v import PredictNetW2V


class ServiceManagerPredict(APIView):
    """
    """
    def post(self, request, type, nnid):
        """
        - desc : insert cnn configuration data
        """
        try:
            input_data = json.loads(str(request.body, 'utf-8'))
            if(type == 'w2v') :
                return_data = PredictNetW2V().run(nnid, input_data)
            else :
                raise Exception ("Not defined type error")

            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def get(self, request, type, nnid):
        """
        - desc : get cnn configuration data
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def put(self, request, type, nnid):
        """
        - desc ; update cnn configuration data
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def delete(self, request, type, nnid):
        """
        - desc : delete cnn configuration data
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))
