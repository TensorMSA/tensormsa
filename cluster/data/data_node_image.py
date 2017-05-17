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


class DataNodeImage(DataNode):
    """
    """

    def _set_dataconf_parm(self, dataconf):
        self.x_size = dataconf["preprocess"]["x_size"]
        self.y_size = dataconf["preprocess"]["y_size"]
        self.channel = dataconf["preprocess"]["channel"]
        self.directory = dataconf["source_path"]
        self.output_directory = dataconf["store_path"]
        self.output_yolo = dataconf["source_path"]+"_yolo"
        self.model_yolo = "/home/dev/hoyai/third_party/yolo/models/pretrain"

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
        println("run yolo")
        set_filepaths(self.output_yolo)
        common_params = {'image_size': self.x_size, 'num_classes': 20, 'batch_size': 1}
        net_params = {'cell_size': 7, 'boxes_per_cell': 2, 'weight_decay': 0.0005}

        net = YoloTinyNet(common_params, net_params, test=True)

        img = tf.placeholder(tf.float32, (1, self.x_size, self.y_size, self.channel))
        predicts = net.inference(img)
        saver = tf.train.Saver(net.trainable_collection)
        return saver, predicts, img

    def run(self, conf_data):
        try:
            println("run DataNodeImage")
            nnid = conf_data['nn_id']
            node_id = conf_data['node_id']
            wf_ver = conf_data['wf_ver']
            net_conf_id = self._find_netconf_node_id(nnid, wf_ver = wf_ver)
            netconf = WorkFlowDataImage().get_step_source(net_conf_id)
            dataconf = WorkFlowDataImage().get_step_source(node_id)
            if dataconf == {}:
                println("/cluster/data/data_node_image DataNodeImage run dataconf("+node_id+") is not Exist")
                return
            else:
                println(node_id)
            self._set_dataconf_parm(dataconf)

            output_filename = strftime("%Y-%m-%d-%H:%M:%S", gmtime())
            output_path = os.path.join(self.output_directory, output_filename)

            labels = netconf['labels']
            try:
                filesize = dataconf["preprocess"]["filesize"]
            except:
                filesize = 1000000

            # unzip & remove zip
            ziplist = os.listdir(self.directory)
            for zipname in ziplist:
                if zipname.find(".zip") > -1:
                    print("Zip=" + zipname)
                    fantasy_zip = zipfile.ZipFile(self.directory + '/' + zipname)
                    fantasy_zip.extractall(self.directory)
                    fantasy_zip.close()
                    os.remove(self.directory + "/" + zipname)

            forderlist = os.listdir(self.directory)

            filecnt = 0
            image_arr = []
            lable_arr = []
            shape_arr = []
            name_arr = []
            processcnt = 1
            createcnt = 1
            tf.reset_default_graph()
            with tf.Session() as sess:
                try:
                    yolo = dataconf["preprocess"]["yolo"]
                    if yolo == "Y" or yolo == "y":
                        yolo_model = self.model_yolo+'/yolo_tiny.ckpt'
                        saver, predicts, img_ph = self.yolo_detection()
                        saver.restore(sess, yolo_model)
                except:
                    yolo = "N"

                for forder in forderlist:
                    try:
                        filelist = os.listdir(self.directory + '/' + forder)
                    except Exception as e:
                        println(e)
                        continue

                    for filename in filelist:
                        try:
                            #PNG -> JPEG
                            img = Image.open(self.directory + '/' + forder + '/' + filename)
                            pngidx = str(type(img)).find("PngImageFile")
                            if pngidx > -1:
                                img = img.convert("RGBA")
                                bg = Image.new("RGBA", img.size, (255, 255, 255))
                                bg.paste(img, (0, 0), img)
                                filename = "Conv_" + str(filename)
                                bg.save(self.directory + '/' + forder + '/' + filename)

                            if self.channel == 1:
                                img = img.convert('L')

                            img = img.resize((self.x_size, self.y_size), Image.ANTIALIAS)
                            img = np.array(img)
                            try:
                                if yolo == "Y" or yolo == "y":
                                    resized_img = cv2.resize(img, (self.x_size, self.y_size))

                                    y_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB)
                                    y_img = y_img.astype(np.float32)
                                    y_img = y_img / 255.0 * 2 - 1
                                    y_img = np.reshape(y_img, (1, self.x_size, self.y_size, self.channel))
                                    np_predict = sess.run(predicts, feed_dict={img_ph: y_img})
                                    xmin, ymin, xmax, ymax, class_num = self.process_predicts(np_predict)
                                    resized_img = resized_img[int(ymin):int(ymax), int(xmin):int(xmax)]

                                    if yolo == "y":
                                        set_filepaths(self.output_yolo+ '/' + forder)
                                        np_img = Image.fromarray(resized_img)
                                        np_img.save(self.output_yolo + '/' + forder + '/' + filename)
                                        img = cv2.resize(resized_img, (self.x_size, self.y_size))
                            except Exception as e:
                                print("yolo file save error......................................." + str(filename))
                                print(e)

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

                            print("Processcnt="+ str(processcnt) + " File=" + self.directory + " forder=" + forder + "  name=" + filename)
                        except:
                            print("Processcnt="+ str(processcnt) + " ErrorFile=" + self.directory + " forder=" + forder + "  name=" + filename)
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
            println(e)
            raise Exception(e)



    def _init_node_parm(self, node_id):
        return None

    def _set_progress_state(self):
        return None

    def load_data(self, node_id="", parm = 'all'):
        dataconf = WorkFlowDataImage().get_step_source(node_id)
        output_directory = dataconf["store_path"]
        return  utils.get_filepaths(output_directory)
