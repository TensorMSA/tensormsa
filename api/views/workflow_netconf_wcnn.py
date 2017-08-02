import json
from rest_framework.response import Response
from rest_framework.views import APIView
from master.workflow.netconf.workflow_netconf_wcnn import WorkFlowNetConfWideCnn as WcnnConf
from common.utils import *
import coreapi

class WorkFlowNetConfWcnn(APIView) :
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
    def post(self, request, nnid, ver, node):
        """
        - desc : insert data
        """
        try:
            input_data = request.data
            input_data['model_path'] = get_model_path(nnid, ver, node)
            return_data = WcnnConf(nnid+"_"+ver+"_"+node).set_view_obj( nnid, ver, node, input_data)
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def get(self, request, nnid, ver, node):
        """
        - desc : get data
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def put(self, request, nnid, ver, node):
        """
        - desc ; update data
        """
        try:
            input_data = request.data
            input_data['model_path'] = get_model_path(nnid, ver, node)
            nodeid = ''.join([nnid, '_', ver, '_', node])
            return_data = WcnnConf().set_view_obj(nodeid, input_data)
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def delete(self, request, nnid, ver, node):
        """
        - desc : delete  data
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))
