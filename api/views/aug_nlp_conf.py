import json
from rest_framework.response import Response
from rest_framework.views import APIView
from cluster.generator.ner_augmentation import DataAugmentation
import coreapi

class AugNlpConf(APIView):

    def post(self, request, nnid, ver):
        """
        Augment text data with pattern and dict
        ---
        # Class Name : AugNlpConf

        # Description:
            This Rest API support to augment train data with pattern and dict, this will generate
            real type of data for sequence labeling, wordembedding and supervised learning
        """
        try:
            da = DataAugmentation(request.data)
            da.run()
            return Response(json.dumps("True"))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))