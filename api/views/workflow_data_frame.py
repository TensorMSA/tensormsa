import json
from rest_framework.response import Response
from rest_framework.views import APIView
from master.workflow.data.workflow_data_frame import WorkFlowDataFrame as data_frm


class WorkFlowDataFrame(APIView):
    """
    """
    def post(self, request, src, form, prg, nnid, ver, node):
        """
        - desc : insert cnn configuration data
        """
        try:
            input_data = json.loads(str(request.body, 'utf-8'))
            if (src == 'local' and prg == 'source'):
                #print("1")#nnid, wfver, config_data
                return_data = data_frm().put_step_source(nnid, ver, input_data)
            else :
                return_data = {'result' : 'no type'}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def get(self, request, src, form, prg, nnid, ver, node):
        """
        - desc : get cnn configuration data
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def put(self, request, src, form, prg, nnid, ver, node):
        """
        - desc ; update cnn configuration data
        """
        try:
            input_data = json.loads(str(request.body, 'utf-8'))
            if(src == 'local' and prg == 'source') :
                return_data = data_frm().put_step_source(nnid, ver, input_data)
            else :
                return_data = {'result' : 'no type'}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def delete(self, request, src, form, prg, nnid, ver, node):
        """
        - desc : delete cnn configuration data
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))
