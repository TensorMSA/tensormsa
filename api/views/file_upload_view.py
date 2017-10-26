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
from master.network.nn_common_manager import NNCommonManager

# from rest_framework import status
from master.workflow.data.workflow_data_image import WorkFlowDataImage

class FileUploadView(APIView):

    coreapi_fields = (
        coreapi.Field(
            name='file',
            required=True,
            type='string',
        ),
    )

    def post(self, request, nnid, ver, dir, type=None):
        """
        File Management Rest Service
        ---
        # Class Name : FileUploadView

        # Description:
            upload actual file via rest api
        """
        try:
            return_data = {}
            if len(request.FILES.keys()) > 0:
                i = 0
                return_data_sub = {}
                for key, requestSingleFile in request.FILES.items():

                    file = requestSingleFile
                    filepath = get_source_path(nnid, ver, dir)
                    if type != None and type.find("store") >= 0:
                        filepath = get_store_path(nnid, ver, dir)
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
                        if file.name.find('.zip') >= 0 :
                            fp.write(chunk)
                        else:
                            fp.write(chunk.decode('cp949').encode('utf-8'))

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

    def get(self, request, nnid, ver, dir, type=None):
        """
        File Management Rest Service
        ---
        # Class Name : FileUploadView

        # Description:
            Get file counts or file name of given network id and version
        """
        if(type != None):
            # tmp 임시 저장소의 값을 만들어서 전달해줌.
            if type.find("tmp") >= 0:
                tmpfilepath = get_source_path(nnid, ver, "")
                if type != None and type.find("store") >= 0:
                    tmpfilepath = get_store_path(nnid, ver, "")

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
                if not os.path.isdir(tmpfilepath+mxcnt):
                    os.mkdir(tmpfilepath+mxcnt)
                return_data = {"path":mxcnt}
            elif type.find("runcheck") >= 0:
                return_data = []
                graph = NNCommonManager().get_nn_node_name(nnid)
                for net in graph:
                    if net['fields']['graph_node'] == 'netconf_data':
                        netconf_data = net['fields']['graph_node_name']
                    if net['fields']['graph_node'] == 'eval_data':
                        eval_data = net['fields']['graph_node_name']
                source_path_n = get_source_path(nnid, ver, netconf_data)
                source_path_e = get_source_path(nnid, ver, eval_data)
                store_path_n = get_store_path(nnid, ver, netconf_data)
                store_path_e = get_store_path(nnid, ver, eval_data)
                source_n_cnt = len(os.listdir(source_path_n))
                source_e_cnt = len(os.listdir(source_path_e))
                store_n_cnt = len(os.listdir(store_path_n))
                store_e_cnt = len(os.listdir(store_path_e))

                if source_n_cnt == 0 and store_n_cnt == 0:
                    resub = {"filecnt":0, "type":"Source"}
                elif source_e_cnt == 0 and store_e_cnt == 0:
                    resub = {"filecnt":0, "type":"Eval"}
                else:
                    resub = {"filecnt":1}

                return_data.append(resub)
            else:
                return_data = []
                tmpfilepath = get_source_path(nnid, ver, dir)
                if type != None and type.find("store") >= 0:
                    tmpfilepath = get_store_path(nnid, ver, dir)
                for i in os.listdir(tmpfilepath):
                    resub = {"filename":i}
                    return_data.append(resub)
        else:
            return_data = WorkFlowDataImage().get_data_node_info(nnid, ver, dir)

        return Response(json.dumps(return_data))

    def put(self, request, nnid, ver, dir):
        """
        File Management Rest Service
        ---
        # Class Name : FileUploadView

        # Description:
            Get file counts or file name of given network id and version
        """
        firsttmpfolder = request.data["first_tmp_folder"]
        lasttmpfolder = request.data["last_tmp_folder"]
        tmpfilepath = get_source_path(firsttmpfolder, ver, lasttmpfolder)
        filepath = get_source_path(nnid, ver, dir)

        for i in os.listdir(tmpfilepath):
            shutil.copy2(tmpfilepath+"/"+i, filepath+"/"+i)

        return_data = {"status": "200", "result": "Success"}
        return Response(json.dumps(return_data))

    def delete(self, request, nnid, ver, dir):
        """
        File Management Rest Service
        ---
        # Class Name : FileUploadView

        # Description:
            delete selected upload file
        """
        try:
            file = request.data["filename"]
            filepath = get_source_path(nnid, ver, dir)

            if request.data["type"] != None and request.data["type"].find("store") >= 0:
                filepath = get_store_path(nnid, ver, dir)
            filepath = filepath + "/" + file

            if (os.path.isfile(filepath)):
                os.remove(filepath)
            elif (os.path.exists(filepath)):
                shutil.rmtree(filepath)

            return_data = {"status": "200", "result": "Success"}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))
