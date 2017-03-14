import json
from rest_framework.response import Response
from rest_framework.views import APIView
from master.workflow.dataconf.workflow_dataconf_frame import WorkflowDataConfFrame as data_conf_frm

class WorkFlowDataConfFrame(APIView):
    """
    """

    #url(r'^api/v1/type/wf/state/dataconf/detail/frame/nnid/(?P<nnid>.*)/ver/(?P<ver>.*)/node/(?P<node>.*)/',
    def post(self, request, nnid, ver, node):
        """
        - desc : insert cnn configuration data
          completed
        """
        try:
            input_data = json.loads(str(request.body, 'utf-8'))

            return_data = data_conf_frm().put_step_source( nnid, ver, node, input_data )


            return Response(json.dumps(input_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def get(self, request, nnid, ver, node):
        """
        - desc : get cnn configuration data
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def put(self, request, nnid, ver, node):
        """
        - desc ; update cnn configuration data
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def delete(self, request, nnid, ver, node):
        """
        - desc : delete cnn configuration data
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))
