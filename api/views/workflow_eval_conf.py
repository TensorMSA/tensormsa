import json
from rest_framework.response import Response
from rest_framework.views import APIView
from master.workflow.evalconf.workflow_evalconf import WorkFlowEvalConfig
import coreapi

class WorkFlowEvalConf(APIView) :

    coreapi_fields = (
        coreapi.Field(
            name='type',
            required=True,
            type='string',
        ),
    )
    def post(self, request, nnid, ver):
        """
        This API is for set node parameters \n
        This node is for evaluation of train result \n
        You can choose 3 diffrent kind of test method (n fold, random, extra test set) \n
        ---
        # Class Name : WorkFlowEvalConf

        # Description:
            Set Test method and test data source
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def get(self, request, nnid):
        """
        This API is for set node parameters \n
        This node is for evaluation of train result \n
        You can choose 3 diffrent kind of test method (n fold, random, extra test set) \n
        ---
        # Class Name : WorkFlowEvalConf

        # Description:
            Get evaluation node configurations
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def put(self, request, nnid, ver, node):
        """
        This API is for set node parameters \n
        This node is for evaluation of train result \n
        You can choose 3 diffrent kind of test method (n fold, random, extra test set) \n
        ---
        # Class Name : WorkFlowEvalConf

        # Description:
            modify evaluation node configurations
        """
        try:
            config_data = request.data
            return_data = WorkFlowEvalConfig().set_view_obj(''.join([nnid, '_', ver, '_', node]),config_data)
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def delete(self, request, nnid):
        """
        This API is for set node parameters \n
        This node is for evaluation of train result \n
        You can choose 3 diffrent kind of test method (n fold, random, extra test set) \n
        ---
        # Class Name : WorkFlowEvalConf

        # Description:
            reset evaluation node configurations
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))
