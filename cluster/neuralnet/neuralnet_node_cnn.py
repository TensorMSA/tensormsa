from cluster.neuralnet.neuralnet_node import NeuralNetNode
from common.utils import *
from master.workflow.netconf.workflow_netconf_cnn import WorkFlowNetConfCNN
from master.workflow.init.workflow_init_simple import WorkFlowSimpleManager
import tensorflow as tf
import numpy as np
import os
import operator
import datetime
from PIL import Image
Image.LOAD_TRUNCATED_IMAGES = True
import io
from cluster.common.train_summary_info import TrainSummaryInfo

from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import ReduceLROnPlateau, CSVLogger, EarlyStopping
from cluster.neuralnet import resnet

class NeuralNetNodeCnn(NeuralNetNode):
    """
    """
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
    def model_file_delete(self, model_path, modelname):
        existcnt = 20
        filelist = os.listdir(model_path)

        flist = []
        i = 0
        for filename in filelist:
            filetime = datetime.datetime.fromtimestamp(os.path.getctime(model_path + '/' + filename)).strftime(
                '%Y%m%d%H%M%S')
            tmp = [filename, filetime]
            if filename.find(modelname) > -1:
                flist.append(tmp)
            i += 1
            flistsort = sorted(flist, key=operator.itemgetter(1), reverse=True)

        for i in range(len(flistsort)):
            if i > existcnt * 3:
                os.remove(model_path + "/" + flistsort[i][0])
    ########################################################################

    def _init_train_parm(self, conf_data):
        # get initial value
        self.conf_data = conf_data
        self.cls_pool = conf_data["cls_pool"]
        self.nn_id = conf_data["nn_id"]
        self.wf_ver = conf_data["wf_ver"]
        self.node_id = self.get_node_name()
        self.node = self.get_node_def()
        self.saveCnt = 100

        # get feed name
        self.train_feed_name = self.nn_id + "_" + self.wf_ver + "_" + WorkFlowSimpleManager().get_train_feed_node()
        self.eval_feed_name = self.nn_id + "_" + self.wf_ver + "_" + WorkFlowSimpleManager().get_eval_feed_node()
        self.feed_node = self.get_prev_node()
    def _init_predict_parm(self, node_id):
        self.node_id = node_id
    def _init_value(self):
        self.g_total_cnt = 0
        # return data
        self.train_return_data = {}
        self.train_return_arr = ["Trainning .................................................."]
        self.pred_return_data = {}
    ########################################################################
    def _set_netconf_parm(self):
        netconf = WorkFlowNetConfCNN().get_view_obj(self.node_id)
        try:
            netconf = WorkFlowNetConfCNN().set_num_classes_predcnt(self.nn_id, self.wf_ver, self.node, self.node_id, netconf)
        except:
            None
        self.netconf = netconf

        #eval
        config = {"type": self.netconf["config"]["eval_type"], "labels": self.netconf["labels"]}
        self.eval_data = TrainSummaryInfo(conf=config)
        self.eval_data.set_nn_id(self.nn_id)
        self.eval_data.set_nn_wf_ver_id(self.wf_ver)
    ########################################################################
    def _set_dataconf_parm(self, dataconf):
        self.dataconf = dataconf
    ########################################################################

    def get_model_cnn(self, type):
        prenumoutputs = 1
        num_classes = self.netconf["config"]["num_classes"]
        learnrate = self.netconf["config"]["learnrate"]
        numoutputs = self.netconf["config"]["layeroutputs"]
        optimizer = self.netconf["config"]["optimizer"]
        node_out = self.netconf["out"]["node_out"]

        x_size = self.dataconf["preprocess"]["x_size"]
        y_size = self.dataconf["preprocess"]["y_size"]
        channel = self.dataconf["preprocess"]["channel"]
        ################################################################
        X = tf.placeholder(tf.float32, shape=[None, x_size, y_size, channel], name='x')
        Y = tf.placeholder(tf.float32, shape=[None, num_classes], name='y')
        ################################################################
        stopper = 1
        model = X

        while True:
            try:
                layer = self.netconf["layer" + str(stopper)]
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
        W1 = tf.Variable(tf.truncated_normal([reout, node_out], stddev=0.1))
        model = tf.nn.relu(tf.matmul(model, W1))

        W5 = tf.Variable(tf.truncated_normal([node_out, num_classes], stddev=0.1))
        model = tf.matmul(model, W5)
        # println(model)
        if type == "P":
            model = tf.nn.softmax(model)
        cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=model, labels=Y))
        if optimizer == "AdamOptimizer":
            optimizer = tf.train.AdamOptimizer(learning_rate=learnrate).minimize(cost)
        else:
            optimizer = tf.train.RMSPropOptimizer(learnrate, 0.9).minimize(cost)
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
    def get_model_resnet(self, type):
        lr_reducer = ReduceLROnPlateau(monitor='val_loss', factor=np.sqrt(0.1), cooldown=0, patience=5, min_lr=0.5e-6)
        early_stopper = EarlyStopping(monitor='val_acc', min_delta=0.001, patience=10)
        csv_logger = CSVLogger('resnet.csv')
        num_classes = self.netconf["config"]["num_classes"]
        numoutputs = self.netconf["config"]["layeroutputs"]
        x_size = self.dataconf["preprocess"]["x_size"]
        y_size = self.dataconf["preprocess"]["y_size"]
        channel = self.dataconf["preprocess"]["channel"]

        if numoutputs == 18:
            model = resnet.ResnetBuilder.build_resnet_18((channel, x_size, y_size), num_classes)
        elif numoutputs == 34:
            model = resnet.ResnetBuilder.build_resnet_34((channel, x_size, y_size), num_classes)
        elif numoutputs == 50:
            model = resnet.ResnetBuilder.build_resnet_50((channel, x_size, y_size), num_classes)
        elif numoutputs == 101:
            model = resnet.ResnetBuilder.build_resnet_101((channel, x_size, y_size), num_classes)
        elif numoutputs == 152:
            model = resnet.ResnetBuilder.build_resnet_152((channel, x_size, y_size), num_classes)
        elif numoutputs == 200:
            model = resnet.ResnetBuilder.build_resnet_200((channel, x_size, y_size), num_classes)

        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        self.model = model
        self.lr_reducer = lr_reducer
        self.early_stopper = early_stopper
        self.csv_logger = csv_logger
        self.data_augmentation = False
    ########################################################################
    def get_batch_img_data(self, data_set, type):
        num_classes = self.netconf["config"]["num_classes"]
        labels = self.netconf["labels"]
        x_size = self.dataconf["preprocess"]["x_size"]
        y_size = self.dataconf["preprocess"]["y_size"]
        channel = self.dataconf["preprocess"]["channel"]

        labelsHot = self.one_hot_encoded(num_classes)

        name_data_batch = data_set[2]
        label_data_batch = data_set[1]
        img_data_batch = data_set[0]

        if type == "T":
            r = 0
            y_batch = np.zeros((len(label_data_batch), num_classes))
            for j in label_data_batch:
                j = j.decode('UTF-8')
                k = labels.index(j)
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

        try:
            x_batch = np.zeros((len(img_data_batch), len(img_data_batch[0])))
        except Exception as e:
            println(e)
        r = 0
        for j in img_data_batch:
            j = j.tolist()
            x_batch[r] = j
            r += 1

        x_batch = np.reshape(x_batch, (-1, x_size, y_size, channel))

        # println("Image Label ////////////////////////////////////////////////")
        # println(label_data_batch)
        # println(y_batch)
        # println("Image /////////////////////////////////////////////////")
        # println(x_batch)

        return x_batch, y_batch, n_batch
    ########################################################################
    def get_saver_model(self, sess):
        self.model_path = self.netconf["modelpath"]
        self.modelname = self.netconf["modelname"]

        try:
            last_chk_path = tf.train.latest_checkpoint(checkpoint_dir=self.model_path)
            saver = tf.train.Saver()
            saver.restore(sess, save_path=last_chk_path)
            step = last_chk_path.split("-")
            self.step_gap = int(step[1])+10
            println("Train Restored checkpoint from:" + last_chk_path)
        except:
            sess.run(tf.global_variables_initializer())
            self.step_gap = 10
            println("None to restore checkpoint. Initializing variables instead.")

        self.save_path = self.model_path + "/" + self.modelname + "-" + str(self.step_gap)
        return sess, saver
    ########################################################################
    def set_saver_model(self, sess):
        if self.saveCnt > self.train_cnt:
            self.saveCnt = self.train_cnt

        if (self.g_total_cnt % self.saveCnt == 0):
            saver = tf.train.Saver()
            saver.save(sess, save_path=self.save_path)
            self.step_gap = self.step_gap + 10
            self.save_path = self.model_path + "/" + self.modelname + "-" + str(self.step_gap)

            self.model_file_delete(self.model_path, self.modelname)

            batch_accR = round(self.batch_acc * 100, 2)
            msg = "Global Step: " + str(self.g_total_cnt) + ", Training Batch Accuracy: " + str(
                batch_accR) + "%" + ", Cost: " + str(self.i_cost)
            println(msg)
            result = [msg]
            self.train_return_arr.append(result)

            self.eval(self.node_id, self.conf_data, None, None)

    def run(self, conf_data):
        println("run NeuralNetNodeCnn Train")
        # init data setup
        self._init_train_parm(conf_data)
        self._init_value()
        # get data & dataconf
        test_data, dataconf = self.get_input_data(self.feed_node, self.cls_pool, self.eval_feed_name)
        input_data, dataconf = self.get_input_data(self.feed_node, self.cls_pool, self.train_feed_name)

        # set netconf, dataconf
        self._set_netconf_parm()
        self._set_dataconf_parm(dataconf)

        net_type = self.netconf["config"]["net_type"]

        # train
        with tf.Session() as sess:
            if net_type == "resnet":
                self.get_model_resnet("T")
                sess, saver = self.get_saver_model(sess)
                self.return_arr = self.train_run_resnet(sess, input_data, test_data)
            else:
                self.get_model_cnn("T")
                sess, saver = self.get_saver_model(sess)
                self.train_run_cnn(sess, input_data, test_data)

            self.train_return_data["TrainResult"] = self.train_return_arr

        return self.train_return_data

    def train_run_resnet(self, sess, input_data, test_data):
        epoch = self.netconf["param"]["epoch"]
        batch_size = self.netconf["param"]["batch_size"]
        train_cnt = self.netconf["param"]["traincnt"]

        try:
            if not self.data_augmentation:
                println('Not using data augmentation.')
            else:
                println('Using real-time data augmentation.')

            while (input_data.has_next()):
                for i in range(epoch):
                    for i in range(0, input_data.size(), batch_size):
                        data_set = input_data[i:i + batch_size]
                        x_batch, y_batch, n_batch = self.get_batch_img_data(data_set, "T")

                        test_set = test_data[i:i + batch_size]
                        x_tbatch, y_tbatch, n_tbatch = self.get_batch_img_data(test_set, "T")

                        for i in range(train_cnt):
                            if not self.data_augmentation:
                                self.model.fit(x_batch, y_batch,
                                               batch_size=batch_size,
                                               epochs=epoch,
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
                                self.model.fit_generator(datagen.flow(x_batch, y_batch, batch_size=batch_size),
                                                    steps_per_epoch=x_batch.shape[0] // batch_size,
                                                    validation_data=(x_tbatch, y_tbatch),
                                                    epochs=epoch, verbose=1, max_q_size=100,
                                                    callbacks=[self.lr_reducer, self.early_stopper, self.csv_logger])

                            self.g_total_cnt += 1
                            println("Train Count=" + str(self.g_total_cnt))
                            # Print status to screen every 10 iterations (and last).
                            saveCnt = 100
                            if saveCnt > train_cnt:
                                saveCnt = train_cnt
                            # Save a checkpoint to disk every 100 iterations (and last).
                            if (self.g_total_cnt % saveCnt == 0):
                                saver = tf.train.Saver()
                                saver.save(sess, save_path=self.save_path)
                                self.model_file_delete(self.model_path, self.modelname)

                        result = ''
                        self.train_return_arr.append(result)

                input_data.next()
        except Exception as e:
            println("Error[400] ..............................................")
            println(e)

    def train_run_cnn(self, sess, input_data, test_data):
        self.epoch = self.netconf["param"]["epoch"]
        self.batch_size = self.netconf["param"]["batch_size"]
        self.train_cnt = self.netconf["param"]["traincnt"]

        try:
            while (input_data.has_next()):
                for i in range(self.epoch):
                    for i in range(0, input_data.size(), self.batch_size):
                        data_set = input_data[i:i + self.batch_size]
                        x_batch, y_batch, n_batch = self.get_batch_img_data(data_set, "T")

                        for i in range(self.train_cnt):
                            feed_dict_train = {self.X: x_batch, self.Y: y_batch}

                            _, self.i_cost, self.batch_acc = sess.run([self.optimizer, self.cost, self.accuracy], feed_dict=feed_dict_train)

                            self.g_total_cnt += 1
                            println("Train Count=" + str(self.g_total_cnt))
                            self.set_saver_model(sess)

                input_data.next()
        except Exception as e:
            println("Error[400] ..............................................")
            println(e)

        return self.train_return_data

    ########################################################################
    def eval(self, node_id, conf_data, data=None, result=None):
        println("run NeuralNetNodeCnn eval")
        self._init_train_parm(conf_data)

        if self.netconf["config"]["net_type"] == "resnet":
            return self.eval_data

        # get data & dataconf
        test_data, dataconf = self.get_input_data(self.feed_node, self.cls_pool, self.eval_feed_name)

        # set netconf, dataconf
        self._set_netconf_parm()
        self._set_dataconf_parm(dataconf)

        with tf.Session() as sess:
            sess, saver = self.get_saver_model(sess)
            return_eval = self.eval_run(sess, test_data)

        return return_eval

    def eval_run(self, sess, input_data):
        batch_size = self.netconf["param"]["batch_size"]
        labels = self.netconf["labels"]

        t_cnt_arr = []
        f_cnt_arr = []
        for i in range(len(labels)):
            t_cnt_arr.append(0)
            f_cnt_arr.append(0)

        input_data.pointer = 0
        while (input_data.has_next()):
            for i in range(0, input_data.size(), batch_size):
                data_set = input_data[i:i + batch_size]
                x_batch, y_batch, n_batch = self.get_batch_img_data(data_set, "E")

                try:
                    logits, y_pred_true = sess.run([self.model, self.y_pred_cls], feed_dict={self.X: x_batch})

                    for i in range(len(logits)):
                        true_name = y_batch[i]
                        file_name = n_batch[i]
                        pred_name = labels[y_pred_true[i]]
                        # print(self.spaceprint(file_name, 30) + " True Category=" + true_name + " Predict Category=" + pred_name)
                        idx = labels.index(true_name)
                        if true_name == pred_name:
                            t_cnt_arr[idx] = t_cnt_arr[idx] + 1
                        else:
                            f_cnt_arr[idx] = f_cnt_arr[idx] + 1

                        self.eval_data.set_result_info(true_name, pred_name)

                except Exception as e:
                    println(e)
                    println("None to restore checkpoint. Initializing variables instead.")

            input_data.next()

        self.eval_print(labels, t_cnt_arr, f_cnt_arr)
        return self.eval_data

    def eval_print(self, labels, t_cnt_arr, f_cnt_arr):
        println("####################################################################################################")
        result = []
        strResult = "['Eval ......................................................']"
        result.append(strResult)
        totCnt = 0
        tCnt = 0
        fCnt = 0
        for i in range(len(labels)):
            strResult = "Category : " + self.spaceprint(labels[i], 15) + " "
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
        strResult = "Total Category=" + self.spaceprint(str(len(labels)), 11) + " "
        strResult += "TotalCnt=" + self.spaceprint(str(totCnt), 8) + " "
        strResult += "TrueCnt=" + self.spaceprint(str(tCnt), 8) + " "
        strResult += "FalseCnt=" + self.spaceprint(str(fCnt), 8) + " "
        if totCnt != 0:
            strResult += "True Percent(TrueCnt/TotalCnt*100)=" + str(round(tCnt / totCnt * 100)) + "%"
        println(strResult)
        result.append(strResult)
        println("###################################################################################################")

    def predict(self, node_id, filelist):
        """
        """
        println("run NeuralNetNodeCnn Predict")
        # init data setup
        self._init_predict_parm(node_id)
        self._init_value()
        # net, data config setup
        data_node_name = self._get_backward_node_with_type(node_id, 'data')
        dataconf = WorkFlowNetConfCNN().get_view_obj(data_node_name[0])
        self._set_netconf_parm()
        self._set_dataconf_parm(dataconf)

        # data shape change MultiValuDict -> nd array
        filename_arr, filedata_arr = self.change_predict_fileList(filelist, dataconf)

        # get variable values
        self.get_model_cnn("P")

        # predict
        with tf.Session() as sess:
            sess, saver = self.get_saver_model(sess)
            for i in range(len(filename_arr)):
                file_name = filename_arr[i]
                file_data = filedata_arr[i]

                logits, y_pred_true = sess.run([self.model, self.y_pred_cls], feed_dict={self.X: file_data})

                labels = self.netconf["labels"]
                pred_cnt = self.netconf["param"]["predictcnt"]
                retrun_data = self.set_predict_return_cnn_img(labels, logits, pred_cnt)
                self.pred_return_data[file_name] = retrun_data
        return self.pred_return_data

