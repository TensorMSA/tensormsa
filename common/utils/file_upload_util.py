import json, os
from common.utils import *
import h5py
import numpy as np

def save_upload_file(request, nnid, ver, dir):
    """
    save files upload via http
    :param request:
    :param nnid:
    :param ver:
    :param dir:
    :return:
    """

    file_cnt = len(request.FILES.keys())
    if file_cnt > 0:
        for key, requestSingleFile in request.FILES.items():

            file = requestSingleFile
            filepath = get_source_path(nnid, ver, dir)

            if not os.path.exists(filepath):
                os.makedirs(filepath)
            fp = open(filepath + "/" + file.name, 'wb')

            for chunk in file.chunks():
                fp.write(chunk)
            fp.close()
        return file_cnt
    else:
        return 0


def hdf_create(self, output_path, filecnt, channel, image_arr, shape_arr, lable_arr, name_arr):
    h5file = h5py.File(output_path, mode='w')
    dtype = h5py.special_dtype(vlen=np.dtype('uint8'))
    hdf_features = h5file.create_dataset('image_features', (filecnt,), dtype=dtype)
    hdf_shapes = h5file.create_dataset('image_features_shapes', (filecnt, channel),dtype='int32')
    hdf_labels = h5file.create_dataset('targets', (filecnt,), dtype='S240')
    hdf_names = h5file.create_dataset('names', (filecnt,), dtype='S240')

    # Attach shape annotations and scales
    hdf_features.dims.create_scale(hdf_shapes, 'shapes')
    hdf_features.dims[0].attach_scale(hdf_shapes)

    hdf_shapes_labels = h5file.create_dataset('image_features_shapes_labels', (3,), dtype='S7')
    hdf_shapes_labels[...] = ['channel'.encode('utf8'),
                              'height'.encode('utf8'),
                              'width'.encode('utf8')]
    hdf_features.dims.create_scale(hdf_shapes_labels, 'shape_labels')
    hdf_features.dims[0].attach_scale(hdf_shapes_labels)

    # Add axis annotations
    hdf_features.dims[0].label = 'batch'

    for i in range(len(image_arr)):
        hdf_features[i] = image_arr[i]
        hdf_shapes[i] = shape_arr[i]
        hdf_labels[i] = lable_arr[i]
        hdf_names[i] = name_arr[i]

    h5file.flush()
    h5file.close()