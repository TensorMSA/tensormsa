import json
from rest_framework.response import Response
from rest_framework.views import APIView
from master.workflow.netconf.workflow_netconf_w2v import WorkFlowNetConfW2V as Word2Vec
from common.utils import *
import coreapi

class WorkFlowNetConfW2V(APIView) :
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
            nodeid = ''.join([nnid, '_', ver, '_', node])
            return_data = Word2Vec().set_view_obj(nodeid, input_data)
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def get(self, request, nnid, ver, node):
        """
        - desc : get data
        """
        try:
            nodeid = ''.join([nnid, '_', ver , '_', node])
            return_data = Word2Vec().get_view_obj(nodeid)
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def put(self, request, nnid, ver, node):
        """
        - desc ; update data
        """
        try:
            input_data = json.loads(str(request.body, 'utf-8'))
            input_data['model_path'] = get_model_path(nnid, ver, node)
            nodeid = ''.join([nnid, '_', ver, '_', node])
            return_data = Word2Vec().set_view_obj(nodeid, input_data)
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
