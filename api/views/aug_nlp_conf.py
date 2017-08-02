import json
from rest_framework.response import Response
from rest_framework.views import APIView
from cluster.generator.ner_augmentation import DataAugmentation
import coreapi

class AugNlpConf(APIView):
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
    def post(self, request, nnid, ver):
        """
        Your docs
        ---
        # Class Name (must be separated by `---`)

        # Description:
            - name: name
              description: Foobar long description goes here
        """
        try:
            da = DataAugmentation(request.data)
            da.run()
            return Response(json.dumps("True"))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))