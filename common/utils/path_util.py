import os
from django.core.cache import cache

def get_source_path(nn_id, wf_ver, name) :
    """
    conbine parms and return source path (before data transformation)
    :param nn_id:
    :param wf_ver:
    :param name:
    :return:
    """

    #path = ''.join([cache.get("source_root"), "/", nn_id, "/", wf_ver, "/", name])
    path = ''.join(["/hoya_src_root", "/", nn_id, "/", wf_ver, "/", name])
    set_filepaths(path)
    return path

def get_store_path(nn_id, wf_ver, name) :

    path = ''.join(["/hoya_str_root", "/", str(nn_id), "/", str(wf_ver), "/", str(name)])
    set_filepaths(path)
    return path

def get_model_path(nn_id, wf_ver, name) :
    """
    get model save path
    :param name:
    :return:
    """
    path = ''.join(["/hoya_model_root", "/", nn_id, "/", wf_ver, "/", name])
    #path = ''.join([cache.get("model_root") , "/" , str(nn_id) , "/" , str(wf_ver) , "/" , str(name)])
    set_filepaths(path)
    return path

def get_filepaths(directory):
    """
    utils return file paths under directory
    :param directory:
    :return:
    """
    import os
    file_paths = []
    for root, directories, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)
    return file_paths

def set_filepaths(path):
    if not os.path.exists(path):
        os.makedirs(path)