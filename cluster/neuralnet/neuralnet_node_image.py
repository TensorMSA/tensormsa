import logging

import keras
import sys,resource

from cluster.neuralnet.neuralnet_node import NeuralNetNode
from cluster.neuralnet_model import resnet
# from cluster.neuralnet_model.inception_resnet_v2 import InceptionResNetV2
from cluster.neuralnet_model.inception_v4 import inception_v4_model
from master.workflow.netconf.workflow_netconf import WorkFlowNetConf
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import ReduceLROnPlateau, CSVLogger, EarlyStopping
from keras.callbacks import LearningRateScheduler
from common.graph.nn_graph_manager import NeuralNetModel
import tensorflow as tf
import numpy as np
from cluster.common.train_summary_info import TrainSummaryInfo
from keras import optimizers
from keras import backend as backendK
# from keras.utils import multi_gpu_model
from django.conf import settings
# from tools import threadsafe_generator
# from third_party.slim.train_image_classifier import TrainImageClassifier
import matplotlib.pyplot as plt

class NeuralNetNodeImage(NeuralNetNode):
    def lr_schedule(self, epoch):
        """Learning Rate Schedule
        Learning rate is scheduled to be reduced after 80, 120, 160, 180 epochs.
        Called automatically every epoch as part of callbacks during training.
        # Arguments
            epoch (int): The number of epochs
        # Returns
            lr (float32): learning rate
        """
        lr = 1e-3
        if epoch > 180:
            lr *= 0.5e-3
        elif epoch > 160:
            lr *= 1e-3
        elif epoch > 120:
            lr *= 1e-2
        elif epoch > 80:
            lr *= 1e-1

        return lr

    def keras_get_model(self):
        # keras.backend.tensorflow_backend.clear_session()
        backendK.clear_session()
        # if settings.GPU_FLAG == True:
        #     gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.333)
        #     sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options))
        #     backendK.set_session(sess)

        try:
            self.model = keras.models.load_model(self.last_chk_path)
            logging.info("Train Restored checkpoint from:" + self.last_chk_path)
        except Exception as e:
            logging.info("None to restore checkpoint. Initializing variables instead." + self.last_chk_path)
            logging.info(e)

            if self.optimizer == 'sgd':
                self.optimizer = optimizers.SGD(lr=0.001, decay=1e-6, momentum=0.9, nesterov=True)
            elif self.optimizer == 'rmsprop':
                self.optimizer = optimizers.RMSprop(lr=0.001, rho=0.9, epsilon=1e-08, decay=1e-6)
            elif self.optimizer == 'adagrad':
                self.optimizer = optimizers.Adagrad(lr=0.01, epsilon=1e-08, decay=1e-6)
            elif self.optimizer == 'adadelta':
                self.optimizer = optimizers.Adadelta(lr=1.0, rho=0.95, epsilon=1e-08, decay=1e-6)
            elif self.optimizer == 'adam':
                self.optimizer = optimizers.Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=1e-6)
                # self.optimizer = optimizers.Adam(lr=self.lr_schedule(0))
            elif self.optimizer == 'adamax':
                self.optimizer = optimizers.Adamax(lr=0.002, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=1e-6)
            elif self.optimizer == 'nadam':
                self.optimizer = optimizers.Nadam(lr=0.002, beta_1=0.9, beta_2=0.999, epsilon=1e-08, schedule_decay=0.004)

            if self.net_type == 'inceptionv4':
                # self.labels_cnt = 1001
                self.model = inception_v4_model(self.labels_cnt, 0.2, self.pretrain_model_path)
            # elif self.net_type == 'nasnet':
            #     self.model = NASNetLarge(input_shape=(331, 331, 3))
            elif self.net_type == 'resnet':
                numoutputs = self.netconf["config"]["layeroutputs"]

                if numoutputs == 18:
                    self.model = resnet.ResnetBuilder.build_resnet_18((self.channel, self.x_size, self.y_size), self.labels_cnt)
                elif numoutputs == 34:
                    self.model = resnet.ResnetBuilder.build_resnet_34((self.channel, self.x_size, self.y_size), self.labels_cnt)
                elif numoutputs == 50:
                    self.model = resnet.ResnetBuilder.build_resnet_50((self.channel, self.x_size, self.y_size), self.labels_cnt)
                elif numoutputs == 101:
                    self.model = resnet.ResnetBuilder.build_resnet_101((self.channel, self.x_size, self.y_size), self.labels_cnt)
                elif numoutputs == 152:
                    self.model = resnet.ResnetBuilder.build_resnet_152((self.channel, self.x_size, self.y_size), self.labels_cnt)

            # if settings.GPU_FLAG == True:
            #     self.model = multi_gpu_model(self.model, gpus=1)
            self.model.compile(loss='categorical_crossentropy', optimizer=self.optimizer, metrics=['accuracy'])
            # self.model.summary()

    def train_run_image(self, input_data, test_data):
        '''
        Train Run
        :param input_data:
        :param test_data:
        :return:
        '''
        self.epoch = self.netconf["param"]["epoch"]
        self.data_augmentation = self.netconf["param"]["augmentation"]
        try:
            self.fit_size = self.netconf["param"]["fit_size"]
        except:
            self.fit_size = 9999999999

        self.lr_scheduler = LearningRateScheduler(self.lr_schedule)
        self.lr_reducer = ReduceLROnPlateau(monitor='val_loss', factor=np.sqrt(0.1), cooldown=0, patience=5, min_lr=0.5e-6)
        self.early_stopper = EarlyStopping(monitor='val_acc', min_delta=0.001, patience=10)

        try:
            while_cnt = 0
            self.loss = 0
            self.acc = 0
            self.val_loss = 0
            self.val_acc = 0

            input_data.reset_pointer()
            test_data.reset_pointer()

            test_set = test_data[0:test_data.data_size()]
            x_tbatch = self.get_convert_img_x(test_set[0], self.x_size, self.y_size, self.channel) # img_data_batch
            y_tbatch = self.get_convert_img_y(test_set[1], self.labels, self.labels_cnt) # label_data_batch

            while (input_data.has_next()):
                run_size = 0
                while( run_size < input_data.data_size()):
                    if run_size + self.fit_size > input_data.data_size():
                        input_set = input_data[run_size:input_data.data_size()]
                    else:
                        input_set = input_data[run_size:run_size + self.fit_size]
                    run_size += self.fit_size + 1
                    x_batch = self.get_convert_img_x(input_set[0], self.x_size, self.y_size, self.channel)  # img_data_batch
                    y_batch = self.get_convert_img_y(input_set[1], self.labels, self.labels_cnt)  # label_data_batch

                    if len(x_batch) < self.batch_size:
                        self.batch_size = len(x_batch)

                    # # Normalize data.
                    # x_batch = x_batch.astype('float32') / 255
                    # x_tbatch = x_tbatch.astype('float32') / 255

                    # # If subtract pixel mean is enabled
                    # if self.subtract_pixel_mean:
                    #     x_train_mean = np.mean(x_batch, axis=0)
                    #     x_batch -= x_train_mean
                    #     x_tbatch -= x_train_mean

                    if self.data_augmentation == "N" or self.data_augmentation == "n":
                        history = self.model.fit(x_batch, y_batch,
                                                 batch_size=self.batch_size,
                                                 epochs=self.epoch,
                                                 validation_data=(x_tbatch, y_tbatch),
                                                 shuffle=True,
                                                 callbacks=[self.lr_reducer, self.early_stopper, self.lr_scheduler])
                    else:
                        # This will do preprocessing and realtime data augmentation:
                        datagen = ImageDataGenerator(
                            featurewise_center=False,  # set input mean to 0 over the dataset
                            samplewise_center=False,  # set each sample mean to 0
                            featurewise_std_normalization=False,  # divide inputs by std of the dataset
                            samplewise_std_normalization=False,  # divide each input by its std
                            zca_whitening=False,  # apply ZCA whitening
                            rotation_range=0,  # randomly rotate images in the range (degrees, 0 to 180)
                            width_shift_range=0.1, # randomly shift images horizontally (fraction of total width)
                            height_shift_range=0.1, # randomly shift images vertically (fraction of total height)
                            horizontal_flip=True,  # randomly flip images
                            vertical_flip=False)  # randomly flip images

                        # Compute quantities required for featurewise normalization
                        # (std, mean, and principal components if ZCA whitening is applied).
                        datagen.fit(x_batch)

                        # Fit the model on the batches generated by datagen.flow().
                        history = self.model.fit_generator(
                            datagen.flow(x_batch, y_batch, batch_size=self.batch_size),
                            validation_data=(x_tbatch, y_tbatch),
                            epochs=self.epoch, verbose=1, workers=5,
                            steps_per_epoch=x_batch.shape[0] // self.batch_size,
                            callbacks=[self.lr_reducer, self.early_stopper, self.lr_scheduler])

                    self.loss += history.history["loss"][len(history.history["loss"])-1]
                    self.acc += history.history["acc"][len(history.history["acc"])-1]
                    self.val_loss += history.history["val_loss"][len(history.history["val_loss"])-1]
                    self.val_acc += history.history["val_acc"][len(history.history["val_acc"])-1]

                    while_cnt += 1
                input_data.next()

            if while_cnt > 0:
                self.loss =self.loss/while_cnt
                self.acc = self.acc / while_cnt
                self.val_loss = self.val_loss / while_cnt
                self.val_acc = self.val_acc / while_cnt

        except Exception as e:
            logging.info("Error[400] ..............................................")
            logging.info(e)

    def run(self, conf_data):
        '''
        Train run init
        :param conf_data: 
        :return: 
        '''
        try :
            logging.info("run NeuralNetNodeImage Train")
            # Common Start #############################################################################################
            # init value
            self = NeuralNetNode()._init_node_parm(self, conf_data)

            # netconf
            self.netconf = WorkFlowNetConf().get_view_obj(self.node_id)

            # dataconf & get data
            input_data, self.dataconf = self.get_input_data(self.feed_node, self.cls_pool, self.train_feed_name)
            test_data, self.dataconf_eval = self.get_input_data(self.feed_node, self.cls_pool, self.eval_feed_name)
            # Common End ###############################################################################################

            # Label Setup (1: HDF label row)
            self.labels, self.labels_cnt = self._get_netconf_labels(self.netconf, input_data, 1)

            self.channel = self.dataconf["preprocess"]["channel"]
            self.x_size = self.dataconf["preprocess"]["x_size"]
            self.y_size = self.dataconf["preprocess"]["y_size"]
            self.train_cnt = self.netconf["param"]["traincnt"]
            self.batch_size = self.netconf["param"]["batch_size"]
            self.predlog = self.netconf["param"]["predictlog"]
            self.optimizer = self.netconf["config"]["optimizer"]
            # Subtracting pixel mean improves accuracy
            self.subtract_pixel_mean = True

            # get model
            self.keras_get_model()

            for i in range(self.train_cnt):
                # Train
                self.train_run_image(input_data, test_data)

                # Model Save :  _init_node_parm : self.save_path
                keras.models.save_model(self.model, self.save_path)

                # Acc Loss Save : _init_node_parm : self.acc_loss_result
                self.set_acc_loss_result(self.acc_loss_result, self.loss, self.acc, self.val_loss, self.val_acc)

                # Eval & Result Save
                self.eval(self.node_id, self.conf_data, test_data, None)

                # Eval Result Print
                self.eval_result_print(self.eval_data, self.predlog)

            if self.train_cnt == 0:
                # Eval & Result Save
                self.eval(self.node_id, self.conf_data, test_data, None)

                # Eval Result Print
                self.eval_result_print(self.eval_data, self.predlog)

            return None
        except Exception as e :
            logging.info("===Error on Train  : {0}".format(e))

    ####################################################################################################################
    def eval(self, node_id, conf_data, data=None, result=None):
        '''
        eval run init
        :param node_id: 
        :param conf_data: 
        :param data: 
        :param result: 
        :return: 
        '''
        try :
            logging.info("run NeuralNetNodeImage eval")

            pred_cnt = self.netconf["param"]["predictcnt"]
            eval_type = self.netconf["config"]["eval_type"]

            # eval result
            config = {"type": eval_type, "labels": self.labels,
                      "nn_id": self.nn_id,
                      "nn_wf_ver_id": self.nn_wf_ver_id, "nn_batch_ver_id": self.train_batch}
            self.eval_data = TrainSummaryInfo(conf=config)

            if data is None:
                return self.eval_data

            data.reset_pointer()

            while (data.has_next()):
                data_set = data[0:data.data_size()]
                x_batch = self.get_convert_img_x(data_set[0], self.x_size, self.y_size, self.channel)  # img_data_batch

                # # Normalize data.
                # x_batch = x_batch.astype('float32') / 255

                # # If subtract pixel mean is enabled
                # if self.subtract_pixel_mean:
                #     x_train_mean = np.mean(x_batch, axis=0)
                #     x_batch -= x_train_mean

                logits = self.model.predict(x_batch)

                y_batch = self.get_convert_img_y_eval(data_set[1])
                n_batch = self.get_convert_img_y_eval(data_set[2]) # File Name

                for i in range(len(logits)):
                    true_name = y_batch[i]

                    logit = []
                    logit.append(logits[i])
                    retrun_data = self.set_predict_return_cnn_img(self.labels, logit, pred_cnt)
                    pred_name = retrun_data["key"]
                    pred_value = retrun_data["val"]
                    #예측값이 배열로 넘어온다 한개라도 맞으면참
                    t_pred_name = pred_name[0]
                    for pred in pred_name:
                        if pred == true_name:
                            t_pred_name = pred

                    # eval result
                    self.eval_data.set_result_info(true_name, t_pred_name)

                    # Row log를 찍기위해서 호출한다.
                    file_name = n_batch[i]
                    self.eval_data.set_tf_log(file_name, true_name, pred_name, pred_value)

                data.next()

            # eval result
            if self.train_cnt != 0:
                TrainSummaryInfo.save_result_info(self, self.eval_data)

            return self.eval_data

        except Exception as e :
            logging.info("===Error on Eval  : {0}".format(e))

    ####################################################################################################################
    def predict(self, nn_id, ver, filelist):
        '''
        predict
        :param node_id: 
        :param filelist: 
        :return: 
        '''
        logging.info("run NeuralNetNodeImage Predict")
        self.subtract_pixel_mean = True
        self = NeuralNetNode()._init_pred_parm(self, nn_id, ver)
        # net   config setup
        self.netconf = WorkFlowNetConf().get_node_info(nn_id, ver, self.netconf_name)
        self.dataconf = WorkFlowNetConf().get_node_info(nn_id, ver, self.dataconf_name)

        # data shape change MultiValuDict -> nd array
        filename_arr, filedata_arr = self.change_predict_fileList(filelist, self.dataconf)

        # get unique key
        unique_key = '_'.join([str(nn_id), str(ver), self.load_batch])

        logging.info("getModelPath:"+self.model_path + "/" + self.load_batch+self.file_end)

        ## create tensorflow graph
        if (NeuralNetModel.dict.get(unique_key)):
            self = NeuralNetModel.dict.get(unique_key)
            # graph = NeuralNetModel.graph.get(unique_key)
        else:
            self.keras_get_model()

            NeuralNetModel.dict[unique_key] = self
            NeuralNetModel.graph[unique_key] = tf.get_default_graph()
            # graph = tf.get_default_graph()

        pred_return_data = {}
        for i in range(len(filename_arr)):
            file_name = filename_arr[i]
            file_data = filedata_arr[i]

            # # Normalize data.
            # file_data = file_data.astype('float32') / 255

            # # If subtract pixel mean is enabled
            # if self.subtract_pixel_mean:
            #     x_train_mean = np.mean(file_data, axis=0)
            #     file_data -= x_train_mean

            try:
                logits = self.model.predict(file_data)
            except Exception as e:
                self.keras_get_model()

                NeuralNetModel.dict[unique_key] = self
                NeuralNetModel.graph[unique_key] = tf.get_default_graph()
                # graph = tf.get_default_graph()
                logits = self.model.predict(file_data)

            labels = self.netconf["labels"]
            pred_cnt = self.netconf["param"]["predictcnt"]
            retrun_data = self.set_predict_return_cnn_img(labels, logits, pred_cnt)
            pred_return_data[file_name] = retrun_data
            logging.info("Return Data.......................................")
            logging.info(pred_return_data)

        return pred_return_data

    ####################################################################################################################

