import json
from rest_framework.response import Response
from rest_framework.views import APIView
from master.workflow.data.workflow_data_text import WorkFlowDataText as WfDataText
from common.utils import *
import coreapi

class WorkFlowDataText(APIView):
    # TODO:add document sample for swagger (need to update)
    coreapi_fields = (
        coreapi.Field(
            name='parm1',
            required=True,
            schema=str,
        ),
        coreapi.Field(
            name='parm2',
            required=True,
            schema=str,
        ),
    )
    def post(self, request, src, form, prg, nnid, ver, node):
        """
        - desc : insert cnn configuration data
        """
        try:
            # save uploaded file on source folder
            file_cnt = save_upload_file(request, nnid, ver, node)
            return Response(json.dumps(["{0} file upload success".format(file_cnt)]))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def get(self, request, src, form, prg, nnid, ver, node):
        """
        - desc : get cnn configuration data
        """
        try:
            if(prg == 'source') :
                return_data = WfDataText(nnid+"_"+ver+"_"+node).get_step_source()
            elif(prg == 'pre') :
                return_data = WfDataText(nnid+"_"+ver+"_"+node).get_step_preprocess()
            elif(prg == 'store') :
                return_data = WfDataText(nnid+"_"+ver+"_"+node).get_step_store()
            else:
                return_data = {'result': 'no type'}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def put(self, request, src, form, prg, nnid, ver, node):
        """
        - desc ; update cnn configuration data
        """
        try:
            if (prg == 'source'):
                return_data = WfDataText().put_step_source(src, form, nnid, ver, node, request.data)
            elif (prg == 'pre'):
                return_data = WfDataText().put_step_preprocess(src, form, nnid, ver, node, request.data)
            elif (prg == 'store'):
                return_data = WfDataText().put_step_store(src, form, nnid, ver, node, request.data)
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
