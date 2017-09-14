import json
from rest_framework.response import Response
from rest_framework.views import APIView
from cluster.automl.automl_runmanager import AutoMlRunManager, automl_run
import coreapi
import threading

class RunManagerAutoTrain(APIView):

    coreapi_fields = (
        coreapi.Field(
            name='flag',
            required=True,
            type='string',
        ),
    )

    def post(self, request, nnid):
        """
        Bellow is the process of running automl on our framework
        (1) Define AutoML Graph definition \n
        (2) Select Type of Data \n
        (3) Select Type of Anal algorithm \n
        (4) Select range of hyper parameters \n
        (5) Run - AutoML (<- for this step) \n
        (6) Check result of each generation with UI/UX  \n
        (7) Select Best model you want use and activate it \n
        ---
        # Class Name : RunManagerAutoTrain

        # Description:
            request train on selected automl id
        """
        try:
            automl_run(nnid)
            return Response(json.dumps([True]))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def get(self, request, nnid):
        """
        Bellow is the process of running automl on our framework
        (1) Define AutoML Graph definition \n
        (2) Select Type of Data \n
        (3) Select Type of Anal algorithm \n
        (4) Select range of hyper parameters \n
        (5) Run - AutoML (<- for this step) \n
        (6) Check result of each generation with UI/UX  \n
        (7) Select Best model you want use and activate it \n
        ---
        # Class Name : RunManagerAutoTrain

        # Description:
            get status of selected autol ml id
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def put(self, request, nnid):
        """
        Bellow is the process of running automl on our framework
        (1) Define AutoML Graph definition \n
        (2) Select Type of Data \n
        (3) Select Type of Anal algorithm \n
        (4) Select range of hyper parameters \n
        (5) Run - AutoML (<- for this step) \n
        (6) Check result of each generation with UI/UX  \n
        (7) Select Best model you want use and activate it \n
        ---
        # Class Name : RunManagerAutoTrain

        # Description:
            change status of automl id (like.. stop process while working..)
        """
        try:
            return_data = ""
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
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))
