from cluster.neuralnet.neuralnet_node import NeuralNetNode
from common.utils import *
from master.workflow.netconf.workflow_netconf_cnn import WorkFlowNetConfCNN
from master.workflow.init.workflow_init_simple import WorkFlowSimpleManager
import tensorflow as tf
import numpy as np
import os
import operator
import datetime
import matplotlib.pyplot as plt
from PIL import Image
Image.LOAD_TRUNCATED_IMAGES = True
import io
from cluster.common.train_summary_info import TrainSummaryInfo

import keras
from keras.preprocessing.image import ImageDataGenerator
from keras.utils import np_utils
from keras.callbacks import ReduceLROnPlateau, CSVLogger, EarlyStopping
from keras.applications.resnet50 import preprocess_input
from keras.preprocessing import image
from cluster.neuralnet import resnet

class NeuralNetNodeCnn(NeuralNetNode):
    """
    """
    def _init_node_parm(self):
        self.conf_data = None
        self.train_feed_name = None
        self.eval_feed_name = None
        self.node_id = self.get_node_name()
        self.node = self.get_node_def()
        self.model = None
        self.X = None
        self.Y = None
        self.optimizer = None
        self.y_pred_cls = None
        self.accuracy = None
        self.cost = None
        self.global_step = tf.Variable(initial_value=10, name='global_step', trainable=False)
        self.global_step_gap = tf.constant(10)

        self.lr_reducer = None
        self.early_stopper = None
        self.csv_logger = None
        self.data_augmentation = False

    ########################################################################
    def _set_netconf_parm(self, netconf):
        self.num_classes = netconf["config"]["num_classes"]
        self.learnrate = netconf["config"]["learnrate"]
        self.numoutputs = netconf["config"]["layeroutputs"]
        self.optimizer = netconf["config"]["optimizer"]
        self.epoch = netconf["param"]["epoch"]
        self.batch_size = netconf["param"]["batch_size"]
        self.num_classes = netconf["config"]["num_classes"]
        self.labels = netconf["labels"]
        self.modelname = netconf["modelname"]
        self.train_cnt = netconf["param"]["traincnt"]
        self.model_path = netconf["modelpath"]
        self.net_type = netconf["config"]["net_type"]
        self.eval_type = netconf["config"]["eval_type"]
        self.pred_cnt = netconf["param"]["predictcnt"]
        try:
            self.node_out = netconf["out"]["node_out"]
        except:
            None
    ########################################################################
    def _set_dataconf_parm(self, dataconf):
        self.x_size = dataconf["preprocess"]["x_size"]
        self.y_size = dataconf["preprocess"]["y_size"]
        self.channel = dataconf["preprocess"]["channel"]
    ########################################################################
    def one_hot_encoded(self, num_classes):
        one = np.zeros((num_classes, num_classes))

        for i in range(num_classes):
            for j in range(num_classes):
                if i == j:
                    one[i][j] = 1
        return one
    ########################################################################
    def spaceprint(self, val, cnt):
        leng = len(str(val))
        cnt = cnt - leng
        restr = ""
        for i in range(cnt):
            restr += " "
        restr = restr + str(val)
        return restr
    ########################################################################
    def model_file_delete(self):
        existcnt = 20
        filelist = os.listdir(self.model_path)

        flist = []
        i = 0
        for filename in filelist:
            filetime = datetime.datetime.fromtimestamp(os.path.getctime(self.model_path + '/' + filename)).strftime(
                '%Y%m%d%H%M%S')
            tmp = [filename, filetime]
            if filename.find(self.modelname) > -1:
                flist.append(tmp)
            i += 1
            flistsort = sorted(flist, key=operator.itemgetter(1), reverse=True)

        for i in range(len(flistsort)):
            if i > existcnt * 3:
                os.remove(self.model_path + "/" + flistsort[i][0])
    ########################################################################
    def get_model_cnn(self, netconf, type):
        prenumoutputs = 1
        ################################################################
        X = tf.placeholder(tf.float32, shape=[None, self.x_size, self.y_size, self.channel], name='x')
        Y = tf.placeholder(tf.float32, shape=[None, self.num_classes], name='y')
        ################################################################
        stopper = 1
        model = X
        numoutputs = self.numoutputs

        while True:
            try:
                layer = netconf["layer" + str(stopper)]
            except Exception as e:
                if stopper == 1:
                    return "Error[100] layer is None ..............................."
                break
            stopper += 1

            try:
                layercnt = layer["layercnt"]
                for i in range(layercnt):
                    # println(layer)
                    if prenumoutputs == 1:
                        prenumoutputs = numoutputs
                    else:
                        numoutputs = prenumoutputs * 2
                        prenumoutputs = numoutputs
                    active = str(layer["active"])
                    convkernelsize = [int((layer["cnnfilter"][0])), int((layer["cnnfilter"][1]))]
                    maxpkernelsize = [int((layer["maxpoolmatrix"][0])), int((layer["maxpoolmatrix"][1]))]
                    stride = [int((layer["maxpoolstride"][0])), int((layer["maxpoolstride"][1]))]
                    padding = str((layer["padding"]))

                    if active == 'relu':
                        activitaion = tf.nn.relu
                    else:
                        activitaion = tf.nn.relu

                    if str(layer["droprate"]) is not "":
                        droprate = float((layer["droprate"]))
                    else:
                        droprate = 0.0

                    model = tf.contrib.layers.conv2d(inputs=model
                                                     , num_outputs=numoutputs
                                                     , kernel_size=convkernelsize
                                                     , activation_fn=activitaion
                                                     , weights_initializer=tf.contrib.layers.xavier_initializer_conv2d()
                                                     , padding=padding)

                    model = tf.contrib.layers.max_pool2d(inputs=model
                                                         , kernel_size=maxpkernelsize
                                                         , stride=stride
                                                         , padding=padding)

                    if droprate > 0.0 and type == "T":
                        model = tf.nn.dropout(model, droprate)

                    # println(model)
            except Exception as e:
                println("Error[200] Model Create Fail.")
                println(e)

        reout = int(model.shape[1]) * int(model.shape[2]) * int(model.shape[3])
        model = tf.reshape(model, [-1, reout])
        # println(model)
        W1 = tf.Variable(tf.truncated_normal([reout, self.node_out], stddev=0.1))
        model = tf.nn.relu(tf.matmul(model, W1))

        W5 = tf.Variable(tf.truncated_normal([self.node_out, self.num_classes], stddev=0.1))
        model = tf.matmul(model, W5)
        # println(model)
        if type == "P":
            model = tf.nn.softmax(model)
        cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=model, labels=Y))
        if self.optimizer == "AdamOptimizer":
            optimizer = tf.train.AdamOptimizer(learning_rate=self.learnrate).minimize(cost, global_step=self.global_step)
        else:
            optimizer = tf.train.RMSPropOptimizer(self.learnrate, 0.9).minimize(cost, global_step=self.global_step)
        y_pred_cls = tf.argmax(model, 1)
        check_prediction = tf.equal(y_pred_cls, tf.argmax(Y, 1))
        accuracy = tf.reduce_mean(tf.cast(check_prediction, tf.float32))

        self.model = model
        self.X = X
        self.Y = Y
        self.optimizer = optimizer
        self.y_pred_cls = y_pred_cls
        self.accuracy = accuracy
        self.cost = cost
    ########################################################################
    def get_model_resnet(self, netconf, type):
        lr_reducer = ReduceLROnPlateau(monitor='val_loss', factor=np.sqrt(0.1), cooldown=0, patience=5, min_lr=0.5e-6)
        early_stopper = EarlyStopping(monitor='val_acc', min_delta=0.001, patience=10)
        csv_logger = CSVLogger('resnet.csv')

        if self.numoutputs == 18:
            model = resnet.ResnetBuilder.build_resnet_18((self.channel, self.x_size, self.y_size), self.num_classes)
        elif self.numoutputs == 34:
            model = resnet.ResnetBuilder.build_resnet_34((self.channel, self.x_size, self.y_size), self.num_classes)
        elif self.numoutputs == 50:
            model = resnet.ResnetBuilder.build_resnet_50((self.channel, self.x_size, self.y_size), self.num_classes)
        elif self.numoutputs == 101:
            model = resnet.ResnetBuilder.build_resnet_101((self.channel, self.x_size, self.y_size), self.num_classes)
        elif self.numoutputs == 152:
            model = resnet.ResnetBuilder.build_resnet_152((self.channel, self.x_size, self.y_size), self.num_classes)
        elif self.numoutputs == 200:
            model = resnet.ResnetBuilder.build_resnet_200((self.channel, self.x_size, self.y_size), self.num_classes)

        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        self.model = model
        self.lr_reducer = lr_reducer
        self.early_stopper = early_stopper
        self.csv_logger = csv_logger
    ########################################################################
    def get_batch_data(self, data_set, type):
        labelsHot = self.one_hot_encoded(self.num_classes)

        name_data_batch = data_set[2]
        label_data_batch = data_set[1]
        img_data_batch = data_set[0]

        if type == "T":
            r = 0
            y_batch = np.zeros((len(label_data_batch), self.num_classes))
            for j in label_data_batch:
                j = j.decode('UTF-8')
                k = self.labels.index(j)
                y_batch[r] = labelsHot[k]
                r += 1
        else:
            y_batch = []
            for j in label_data_batch:
                j = j.decode('UTF-8')
                y_batch.append(j)

        n_batch = []
        for j in name_data_batch:
            j = j.decode('UTF-8')
            n_batch.append(j)

        x_batch = np.zeros((len(img_data_batch), len(img_data_batch[0])))
        r = 0
        for j in img_data_batch:
            j = j.tolist()
            x_batch[r] = j
            r += 1

        x_batch = np.reshape(x_batch, (-1, self.x_size, self.y_size, self.channel))

        # println("Image Label ////////////////////////////////////////////////")
        # println(label_data_batch)
        # println(y_batch)
        # println("Image /////////////////////////////////////////////////")
        # println(x_batch)

        return x_batch, y_batch, n_batch
    ########################################################################
    def run(self, conf_data):
        println("run NeuralNetNodeCnn Train")
        self._init_node_parm()
        self.conf_data = conf_data
        self.nn_id = conf_data['nn_id']
        self.wfver = conf_data['wf_ver']
        self.train_feed_name = self.nn_id+"_"+self.wfver+"_"+WorkFlowSimpleManager().get_train_feed_node()
        self.eval_feed_name = self.nn_id+"_"+self.wfver+"_"+WorkFlowSimpleManager().get_eval_feed_node()

        netconf = WorkFlowNetConfCNN().get_view_obj(self.node_id)
        netconf = WorkFlowNetConfCNN().set_num_classes_predcnt(self.nn_id, self.wfver, self.node, self.node_id, netconf)
        self._set_netconf_parm(netconf)

        feed_node = self.get_prev_node()
        return_data = {}
        return_arr = []
        for feed in feed_node:
            feed_name = feed.get_node_name()
            if feed_name == self.train_feed_name:
                data_node = feed.get_prev_node()
                for data in data_node:
                    data_name = data.get_node_name()
                    dataconf = WorkFlowNetConfCNN().get_view_obj(data_name)
                    self._set_dataconf_parm(dataconf)
                    cls_pool = conf_data['cls_pool']
                    input_data = cls_pool[feed_name]

                    if self.net_type == "resnet":
                        self.get_model_resnet(netconf, "T")
                        test_data = cls_pool[self.eval_feed_name]
                        return_arr = self.train_run_resnet(input_data, test_data)
                    else:
                        self.get_model_cnn(netconf, "T")
                        return_arr = self.train_run_cnn(input_data)

            return_data["TrainResult"] = return_arr

        return return_data

    def train_run_resnet(self, input_data, test_data):
        try:
            return_arr = []
            g_total_cnt = 0
            save_path = self.model_path + "/" + self.modelname
            if not self.data_augmentation:
                println('Not using data augmentation.')
            else:
                println('Using real-time data augmentation.')
            with tf.Session() as sess:
                try:
                    last_chk_path = tf.train.latest_checkpoint(checkpoint_dir=self.model_path)
                    saver = tf.train.Saver()
                    saver.restore(sess, save_path=last_chk_path)
                    println("Train Restored checkpoint from:" + last_chk_path)
                    step = last_chk_path.split("-")
                    self.global_step = tf.Variable(int(step[1]), name='global_step', trainable=False)
                except:
                    println("None to restore checkpoint. Initializing variables instead.")
                    sess.run(tf.initialize_all_variables())

                while (input_data.has_next()):
                    for i in range(self.epoch):
                        for i in range(0, input_data.size(), self.batch_size):
                            data_set = input_data[i:i + self.batch_size]
                            x_batch, y_batch, n_batch = self.get_batch_data(data_set, "T")

                            test_set = test_data[i:i + self.batch_size]
                            x_tbatch, y_tbatch, n_tbatch = self.get_batch_data(test_set, "T")

                            result = ["Trainning .................................................."]
                            return_arr.append(result)

                            for i in range(self.train_cnt):
                                if not self.data_augmentation:
                                    self.model.fit(x_batch, y_batch,
                                                   batch_size=self.batch_size,
                                                   epochs=self.epoch,
                                                   validation_data=(x_tbatch, y_tbatch),
                                                   shuffle=True,
                                                   callbacks=[self.lr_reducer, self.early_stopper, self.csv_logger])
                                else:
                                    # This will do preprocessing and realtime data augmentation:
                                    datagen = ImageDataGenerator(
                                        featurewise_center=False,  # set input mean to 0 over the dataset
                                        samplewise_center=False,  # set each sample mean to 0
                                        featurewise_std_normalization=False,  # divide inputs by std of the dataset
                                        samplewise_std_normalization=False,  # divide each input by its std
                                        zca_whitening=False,  # apply ZCA whitening
                                        rotation_range=0,  # randomly rotate images in the range (degrees, 0 to 180)
                                        width_shift_range=0.1,
                                        # randomly shift images horizontally (fraction of total width)
                                        height_shift_range=0.1,
                                        # randomly shift images vertically (fraction of total height)
                                        horizontal_flip=True,  # randomly flip images
                                        vertical_flip=False)  # randomly flip images

                                    # Compute quantities required for featurewise normalization
                                    # (std, mean, and principal components if ZCA whitening is applied).
                                    datagen.fit(x_batch)

                                    # Fit the model on the batches generated by datagen.flow().
                                    self.model.fit_generator(datagen.flow(x_batch, y_batch, batch_size=self.batch_size),
                                                        steps_per_epoch=x_batch.shape[0] // self.batch_size,
                                                        validation_data=(x_tbatch, y_tbatch),
                                                        epochs=self.epoch, verbose=1, max_q_size=100,
                                                        callbacks=[self.lr_reducer, self.early_stopper, self.csv_logger])

                                g_total_cnt += 1
                                println("Train Count=" + str(g_total_cnt))
                                # Print status to screen every 10 iterations (and last).
                                saveCnt = 100
                                if saveCnt > self.train_cnt:
                                    saveCnt = self.train_cnt
                                # Save a checkpoint to disk every 100 iterations (and last).
                                if (g_total_cnt % saveCnt == 0):
                                    # batch_accR = round(batch_acc * 100, 2)
                                    # msg = "Global Step: " + str(i_global) + ", Training Batch Accuracy: " + str(batch_accR) + "%" + ", Cost: " + str(i_cost)
                                    # println(msg)
                                    # result = [msg]
                                    # return_arr.append(result)
                                    self.global_step = tf.add(self.global_step, self.global_step_gap)
                                    saver.save(sess, save_path=save_path, global_step=self.global_step)
                                    self.model_file_delete()

                            result = ''
                            return_arr.append(result)

                    input_data.next()
        except Exception as e:
            println("Error[400] ..............................................")
            println(e)

        return return_arr

    def train_run_cnn(self, input_data):
        try:
            return_arr = []
            g_total_cnt = 0
            save_path = self.model_path + "/" + self.modelname

            with tf.Session() as sess:
                try:
                    last_chk_path = tf.train.latest_checkpoint(checkpoint_dir=self.model_path)
                    saver = tf.train.Saver()
                    saver.restore(sess, save_path=last_chk_path)
                    println("Train Restored checkpoint from:" + last_chk_path)
                except:
                    println("None to restore checkpoint. Initializing variables instead.")
                    sess.run(tf.initialize_all_variables())

                while (input_data.has_next()):
                    for i in range(self.epoch):
                        for i in range(0, input_data.size(), self.batch_size):
                            data_set = input_data[i:i + self.batch_size]
                            x_batch, y_batch, n_batch = self.get_batch_data(data_set, "T")

                            result = ["Trainning .................................................."]
                            return_arr.append(result)

                            for i in range(self.train_cnt):
                                feed_dict_train = {self.X: x_batch, self.Y: y_batch}

                                i_global, _, i_cost, batch_acc = sess.run([self.global_step, self.optimizer, self.cost, self.accuracy], feed_dict=feed_dict_train)
                                g_total_cnt += 1
                                println("Train Count=" + str(g_total_cnt))
                                # Print status to screen every 10 iterations (and last).
                                saveCnt = 100
                                if saveCnt > self.train_cnt:
                                    saveCnt = self.train_cnt
                                # Save a checkpoint to disk every 100 iterations (and last).
                                if (g_total_cnt % saveCnt == 0):
                                    batch_accR = round(batch_acc * 100, 2)
                                    msg = "Global Step: " + str(i_global) + ", Training Batch Accuracy: " + str(batch_accR) + "%" + ", Cost: " + str(i_cost)
                                    println(msg)
                                    result = [msg]
                                    return_arr.append(result)

                                    saver.save(sess, save_path=save_path, global_step=self.global_step)
                                    self.model_file_delete()

                                    eval_data = self.eval(self.node_id, self.conf_data, None, None)

                            result = ''
                            return_arr.append(result)

                    input_data.next()
        except Exception as e:
            println("Error[400] ..............................................")
            println(e)

        return return_arr

    ########################################################################
    def eval(self, node_id, conf_data, data=None, result=None):
        eval_data = None
        println("run NeuralNetNodeCnn eval")
        nn_id = conf_data['nn_id']
        wfver = conf_data['wf_ver']

        feed_node = self.get_prev_node()
        for feed in feed_node:
            feed_name = feed.get_node_name()
            if feed_name == self.eval_feed_name:
                data_node = feed.get_prev_node()
                for data in data_node:
                    data_name = data.get_node_name()
                    dataconf = WorkFlowNetConfCNN().get_view_obj(data_name)
                    self._set_dataconf_parm(dataconf)

                    cls_pool = conf_data['cls_pool']

                    if self.net_type == "resnet":
                        config = {"type": self.eval_type, "labels": self.labels}
                        eval_data = TrainSummaryInfo(conf=config)
                        eval_data.set_nn_id(nn_id)
                        eval_data.set_nn_wf_ver_id(wfver)
                        return eval_data

                    if feed_name.find("eval") > 0:
                        input_data = cls_pool[feed_name]
                        eval_data = self.eval_run(input_data)

        return eval_data

    def eval_run(self, input_data):
        config = {"type": self.eval_type, "labels": self.labels}
        eval_data = TrainSummaryInfo(conf=config)
        eval_data.set_nn_id(self.nn_id)
        eval_data.set_nn_wf_ver_id(self.wfver)

        t_cnt_arr = []
        f_cnt_arr = []
        for i in range(len(self.labels)):
            t_cnt_arr.append(0)
            f_cnt_arr.append(0)
        with tf.Session() as sess:
            input_data.pointer = 0
            while (input_data.has_next()):
                for i in range(0, input_data.size(), self.batch_size):
                    data_set = input_data[i:i + self.batch_size]
                    x_batch, y_batch, n_batch = self.get_batch_data(data_set, "E")

                    try:
                        last_chk_path = tf.train.latest_checkpoint(checkpoint_dir=self.model_path)
                        saver = tf.train.Saver()

                        saver.restore(sess, save_path=last_chk_path)
                        println("Eval Restored checkpoint from:" + last_chk_path)

                        logits, y_pred_true = sess.run([self.model, self.y_pred_cls], feed_dict={self.X: x_batch})

                        for i in range(len(logits)):
                            true_name = y_batch[i]
                            file_name = n_batch[i]
                            pred_name = self.labels[y_pred_true[i]]
                            # print(self.spaceprint(file_name, 30) + " True Category=" + true_name + " Predict Category=" + pred_name)
                            idx = self.labels.index(true_name)
                            if true_name == pred_name:
                                t_cnt_arr[idx] = t_cnt_arr[idx] + 1
                            else:
                                f_cnt_arr[idx] = f_cnt_arr[idx] + 1

                            eval_data.set_result_info(true_name, pred_name)

                        # for i in range(len(x_batch)):
                        #     println(n_batch[i])
                            # println(x_batch[i])
                            # xmin, ymin, xmax, ymax, class_num = self.process_predicts(x_batch[i])
                            # cv2.imwrite("/hoya_src_root/mro001/2/01_new/" + n_batch[i], x_batch[i])

                    except Exception as e:
                        println(e)
                        println("None to restore checkpoint. Initializing variables instead.")

                input_data.next()

        println("####################################################################################################")
        result = []
        strResult = "['Eval ......................................................']"
        result.append(strResult)
        totCnt = 0
        tCnt = 0
        fCnt = 0
        for i in range(len(self.labels)):
            strResult = "Category : " + self.spaceprint(self.labels[i], 15) + " "
            strResult += "TotalCnt=" + self.spaceprint(str(t_cnt_arr[i] + f_cnt_arr[i]), 8) + " "
            strResult += "TrueCnt=" + self.spaceprint(str(t_cnt_arr[i]), 8) + " "
            strResult += "FalseCnt=" + self.spaceprint(str(f_cnt_arr[i]), 8) + " "
            if t_cnt_arr[i] + f_cnt_arr[i] != 0:
                strResult += "True Percent(TrueCnt/TotalCnt*100)=" + str(
                    round(t_cnt_arr[i] / (t_cnt_arr[i] + f_cnt_arr[i]) * 100)) + "%"
            totCnt += t_cnt_arr[i] + f_cnt_arr[i]
            tCnt += t_cnt_arr[i]
            fCnt += f_cnt_arr[i]
            println(strResult)
            result.append(strResult)
        strResult = "---------------------------------------------------------------------------------------------------"
        println(strResult)
        strResult = "Total Category=" + self.spaceprint(str(len(self.labels)), 11) + " "
        strResult += "TotalCnt=" + self.spaceprint(str(totCnt), 8) + " "
        strResult += "TrueCnt=" + self.spaceprint(str(tCnt), 8) + " "
        strResult += "FalseCnt=" + self.spaceprint(str(fCnt), 8) + " "
        if totCnt != 0:
            strResult += "True Percent(TrueCnt/TotalCnt*100)=" + str(round(tCnt / totCnt * 100)) + "%"
        println(strResult)
        result.append(strResult)
        println("###################################################################################################")
        return eval_data

    def predict(self, node_id, filelist):
        """
        """
        println("run NeuralNetNodeCnn Predict")
        println(node_id)
        self._init_node_parm()

        data_node_name = self._get_backward_node_with_type(node_id, 'data')

        netconf = WorkFlowNetConfCNN().get_view_obj(node_id)
        dataconf = WorkFlowNetConfCNN().get_view_obj(data_node_name[0])
        self._set_netconf_parm(netconf)
        self._set_dataconf_parm(dataconf)
        if self.net_type == "resnet":
            self.get_model_resnet(netconf, "P")
        else:
            self.get_model_cnn(netconf, "P")

        data = self.predict_run_cnn(filelist)

        return data

    def predict_run_cnn(self, filelist):
        filelist = sorted(filelist.items(), key=operator.itemgetter(0))

        data = {}
        with tf.Session() as sess:
            try:
                last_chk_path = tf.train.latest_checkpoint(checkpoint_dir=self.model_path)
                saverss = tf.train.Saver()
                saverss.restore(sess, save_path=last_chk_path)
                println("Predict Restored checkpoint from:" + last_chk_path)

                for file in filelist:
                    # println(file)
                    value = file[1]
                    filename = file[1].name

                    for img_val in value.chunks():
                        img = Image.open(io.BytesIO(img_val))
                        # println(image)

                        img = img.resize((self.x_size, self.y_size), Image.ANTIALIAS)

                        img = np.array(img)
                        img = img.reshape([-1, self.x_size, self.y_size, self.channel])

                        try:
                            logits, y_pred_true = sess.run([self.model, self.y_pred_cls], feed_dict={self.X: img})
                            # println(logits)
                            # println(y_pred_true)
                            # cls_name = labels[y_pred_true[0]]
                            # println(cls_name)

                            one = np.zeros((len(self.labels), 2))

                            for i in range(len(self.labels)):
                                one[i][0] = i
                                one[i][1] = logits[0][i]

                            onesort = sorted(one, key=operator.itemgetter(1, 0), reverse=True)
                            # println("############################################")
                            # println(onesort)
                            println("filename=" + filename + " predict=" + self.labels[int(onesort[0][0])])
                            # println(onesort)
                            data_sub = {}
                            data_sub_key = []
                            data_sub_val = []
                            for i in range(self.pred_cnt):
                                data_sub_key.append(self.labels[int(onesort[i][0])])
                                val = round(onesort[i][1], 8)*100
                                if val <0:
                                    val = 0
                                data_sub_val.append(val)
                            data_sub["key"] = data_sub_key
                            data_sub["val"] = data_sub_val
                            data[filename] = data_sub
                            # # println(file)
                            # println(data_sub)
                        except:
                            data_sub = {}
                            data_sub_key = []
                            data_sub_val = []
                            for i in range(self.pred_cnt):
                                data_sub_key.append(self.labels[int(onesort[i][0])])
                                val = round(onesort[i][1], 8) * 100
                                if val < 0:
                                    val = 0
                                data_sub_val.append(val)
                            data_sub["key"] = data_sub_key
                            data_sub["val"] = data_sub_val
                            data[filename] = data_sub

            except Exception as e:
                println("None to restore checkpoint. Initializing variables instead.")
                println(e)
        return data

