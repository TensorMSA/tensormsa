from cluster.neuralnet.neuralnet_node import NeuralNetNode
from common.utils import *
from master.workflow.netconf.workflow_netconf_cnn import WorkFlowNetConfCNN
from master.workflow.init.workflow_init_simple import WorkFlowSimpleManager
import tensorflow as tf
import numpy as np
import os
import operator
import datetime, logging
from cluster.common.train_summary_info import TrainSummaryInfo
import keras
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import ReduceLROnPlateau, CSVLogger, EarlyStopping
from cluster.neuralnet import resnet
from common.graph.nn_graph_manager import NeuralNetModel
from cluster.common.train_summary_accloss_info import TrainSummaryAccLossInfo

class History(keras.callbacks.Callback):
    def on_train_begin(self, logs={}):
        self.losses = []
        self.acc = []

    def on_batch_end(self, batch, logs={}):
        self.losses.append(str(logs.get('loss')))
        self.acc.append(str(logs.get('acc')))

class NeuralNetNodeReNet(NeuralNetNode):
    """
    """
    def _init_train_parm(self, conf_data):
        # get initial value
        self.conf_data = conf_data
        self.cls_pool = conf_data["cls_pool"]
        self.nn_id = conf_data["nn_id"]
        self.wf_ver = conf_data["wf_ver"]
        self.node_id = conf_data["node_id"]
        self.node = WorkFlowSimpleManager().get_train_node()

        # get feed name
        self.train_feed_name = self.nn_id + "_" + self.wf_ver + "_" + WorkFlowSimpleManager().get_train_feed_node()
        self.eval_feed_name = self.nn_id + "_" + self.wf_ver + "_" + WorkFlowSimpleManager().get_eval_feed_node()
        self.feed_node = self.get_prev_node()

    def _init_value(self):
        self.g_train_cnt = 0
        self.file_end = '.bin'
        self.train_return_data = {}
        self.train_return_arr = ["Trainning .................................................."]

    ####################################################################################################################
    def _set_netconf_parm(self):
        netconf = WorkFlowNetConfCNN().get_view_obj(self.node_id)
        try:
            netconf = WorkFlowNetConfCNN().set_num_classes_predcnt(self.nn_id, self.wf_ver, self.node, self.node_id, netconf)
        except:
            None
        self.netconf = netconf

        try:
            self.train_cnt = self.netconf["param"]["traincnt"]
            self.epoch = self.netconf["param"]["epoch"]
            self.batch_size = self.netconf["param"]["batch_size"]
            self.model_path = self.netconf["modelpath"]
            self.modelname = self.netconf["modelname"]
        except Exception as e:
            logging.info("NetConf is not exist.")
            logging.info(e)

    def _set_dataconf_parm(self, dataconf):
        self.dataconf = dataconf

    ####################################################################################################################
    def set_saver_model(self):
        self.save_path = self.model_path + "/" + str(self.batch) + str(self.file_end)
        keras.models.save_model(self.model, self.save_path)

        loss = round(self.loss * 100, 2)
        accR = round(self.acc * 100, 2)
        val_loss = round(self.val_loss * 100, 2)
        val_acc = round(self.val_acc * 100, 2)
        msg = "Global Step: " + str(self.g_train_cnt)
        msg += ", Training Loss: " + str(loss) + "%" + ", Training Accuracy: " + str(accR) + "%"
        msg += ", Test Loss: " + str(val_loss) + "%" + ", Test Accuracy: " + str(val_acc) + "%"
        logging.info(msg)

        config = {"nn_id": self.nn_id, "nn_wf_ver_id": self.wf_ver, "nn_batch_ver_id": self.batch}
        result = TrainSummaryAccLossInfo(config)
        result.loss_info["loss"] = str(val_loss)
        result.acc_info["acc"] = str(val_acc)
        self.save_accloss_info(result)

        result = [msg]

        # self.model_file_delete(self.model_path, self.modelname)

        self.train_return_arr.append(result)

        self.eval(self.node_id, self.conf_data, None, None)

    def get_model_resnet(self):
        try :
            keras.backend.tensorflow_backend.clear_session()
            self.lr_reducer = ReduceLROnPlateau(monitor='val_loss', factor=np.sqrt(0.1), cooldown=0, patience=5, min_lr=0.5e-6)
            self.early_stopper = EarlyStopping(monitor='val_acc', min_delta=0.001, patience=10)
            self.csv_logger = CSVLogger('resnet.csv')
            num_classes = self.netconf["config"]["num_classes"]
            numoutputs = self.netconf["config"]["layeroutputs"]
            x_size = self.dataconf["preprocess"]["x_size"]
            y_size = self.dataconf["preprocess"]["y_size"]
            channel = self.dataconf["preprocess"]["channel"]
            optimizer = self.netconf["config"]["optimizer"]

            filelist = os.listdir(self.model_path)
            filelist.sort(reverse=True)
            last_chk_path = self.model_path + "/" + self.load_batch+self.file_end

            try:
                self.model = keras.models.load_model(last_chk_path)
                logging.info("Train Restored checkpoint from:" + last_chk_path)
            except Exception as e:
                if numoutputs == 18:
                    self.model = resnet.ResnetBuilder.build_resnet_18((channel, x_size, y_size), num_classes)
                elif numoutputs == 34:
                    self.model = resnet.ResnetBuilder.build_resnet_34((channel, x_size, y_size), num_classes)
                elif numoutputs == 50:
                    self.model = resnet.ResnetBuilder.build_resnet_50((channel, x_size, y_size), num_classes)
                elif numoutputs == 101:
                    self.model = resnet.ResnetBuilder.build_resnet_101((channel, x_size, y_size), num_classes)
                elif numoutputs == 152:
                    self.model = resnet.ResnetBuilder.build_resnet_152((channel, x_size, y_size), num_classes)
                elif numoutputs == 200:
                    self.model = resnet.ResnetBuilder.build_resnet_200((channel, x_size, y_size), num_classes)
                logging.info("None to restore checkpoint. Initializing variables instead." + last_chk_path)
                logging.info(e)

            self.model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])
        except Exception as e :
            logging.error("===Error on Residualnet build model : {0}".format(e))

    ####################################################################################################################
    def train_run_resnet(self, input_data, test_data):
        data_augmentation = self.netconf["param"]["augmentation"]
        try:
            if data_augmentation == "N" or data_augmentation == "n":
                logging.info('Not using data augmentation.')
            else:
                logging.info('Using real-time data augmentation.')

            while (input_data.has_next()):
                data_set = input_data[0:input_data.data_size()]
                x_batch, y_batch, n_batch = self.get_batch_img_data(data_set, "T")

                test_set = test_data[0:test_data.data_size()]
                x_tbatch, y_tbatch, n_tbatch = self.get_batch_img_data(test_set, "T")

                for i in range(self.train_cnt):
                    if data_augmentation == "N" or data_augmentation == "n":
                        history = self.model.fit(x_batch, y_batch,
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
                        history = self.model.fit_generator(datagen.flow(x_batch, y_batch, batch_size=self.batch_size),
                                            steps_per_epoch=x_batch.shape[0] // self.batch_size,
                                            validation_data=(x_tbatch, y_tbatch),
                                            epochs=self.epoch, verbose=1, max_q_size=100,
                                            callbacks=[self.lr_reducer, self.early_stopper, self.csv_logger])

                    self.loss = history.history["loss"][0]
                    self.acc = history.history["acc"][0]
                    self.val_loss = history.history["val_loss"][0]
                    self.val_acc = history.history["val_acc"][0]

                    self.g_train_cnt += 1
                    logging.info("Save Train Count=" + str(self.g_train_cnt))
                    self.set_saver_model()

                input_data.next()
        except Exception as e:
            logging.info("Error[400] ..............................................")
            logging.info(e)

    def run(self, conf_data):
        try :
            logging.info("run NeuralNetNodeResnet Train")
            # init data setup
            self._init_train_parm(conf_data)
            self._init_value()

            # get data & dataconf
            test_data, dataconf = self.get_input_data(self.feed_node, self.cls_pool, self.eval_feed_name)
            input_data, dataconf = self.get_input_data(self.feed_node, self.cls_pool, self.train_feed_name)

            # set netconf, dataconf
            self._set_netconf_parm()
            self._set_dataconf_parm(dataconf)

            # set batch
            self.load_batch = self.get_eval_batch(self.node_id)
            if self.epoch != 0 and self.train_cnt != 0:
                self.train_batch, self.batch = self.make_batch(self.node_id)
            else:
                self.batch = self.load_batch

            self.get_model_resnet()

            self.train_run_resnet(input_data, test_data)

            self.train_return_data["TrainResult"] = self.train_return_arr

            if self.epoch == 0 or self.train_cnt == 0:
                self.eval(self.node_id, self.conf_data, None, None)

            return self.train_return_data
        except Exception as e :
            logging.info("===Error on running residualnet : {0}".format(e))

    ####################################################################################################################
    def eval_run(self, input_data):
        self.batch_size = self.netconf["param"]["batch_size"]
        labels = self.netconf["labels"]
        pred_cnt = self.netconf["param"]["predictcnt"]
        try:
            predlog = self.netconf["param"]["predictlog"]
        except:
            predlog = "N"
        # logging.info(labels)
        t_cnt_arr = []
        f_cnt_arr = []
        for i in range(len(labels)):
            t_cnt_arr.append(0)
            f_cnt_arr.append(0)

        input_data.pointer = 0
        # eval
        config = {"type": self.netconf["config"]["eval_type"], "labels": self.netconf["labels"],
                  "nn_id": self.nn_id,
                  "nn_wf_ver_id": self.wf_ver, "nn_batch_ver_id": self.batch}

        self.eval_data = TrainSummaryInfo(conf=config)

        while (input_data.has_next()):
            data_set = input_data[0:input_data.data_size()]
            x_batch, y_batch, n_batch = self.get_batch_img_data(data_set, "E")

            try:
                logits = self.model.predict(x_batch)

                for i in range(len(logits)):
                    true_name = y_batch[i]
                    file_name = n_batch[i]

                    logit = []
                    logit.append(logits[i])
                    #
                    idx = labels.index(true_name)
                    retrun_data = self.set_predict_return_cnn_img(labels, logit, pred_cnt)
                    pred_name = retrun_data["key"][0]

                    if self.eval_flag == "E":
                        if true_name == pred_name:
                            t_cnt_arr[idx] = t_cnt_arr[idx] + 1
                            strLog = "[True] : "
                            if (predlog == "TT"):
                                logging.info(strLog + true_name + " FileName=" + file_name)
                                logging.info(retrun_data["key"])
                                logging.info(retrun_data["val"])
                        else:
                            f_cnt_arr[idx] = f_cnt_arr[idx] + 1
                            strLog = "[False] : "
                            if (predlog == "FF"):
                                logging.info(strLog + true_name + " FileName=" + file_name)
                                logging.info(retrun_data["key"])
                                logging.info(retrun_data["val"])
                        if (predlog == "AA"):
                            logging.info(strLog + true_name + " FileName=" + file_name)
                            logging.info(retrun_data["key"])
                            logging.info(retrun_data["val"])
                    else:
                        try:
                            listTF = retrun_data["key"].index(true_name)
                            t_cnt_arr[idx] = t_cnt_arr[idx] + 1
                            strLog = "[True] : "
                            if (predlog == "T"):
                                logging.info(strLog + true_name + " FileName=" + file_name)
                                logging.info(retrun_data["key"])
                                logging.info(retrun_data["val"])
                        except:
                            f_cnt_arr[idx] = f_cnt_arr[idx] + 1
                            strLog = "[False] : "
                            if (predlog == "F"):
                                logging.info(strLog + true_name + " FileName=" + file_name)
                                logging.info(retrun_data["key"])
                                logging.info(retrun_data["val"])
                        if (predlog == "A"):
                            logging.info(strLog + true_name + " FileName=" + file_name)
                            logging.info(retrun_data["key"])
                            logging.info(retrun_data["val"])

                    self.eval_data.set_result_info(true_name, pred_name)

            except Exception as e:
                logging.info(e)
                logging.info("None to restore checkpoint. Initializing variables instead.")

            input_data.next()

        # set parms for db store
        input_data = TrainSummaryInfo.save_result_info(self, self.eval_data)

        self.eval_print(labels, t_cnt_arr, f_cnt_arr)

    def eval_print(self, labels, t_cnt_arr, f_cnt_arr):
        logging.info(
            "####################################################################################################")
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
            logging.info(strResult)
            result.append(strResult)
        strResult = "---------------------------------------------------------------------------------------------------"
        logging.info(strResult)
        strResult = "Total Category=" + self.spaceprint(str(len(labels)), 11) + " "
        strResult += "TotalCnt=" + self.spaceprint(str(totCnt), 8) + " "
        strResult += "TrueCnt=" + self.spaceprint(str(tCnt), 8) + " "
        strResult += "FalseCnt=" + self.spaceprint(str(fCnt), 8) + " "
        if totCnt != 0:
            strResult += "True Percent(TrueCnt/TotalCnt*100)=" + str(round(tCnt / totCnt * 100)) + "%"
        logging.info(strResult)
        result.append(strResult)
        logging.info(
            "###################################################################################################")

    def eval(self, node_id, conf_data, data=None, result=None):
        logging.info("run NeuralNetNodeCnn eval")

        if data == None:
            self.eval_flag = "T"
        else:
            self.eval_flag = "E"

        # get data & dataconf
        test_data, dataconf = self.get_input_data(self.feed_node, self.cls_pool, self.eval_feed_name)

        self.eval_run(test_data)

        return self.eval_data

    ####################################################################################################################
    def predict(self, node_id, filelist):
        """
        """
        logging.info("run NeuralNetNodeCnn Predict")
        self.node_id = node_id
        self._init_value()
        # net, data config setup
        data_node_name = self._get_backward_node_with_type(node_id, 'data')
        dataconf = WorkFlowNetConfCNN().get_view_obj(data_node_name[0])
        self._set_netconf_parm()
        self._set_dataconf_parm(dataconf)

        # data shape change MultiValuDict -> nd array
        filename_arr, filedata_arr = self.change_predict_fileList(filelist, dataconf)

        # get unique key
        self.load_batch = self.get_active_batch(self.node_id)
        unique_key = '_'.join([node_id, self.load_batch])

        logging.info("getModelPath:"+self.model_path + "/" + self.load_batch+self.file_end)

        ## create tensorflow graph
        if (NeuralNetModel.dict.get(unique_key)):
            self = NeuralNetModel.dict.get(unique_key)
            graph = NeuralNetModel.graph.get(unique_key)
        else:
            self.get_model_resnet()

            NeuralNetModel.dict[unique_key] = self
            NeuralNetModel.graph[unique_key] = tf.get_default_graph()
            graph = tf.get_default_graph()
        pred_return_data = {}
        for i in range(len(filename_arr)):
            file_name = filename_arr[i]
            file_data = filedata_arr[i]

            logits = self.model.predict(file_data)

            labels = self.netconf["labels"]
            pred_cnt = self.netconf["param"]["predictcnt"]
            retrun_data = self.set_predict_return_cnn_img(labels, logits, pred_cnt)
            pred_return_data[file_name] = retrun_data
            logging.info("Return Data.......................................")
            logging.info(pred_return_data)

        return pred_return_data