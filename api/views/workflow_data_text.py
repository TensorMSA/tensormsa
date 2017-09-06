import json
from rest_framework.response import Response
from rest_framework.views import APIView
from master.workflow.data.workflow_data_text import WorkFlowDataText as WfDataText
from common.utils import *
import coreapi

class WorkFlowDataText(APIView):

    coreapi_fields = (
        coreapi.Field(
            name='type',
            required=True,
            type='string',
        ),
        coreapi.Field(
            name='source_server',
            required=True,
            type='string',
        ),
        coreapi.Field(
            name='source_sql',
            required=True,
            type='string',
        ),
        coreapi.Field(
            name='preprocess',
            required=True,
            type='string',
        ),
    )
    def post(self, request, src, form, prg, nnid, ver, node):
        """
        This API is for set node parameters \n
        This node is for data extraction \n
        This node especially handles text type data \n
        You can set source server by set up parameters \n
        ---
        # Class Name : WorkFlowDataText

        # Description:
            Set params for data source, preprocess method and etc
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
        This API is for set node parameters \n
        This node is for data extraction \n
        This node especially handles text type data \n
        You can set source server by set up parameters \n
        ---
        # Class Name : WorkFlowDataText

        # Description:
            1. Search real data from the source in range (use datamanager instead)
            2. See Data Node Parameters for selected nnid
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
        This API is for set node parameters \n
        This node is for data extraction \n
        This node especially handles text type data \n
        You can set source server by set up parameters \n
        ---
        # Class Name : WorkFlowDataText

        # Description:
            1. Modify selected data (use datamanager instead)
            2. Modify params for data source, preprocess method and etc
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
        This API is for set node parameters \n
        This node is for data extraction \n
        This node especially handles text type data \n
        You can set source server by set up parameters \n
        ---
        # Class Name : WorkFlowDataText

        # Description:
            1. Delete part of data (seleted by user ) conditions or rows (use datamanager instead)
            2. Reset Node parameters
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))
