import os
import zipfile
import h5py
import numpy
from PIL import Image, ImageFilter
from cluster.data.data_node import DataNode
from cluster.data.hdf5 import H5PYDataset
from master.workflow.data.workflow_data_image import WorkFlowDataImage
from time import gmtime, strftime
from common import utils
from common.utils import *

class DataNodeImage(DataNode):
    """

    """

    def run(self, conf_data):
        TRAIN = 'cat_vs_dog.zip'
        node_id = conf_data['node_id']
        config_data = WorkFlowDataImage().get_step_source(node_id)
        directory = config_data['source_path']
        output_directory = config_data['store_path']
        output_filename = strftime("%Y-%m-%d-%H:%M:%S", gmtime())

        # Prepare output file
        output_path = os.path.join(output_directory, output_filename)
        h5file = h5py.File(output_path, mode='w')
        dtype = h5py.special_dtype(vlen=numpy.dtype('uint8'))
        hdf_features = h5file.create_dataset('image_features', (2,), dtype=dtype)
        hdf_shapes = h5file.create_dataset('image_features_shapes', (2, 3), dtype='int32')
        hdf_labels = h5file.create_dataset('targets', (2, ), dtype='S10')

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
        #hdf_labels.dims[0].label = 'batch'
        #hdf_labels.dims[1].label = 'index'
        labels = []

        # Convert
        i = 0
        for split, split_size in zip([TRAIN], [25000]):
            # Open the ZIP file
            filename = os.path.join(directory, split)
            zip_file = zipfile.ZipFile(filename, 'r')
            image_names = zip_file.namelist()  # Discard the directory name
            # Shuffle the examples
            if split == TRAIN:
                rng = numpy.random.RandomState(123522)
                rng.shuffle(image_names)
            else:
                image_names.sort(key=lambda fn: int(os.path.splitext(fn[6:])[0]))
            # Convert from JPEG to NumPy arrays
            #with progress_bar(filename, split_size) as bar:
            for image_name in image_names:
                # Save image
                if image_name.count('.') != 0:
                    im = Image.open(zip_file.open(image_name))
                    format_info = config_data['preprocess']
                    image = numpy.array(self._resize_file_image(im, format_info))
                    image = image.transpose(2, 0, 1)
                    hdf_features[i] = image.flatten()
                    hdf_shapes[i] = image.shape
                    # Cats are 0, Dogs are 1
                    if split == TRAIN:
                        hdf_labels[i] = image_name.split('/')[0].encode('utf8')
                    # Update progress
                    i += 1
                else:
                    try:
                        labels.append(image_name.split('/')[0])
                    except Exception as e:
                        print("exception : {0}".format(e))
                        raise Exception(e)
                #bar.update(i if split == TRAIN else i - 25000)
        # Add the labels
        config_data['labels'] = labels
        WorkFlowDataImage().put_step_source(node_id.split('_')[0],node_id.split('_')[1], node_id.split('_')[2], config_data)
        split_dict = {}
        sources = ['image_features', 'targets']
        split_dict['train'] = dict(zip(sources, [(0, 25000)] * 2))
        split_dict['test'] = {sources[0]: (25000, 37500)}
        h5file.attrs['split'] = H5PYDataset.create_split_array(split_dict)

        h5file.flush()
        h5file.close()

        return (output_path,)
        #return None

    def _init_node_parm(self, node_id):
        return None

    def _set_progress_state(self):
        return None

    def _resize_file_image(self, im, format_info):
        """
        load uploaded image and resize
        :param path:
        :return:
        """
        x_size = int(format_info['x_size'])
        y_size = int(format_info['y_size'])
        #dataframe = net_info['dir']
        #table = net_info['table']

        #im = Image.open(path).convert('L')
        width = float(im.size[0])
        height = float(im.size[1])
        newImage = Image.new('RGB', (x_size, y_size), (255))

        if width > height:
            nheight = int(round((x_size / width * height), 0))
            img = im.resize((x_size, nheight), Image.ANTIALIAS).filter(ImageFilter.SHARPEN)
            wtop = int(round(((y_size - nheight) / 2), 0))
            newImage.paste(img, (4, wtop))
        else:
            nwidth = int(round((x_size / height * width), 0))
            if (nwidth == 0):
                nwidth = 1

            img = im.resize((nwidth, y_size), Image.ANTIALIAS).filter(ImageFilter.SHARPEN)
            wleft = int(round(((y_size - nwidth) / 2), 0))
            newImage.paste(img, (wleft, 4))
        width, height = newImage.size

        # save preview on jango static folder
        #self.save_preview_image(newImage, dataframe, table, file_name, label)
        return newImage

    def load_train_data(self, node_id, parm = 'all'):
        config_data = WorkFlowDataImage().get_step_source(node_id)
        output_directory = config_data['store_path']
        fp_list = utils.get_filepaths(output_directory)
        for file_path in fp_list:
            h5file = h5py.File(file_path, mode='r')
            img_data = h5file['image_features']
            targets = h5file['targets']
            labels = config_data['labels']
        return img_data, targets, labels

    def load_test_data(self, node_id, parm='all'):
        return []

# a = DataNodeImage()
# a.run(1)