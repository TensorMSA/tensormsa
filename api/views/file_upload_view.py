import json,os
from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.files.storage import FileSystemStorage
from common.utils import *
import coreapi
import time
from rest_framework.parsers import FileUploadParser,MultiPartParser
import shutil

# from rest_framework import status
from master.workflow.data.workflow_data_image import WorkFlowDataImage

class FileUploadView(APIView):
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

    def post(self, request, nnid, ver, dir):
        """
        Your docs
        ---
        # Class Name (must be separated by `---`)

        # Description:
            - name: name
              description: Foobar long description goes here
        """
        try:
            return_data = {}
            if len(request.FILES.keys()) > 0:
                i = 0
                return_data_sub = {}
                for key, requestSingleFile in request.FILES.items():

                    file = requestSingleFile
                    filepath = get_source_path(nnid, ver, dir)
                    filename = filepath + "/" + file.name
                    # payload = MultipartEncoder({})
                    # save file on file system
                    if not os.path.exists(filepath):
                        os.makedirs(filepath)
                    j = 1
                    while os.path.isfile(filename):
                        filename = filepath + "/" + file.name+str(j)
                        j += 1

                    fp = open(filename,'wb')

                    for chunk in file.chunks():
                        fp.write(chunk)
                    fp.close()
                    return_data_sub["File"] = "File Create.(" + filename + ")"
                    return_data["File"+str(i)] = return_data_sub
                    i += 1
            else :
                raise Exception("not supported type")
                return_data = {"status": "200", "result": "fail"}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = None
            return Response(json.dumps(return_data))

    def get(self, request, nnid, ver, dir):
        """
        Your docs
        ---
        # Class Name (must be separated by `---`)

        # Description:
            - name: name
              description: Foobar long description goes here
        """
        if nnid == "tmpFilePathTrain" or nnid == "tmpFilePathEval":
            if ver != "list":
                tmpfilepath = get_source_path(nnid, "1", "")
                fileName = time.strftime('%Y%m%d')
                stand = "1".zfill(10)
                stcnt = int(fileName + stand)
                mxcnt = stcnt
                for i in os.listdir(tmpfilepath):
                    try:
                        if int(i) >= mxcnt:
                            mxcnt = int(i) + 1

                        if int(i) < stcnt:
                            shutil.rmtree(tmpfilepath + i)
                    except:
                        None

                mxcnt = str(mxcnt)
                tmpfilepath = get_source_path(nnid, "1", mxcnt)
                return_data = {"path":mxcnt}
            else:
                return_data = []
                tmpfilepath = get_source_path(nnid, "1", dir)
                for i in os.listdir(tmpfilepath):
                    resub = {"filename":i}
                    return_data.append(resub)
        else:
            return_data = WorkFlowDataImage().get_data_node_info(nnid, ver, dir)

        return Response(json.dumps(return_data))

    def put(self, request, nnid, ver, dir):
        pretype = request.data["type"]
        prepath = request.data["path"]
        tmpfilepath = get_source_path(pretype, "1", prepath)
        filepath = get_source_path(nnid, ver, dir)

        for i in os.listdir(tmpfilepath):
            shutil.copy2(tmpfilepath+"/"+i, filepath+"/"+i)

        return_data = {"status": "200", "result": "Success"}
        return Response(json.dumps(return_data))

    def delete(self, request, nnid, ver, dir):
        """
        - desc : delete cnn configuration data
        """
        try:
            file = request.data["filename"]
            filepath = get_source_path(nnid, ver, dir)
            filepath = filepath + "/" + file
            os.remove(filepath)
            return_data = {"status": "200", "result": "Success"}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))
