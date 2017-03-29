import os
import zipfile
import h5py
import numpy as np
from PIL import Image, ImageFilter
from cluster.data.data_node import DataNode
from cluster.data.hdf5 import H5PYDataset
from master.workflow.data.workflow_data_image import WorkFlowDataImage
from master.workflow.netconf.workflow_netconf_cnn import WorkFlowNetConfCNN
from time import gmtime, strftime
from common import utils
from common.utils import *
import tensorflow as tf
import shutil
from master import models

class DataNodeImage(DataNode):
    """

    """
    def run(self, conf_data):
        try:
            # println(conf_data)
            dataconf = WorkFlowNetConfCNN().get_view_obj(str(conf_data["node_list"][0]))
            directory = get_source_path(dataconf["key"]["nn_id"], dataconf["key"]["wf_ver_id"], dataconf["key"]["node"])
            output_directory = get_store_path(dataconf["key"]["nn_id"], dataconf["key"]["wf_ver_id"], dataconf["key"]["node"])
            x_size = dataconf["preprocess"]["x_size"]
            y_size = dataconf["preprocess"]["y_size"]
            channel = dataconf["preprocess"]["channel"]
            output_filename = strftime("%Y-%m-%d-%H:%M:%S", gmtime())

            # unzip & remove zip
            ziplist = os.listdir(directory)
            for zipname in ziplist:
                if zipname.find(".zip") > -1:
                    print("Zip=" + zipname)
                    fantasy_zip = zipfile.ZipFile(directory + '/' + zipname)
                    fantasy_zip.extractall(directory)
                    fantasy_zip.close()
                    os.remove(directory + "/" + zipname)

            forderlist = os.listdir(directory)

            filecnt = 0
            for forder in forderlist:
                filelist = os.listdir(directory + '/' + forder)
                for filename in filelist:
                    value = tf.read_file(directory + '/' + forder + '/' + filename)
                    try:
                        decoded_image = tf.image.decode_image(contents=value, channels=channel, name="img")
                        resized_image = tf.image.resize_image_with_crop_or_pad(decoded_image, x_size, y_size)

                        with tf.Session() as sess:
                            image = sess.run(resized_image)
                            image = image.reshape([-1, x_size, y_size, channel])
                        filecnt += 1
                    except:
                        None

            if len(forderlist) > 0 and filecnt > 0:
                output_path = os.path.join(output_directory, output_filename)
                h5file = h5py.File(output_path, mode='w')
                dtype = h5py.special_dtype(vlen=np.dtype('uint8'))
                hdf_features = h5file.create_dataset('image_features', (filecnt,), dtype=dtype)
                hdf_shapes = h5file.create_dataset('image_features_shapes', (filecnt, channel), dtype='int32')
                hdf_labels = h5file.create_dataset('targets', (filecnt,), dtype='S10')

                # Attach shape annotations and scales
                hdf_features.dims.create_scale(hdf_shapes, 'shapes')
                hdf_features.dims[0].attach_scale(hdf_shapes)

                hdf_shapes_labels = h5file.create_dataset('image_features_shapes_labels', (channel,), dtype='S7')
                hdf_shapes_labels[...] = ['channel'.encode('utf8'),
                                          'height'.encode('utf8'),
                                          'width'.encode('utf8')]
                hdf_features.dims.create_scale(hdf_shapes_labels, 'shape_labels')
                hdf_features.dims[0].attach_scale(hdf_shapes_labels)

                # Add axis annotations
                hdf_features.dims[0].label = 'batch'
                i = 0

                labels = dataconf['labels']
                # println(labels)
                for forder in forderlist:
                    filelist = os.listdir(directory + '/' + forder)
                    # println(forder)
                    for filename in filelist:
                        # println(filename)
                        value = tf.read_file(directory + '/' + forder + '/' + filename)
                        # decoded_image = tf.image.decode_jpeg(value, channels=channel)
                        # resized_image = tf.image.resize_images(decoded_image, [x_size, y_size])
                        # resized_image = tf.cast(resized_image, tf.uint8)
                        try:
                            decoded_image = tf.image.decode_image(contents=value, channels=channel, name="img")
                            resized_image = tf.image.resize_image_with_crop_or_pad(decoded_image, x_size, y_size)

                            with tf.Session() as sess:
                                image = sess.run(resized_image)
                                image = image.reshape([-1, x_size, y_size, channel])

                                # println(image)
                                image = image.flatten()
                                hdf_features[i] = image
                                hdf_shapes[i] = image.shape
                                hdf_labels[i] = forder.encode('utf8')
                                i += 1
                        except:
                            println("ErrorFile="+directory + " forder=" + forder + "  name=" + filename)

                    shutil.rmtree(directory + "/" + forder)
                    try:
                        idx = labels.index(forder)
                    except:
                        labels.append(forder)

                dataconf["labels"] = labels
                # println(labels)

                obj = models.NN_WF_NODE_INFO.objects.get(wf_state_id=dataconf["key"]["nn_id"] + "_" + dataconf["key"]["wf_ver_id"], nn_wf_node_name=dataconf["key"]["node"])
                setattr(obj, 'node_config_data', dataconf)
                obj.save()

                h5file.flush()
                h5file.close()

            return None

        except Exception as e:
            println(e)
            raise Exception(e)

    def _init_node_parm(self, node_id):
        return None

    def _set_progress_state(self):
        return None

    def load_data(self, node_id, parm = 'all'):
        dataconf = WorkFlowDataImage().get_step_source(node_id)
        output_directory = get_store_path(dataconf["key"]["nn_id"], dataconf["key"]["wf_ver_id"], dataconf["key"]["node"])
        fp_list = utils.get_filepaths(output_directory)
        return_arr = []
        for file_path in fp_list:
            h5file = h5py.File(file_path, mode='r')
            return_arr.append(h5file)
        return return_arr

    def _resize_file_image(self, im, format_info):
        """
        load uploaded image and resize
        :param path:
        :return:
        """
        x_size = int(format_info['x_size'])
        y_size = int(format_info['y_size'])
        # dataframe = net_info['dir']
        # table = net_info['table']

        # im = Image.open(path).convert('L')
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
        # self.save_preview_image(newImage, dataframe, table, file_name, label)

        return newImage
