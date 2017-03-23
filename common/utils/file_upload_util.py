import json, os
from common.utils import *

def save_upload_file(request, nnid, ver, dir):


    if len(request.FILES.keys()) > 0:

        for key, requestSingleFile in request.FILES.items():

            file = requestSingleFile
            filepath = get_source_path(nnid, ver, dir)

            if not os.path.exists(filepath):
                os.makedirs(filepath)
            fp = open(filepath + "/" + file.name, 'wb')

            for chunk in file.chunks():
                fp.write(chunk)
            fp.close()
    else:
        raise Exception("no file data exist")


