import json
from rest_framework.response import Response
from rest_framework.views import APIView
from cluster.generator.ner_augmentation import DataAugmentation

class AugNlpConf(APIView):
    """
    """
    def post(self, request, nnid, ver):
        """
        - desc : insert cnn configuration data
        """
        try:
            da = DataAugmentation(request.data)
            da.load_dict()
            da.convert_data()
            return Response(json.dumps("True"))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))