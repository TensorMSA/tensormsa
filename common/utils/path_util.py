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

def get_source_predict_path(nn_id, wf_ver, predict) :
    """
    conbine parms and return source predict path (before data transformation)
    :param nn_id:
    :param wf_ver:
    :param name:
    :return:
    """

    #path = ''.join([cache.get("source_root"), "/", nn_id, "/", wf_ver, "/", name])
    path = ''.join(["/hoya_src_root", "/", nn_id, "/", wf_ver, "/", predict])
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

def get_yolo_path() :
    path = "/home/dev/hoyai/third_party/yolo/models/pretrain"
    set_filepaths(path)
    return path

def get_filepaths(directory, file_type = "*"):
    """
    utils return file paths under directory
    Modify filtering file type
    :param directory:
    :return:
    """
    import os
    file_paths = []
    for root, directories, files in os.walk(directory):
        for filename in files:
            if file_type == '*':
                filepath = os.path.join(root, filename)
                file_paths.append(filepath)
            else:
                if os.path.splitext(filename)[1].lower() == '.' + file_type:
                    filepath = os.path.join(root, filename)
                    file_paths.append(filepath)

    return file_paths

def del_filepaths(directory, file_type = "*"):
    """
    utils return file paths under directory
    Modify filtering file type
    :param directory:
    :return:
    """
    import os
    file_list = get_filepaths(directory, file_type)
    for file_path in file_list :
        os.remove(file_path)

def set_filepaths(path):
    if not os.path.exists(path):
        os.makedirs(path)