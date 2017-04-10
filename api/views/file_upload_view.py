import json,os
from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.files.storage import FileSystemStorage
from common.utils import *
# from requests_toolbelt import MultipartEncoder
# import requests

from rest_framework.parsers import FileUploadParser,MultiPartParser
# from rest_framework import status
from master.workflow.data.workflow_data_image import WorkFlowDataImage

class FileUploadView(APIView):
    # parser_classes = (FileUploadParser,MultiPartParser, )

    def post(self, request, nnid, ver, dir):

        try:
            # println("post file upload:"+dir)
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
                    # println(return_data_sub)
                    return_data["File"+str(i)] = return_data_sub
                    i += 1
            else :
                raise Exception("not supported type")
                return_data = {"status": "200", "result": "fail"}
            # println(return_data)
            return Response(json.dumps(return_data))
            # up_file = request.FILES['file']
            # payload = MultipartEncoder({up_file.name: up_file})

            # r = requests.post("url",
            #                   data=payload,
            #                   headers = {"Content-Type": payload.content_type})
            #
            # fs = FileSystemStorage()
            # filename = fs.save(up_file.name,up_file)
            # uploaded_file_url = fs.url(filename)
            # return Response(json.dumps(return_data))
            # return render(request,'',{'uploaded_file_url': uploaded_file_url })

        except Exception as e:
            println("file upload post except")
            return_data = None
            return Response(json.dumps(return_data))

    def get(self, request, nnid, ver, dir):
        return_data = WorkFlowDataImage().get_data_node_info(nnid, ver, dir)
        return Response(json.dumps(return_data))