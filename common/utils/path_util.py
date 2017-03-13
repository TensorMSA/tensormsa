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
    return ''.join([cache.get("source_root") , "/" , nn_id , "/" , wf_ver , "/" , name])

def get_store_path(nn_id, name) :
    """
    conbine parms and return store path (after data transformation, use on net train)
    :param name:
    :return:
    """
    from master import models
    try:
        obj = models.NN_DEF_LIST_INFO.objects.get(nn_id=str(nn_id))
        if(obj != None) :
            return ''.join([cache.get("store_root") , "/" , obj.biz_cate , "/" , obj.biz_sub_cate , "/" , name])
        else :
            return ""
    except Exception as e:
        raise Exception(e)

def get_model_path(nn_id, wf_ver, name) :
    """
    get model save path
    :param name:
    :return:
    """
    path = ''.join([cache.get("model_root") , "/" , nn_id , "/" , wf_ver , "/" , name])
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