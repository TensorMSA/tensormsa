import json
from rest_framework.response import Response
from rest_framework.views import APIView
from master.workflow.dataconf.workflow_dataconf_frame import WorkflowDataConfFrame as data_conf_frm
import coreapi

class WorkFlowDataConfFrame(APIView):
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

    #url(r'^api/v1/type/wf/state/dataconf/detail/frame/nnid/(?P<nnid>.*)/ver/(?P<ver>.*)/node/(?P<node>.*)/',
    def post(self, request, nnid, ver, node):
        """
        - desc : insert cnn configuration data
          completed
        """
        try:
            data_conf_frm().put_step_source( nnid, ver, node, request.data )
            return Response(json.dumps(request.data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def get(self, request, nnid, ver, node):
        """
        - desc : get cnn configuration data
        """
        try:
            return_data = data_conf_frm().get_data_conf( nnid, ver, node)
            #data_conf_frm().get_data_conf(nnid, ver, node, request.data)
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def put(self, request, nnid, ver, node):
        """
        - desc ; update cnn configuration data
        """
        try:
            #put_step_source(self, nnid, ver, node, input_data):
            data_conf_frm().put_step_source(nnid, ver, node, request.data)
            return Response(json.dumps(request.data))
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
