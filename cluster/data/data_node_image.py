import os
import zipfile
import numpy as np
from PIL import Image, ImageFilter
from cluster.data.data_node import DataNode
from master.workflow.data.workflow_data_image import WorkFlowDataImage
from time import gmtime, strftime
from common import utils
from common.utils import *
import shutil
import tensorflow as tf
from third_party.yolo.yolo.net.yolo_tiny_net import YoloTinyNet
import cv2
import requests
import logging

class DataNodeImage(DataNode):
    """
    """
    # yolo
    def get_confirm_token(self, response):
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value

        return None

    def save_response_content(self, response, destination):
        CHUNK_SIZE = 32768

        with open(destination, "wb") as f:
            for chunk in response.iter_content(CHUNK_SIZE):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)

    def download_file_from_google_drive(self, URL, destination):
        session = requests.Session()

        response = session.get(URL, params={'id': 1}, stream=True)
        token = self.get_confirm_token(response)

        if token:
            params = {'id': 1, 'confirm': token}
            response = session.get(URL, params=params, stream=True)

        self.save_response_content(response, destination)

    def process_predicts(self, predicts):
        p_classes = predicts[0, :, :, 0:20]
        C = predicts[0, :, :, 20:22]
        coordinate = predicts[0, :, :, 22:]

        p_classes = np.reshape(p_classes, (7, 7, 1, 20))
        C = np.reshape(C, (7, 7, 2, 1))

        P = C * p_classes

        index = np.argmax(P)

        index = np.unravel_index(index, P.shape)

        class_num = index[3]

        coordinate = np.reshape(coordinate, (7, 7, 2, 4))

        max_coordinate = coordinate[index[0], index[1], index[2], :]

        xcenter = max_coordinate[0]
        ycenter = max_coordinate[1]
        w = max_coordinate[2]
        h = max_coordinate[3]

        xcenter = (index[1] + xcenter) * (self.x_size / 7.0)
        ycenter = (index[0] + ycenter) * (self.y_size / 7.0)

        w = w * self.x_size
        h = h * self.y_size

        xmin = xcenter - w / 2.0
        ymin = ycenter - h / 2.0

        xmax = xmin + w
        ymax = ymin + h

        return xmin, ymin, xmax, ymax, class_num

    def yolo_detection(self):
        # logging.info("run yolo")
        set_filepaths(self.output_yolo)
        common_params = {'image_size': self.x_size, 'num_classes': 20, 'batch_size': 1}
        net_params = {'cell_size': 7, 'boxes_per_cell': 2, 'weight_decay': 0.0005}

        net = YoloTinyNet(common_params, net_params, test=True)

        img = tf.placeholder(tf.float32, (1, self.x_size, self.y_size, self.channel))
        predicts = net.inference(img)
        saver = tf.train.Saver(net.trainable_collection)
        return saver, predicts, img

    # image convert
    def image_convert(self, sess, dataconf, img, filename, forder=None):
        set_flag = "N"
        if forder == None:# forder None = predict call
            set_flag = "Y"
            forder = "tmp"
        else:# forder exist = make hdf5
            if self.set_flag == "N":
                self.set_flag = "Y"
                set_flag = "Y"

        if set_flag == "Y":
            self.x_size = dataconf["preprocess"]["x_size"]
            self.y_size = dataconf["preprocess"]["y_size"]
            self.channel = dataconf["preprocess"]["channel"]
            self.directory = dataconf["source_path"]
            self.output_yolo = dataconf["source_path"] + "_yolo"
            self.model_yolo = get_yolo_path()
            self.yolo_tiny = self.model_yolo + '/yolo_tiny.ckpt'
            self.yolo_face = self.model_yolo + '/YOLO_face.tar.gz'
            self.yolo_model = self.yolo_tiny
            self.tiny_url = 'https://drive.google.com/uc?id=0B-yiAeTLLamRekxqVE01Yi1RRlk&export=download'
            self.face_url = "https://drive.google.com/uc?id=0B2JbaJSrWLpzMzR5eURGN2dMTk0&export=download"
            try:
                self.yolo = dataconf["preprocess"]["yolo"]
                if self.yolo == "Y" or self.yolo == "y":
                    if os.path.isfile(self.yolo_model):
                        None
                    else:  # yolo_tiny down :
                        try:
                            self.download_file_from_google_drive(self.tiny_url, self.yolo_tiny)
                            self.download_file_from_google_drive(self.face_url, self.yolo_face)
                        except:
                            logging.info("Error : yolo_tiny,ckpt down.")

                    saver, self.predicts, self.img_ph = self.yolo_detection()
                    saver.restore(sess, self.yolo_model)
            except:
                self.yolo = "N"

        # png -> jpg
        pngidx = str(type(img)).find("PngImageFile")
        if pngidx > -1:
            img = img.convert("RGBA")
            bg = Image.new("RGBA", img.size, (255, 255, 255))
            bg.paste(img, (0, 0), img)
            filename = "Conv_" + str(filename)
            bg.save(self.directory + '/' + forder + '/' + filename)
            img = Image.open(self.directory + '/' + forder + '/' + filename)

        # grey color
        if self.channel == 1:
            img = img.convert('L')

        # image cropping
        longer_side = max(img.size)
        horizontal_padding = (longer_side - img.size[0]) / 2
        vertical_padding = (longer_side - img.size[1]) / 2
        img = img.crop(
            (
                -horizontal_padding,
                -vertical_padding,
                img.size[0] + horizontal_padding,
                img.size[1] + vertical_padding
            )
        )

        # set_filepaths(self.output_yolo + '/' + forder)
        # img.save(self.output_yolo + '/' + forder + '/' + filename)

        # image resize
        img = img.resize((self.x_size, self.y_size), Image.ANTIALIAS)
        img = np.array(img)

        # yolo
        if self.yolo == "Y" or self.yolo == "y":
            if self.x_size<385 or self.y_size<385:
                logging.info("Error : The Yolo x_size or y_size must be greater than 385 pixel")

            else:
                try:
                    resized_img = cv2.resize(img, (self.x_size, self.y_size))
                    img = np.array(img)

                    y_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB)
                    y_img = y_img.astype(np.float32)
                    y_img = y_img / 255.0 * 2 - 1
                    y_img = np.reshape(y_img, (1, self.x_size, self.y_size, self.channel))
                    np_predict = sess.run(self.predicts, feed_dict={self.img_ph: y_img})
                    xmin, ymin, xmax, ymax, class_num = self.process_predicts(np_predict)
                    resized_img = resized_img[int(ymin):int(ymax), int(xmin):int(xmax)]

                    if self.yolo == "y":
                        set_filepaths(self.output_yolo + '/' + forder)
                        np_img = Image.fromarray(resized_img)
                        np_img.save(self.output_yolo + '/' + forder + '/' + filename)
                        img = cv2.resize(resized_img, (self.x_size, self.y_size))
                except Exception as e:
                    print("yolo file save error......................................." + str(filename))
                    print(e)

        return sess, img

    def run(self, conf_data):
        try:
            logging.info("run DataNodeImage")
            nnid = conf_data['nn_id']
            node_id = conf_data['node_id']
            wf_ver = conf_data['wf_ver']
            net_conf_id = self._find_netconf_node_id(nnid, wf_ver = wf_ver)
            netconf = WorkFlowDataImage().get_step_source(net_conf_id)
            dataconf = WorkFlowDataImage().get_step_source(node_id)
            if dataconf == {}:
                logging.info("/cluster/data/data_node_image DataNodeImage run dataconf("+node_id+") is not Exist")
                return
            else:
                logging.info(node_id)

            directory = dataconf["source_path"]
            output_directory = dataconf["store_path"]
            self.set_flag = "N"

            output_filename = strftime("%Y-%m-%d-%H:%M:%S", gmtime())
            output_path = os.path.join(output_directory, output_filename)

            labels = netconf['labels']
            try:
                filesize = dataconf["preprocess"]["filesize"]
            except:
                filesize = 1000000

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
            forderlist.sort()

            filecnt = 0
            image_arr = []
            lable_arr = []
            shape_arr = []
            name_arr = []
            processcnt = 1
            createcnt = 1
            tf.reset_default_graph()

            with tf.Session() as sess:
                for forder in forderlist:
                    try:
                        filelist = os.listdir(directory + '/' + forder)
                    except Exception as e:
                        logging.info(e)
                        continue

                    for filename in filelist:
                        try:
                            #PNG -> JPEG
                            img = Image.open(directory + '/' + forder + '/' + filename)
                            sess, img = self.image_convert(sess, dataconf, img, filename, forder)

                            img = img.reshape([-1, self.x_size, self.y_size, self.channel])
                            img = img.flatten()

                            image_arr.append(img)
                            shape_arr.append(img.shape)
                            lable_arr.append(forder.encode('utf8'))
                            name_arr.append(filename.encode('utf8'))
                            filecnt += 1

                            if filecnt >= filesize :
                                output_path_sub = output_path+"_"+str(createcnt)
                                hdf_create(self, output_path_sub, filecnt, self.channel, image_arr, shape_arr, lable_arr, name_arr)

                                filecnt = 0
                                image_arr = []
                                lable_arr = []
                                shape_arr = []
                                name_arr = []
                                createcnt += 1

                            print("Processcnt="+ str(processcnt) + " File=" + directory + " forder=" + forder + "  name=" + filename)
                        except:
                            print("Processcnt="+ str(processcnt) + " ErrorFile=" + directory + " forder=" + forder + "  name=" + filename)
                        processcnt += 1
                    shutil.rmtree(self.directory + "/" + forder)
                    try:
                        idx = labels.index(forder)
                    except:
                        labels.append(forder)

            if filecnt > 0:
                output_path_sub = output_path + "_" + str(createcnt)
                hdf_create(self, output_path_sub, filecnt, self.channel, image_arr, shape_arr, lable_arr, name_arr)

            netconf["labels"] = labels
            WorkFlowDataImage().put_step_source_ori(net_conf_id, netconf)

            return None

        except Exception as e:
            logging.info(e)
            raise Exception(e)



    def _init_node_parm(self, node_id):
        return None

    def _set_progress_state(self):
        return None

    def load_data(self, node_id="", parm = 'all'):
        dataconf = WorkFlowDataImage().get_step_source(node_id)
        output_directory = dataconf["store_path"]
        return  utils.get_filepaths(output_directory)
