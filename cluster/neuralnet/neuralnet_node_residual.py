from __future__ import print_function
from cluster.neuralnet.neuralnet_node import NeuralNetNode
from keras.datasets import cifar10
from keras.preprocessing.image import ImageDataGenerator
from keras.utils import np_utils
from keras.callbacks import ReduceLROnPlateau, CSVLogger, EarlyStopping
import numpy as np
import os
import keras
from master.workflow.netconf.workflow_netconf_renet import WorkFlowNetConfReNet
from cluster.neuralnet import resnet
from master.workflow.data.workflow_data_image import WorkFlowDataImage
from cluster.common.train_summary_info import TrainSummaryInfo
import operator
from master.workflow.evalconf.workflow_evalconf import WorkFlowEvalConfig
from keras.applications.resnet50 import preprocess_input
from keras.preprocessing import image
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

    def run(self, conf_data):
        return
        try:
            # init parms
            self._init_node_parm(conf_data['node_id'])
            self.cls_pool = conf_data['cls_pool']
            self.train_batch, self.batch = self.make_batch(conf_data['node_id'])
            if self.train_batch == None :
                path = ''.join([self.md_store_path+'/'+self.batch,'/model.bin'])
            else :
                path = ''.join([self.md_store_path + '/' + self.train_batch, '/model.bin'])

            train_data_set = self.cls_pool[self.wf_state_id + '_' + self.train_feed_node]
            test_data = self.cls_pool[self.wf_state_id + '_' + self.eval_feed_node]
            data_node_name = self._get_backward_node_with_type(conf_data['node_id'], 'data')

            lr_reducer = ReduceLROnPlateau(monitor='val_loss', factor=np.sqrt(0.1), cooldown=0, patience=5, min_lr=0.5e-6)
            early_stopper = EarlyStopping(monitor='val_acc', min_delta=0.001, patience=10)
            csv_logger = CSVLogger('resnet18_cifar10.csv')
            history = History()

            data_config = WorkFlowDataImage().get_step_source(data_node_name[0])
            preprocess = data_config['preprocess']

            # input image dimensions
            img_rows, img_cols = preprocess['x_size'], preprocess['y_size']
            # The CIFAR10 images are RGB.
            img_channels = preprocess['channel']

            # load model for train
            if (os.path.exists(path) == True):
                model = keras.models.load_model(path)
            else:
                model = resnet.ResnetBuilder.build_resnet_18((img_channels, img_rows, img_cols), self.nb_classes)

            while (train_data_set.has_next()):
                data_set = train_data_set[0:train_data_set.data_size()]
                test_data_set = test_data[0:test_data.data_size()]
                X_train = data_set[0]
                X_test = test_data_set[0]
                targets = data_set[1]
                test_targets = test_data_set[1]
                targets_conv = []
                test_targets_conv = []
                rawdata_conv = np.zeros((X_train.size, X_train[0].size))
                test_rawdata_conv = np.zeros((X_test.size, X_test[0].size))
                for j in range(0, data_set[0].size, 1):
                    targets_conv.append(self.labels.index(str(targets[j], 'utf-8')))
                for j in range(0, test_data_set[0].size, 1):
                    test_targets_conv.append(self.labels.index(str(test_targets[j], 'utf-8')))
                r = 0
                for j in X_train:
                    j = j.tolist()
                    rawdata_conv[r] = j
                    r += 1
                r = 0
                for j in X_test:
                    j = j.tolist()
                    test_rawdata_conv[r] = j
                    r += 1
                rawdata_conv = np.reshape(rawdata_conv, (-1, img_rows, img_cols, img_channels))
                test_rawdata_conv = np.reshape(test_rawdata_conv, (-1, img_rows, img_cols, img_channels))
                y_train = targets_conv
                y_test = test_targets_conv

                # Convert class vectors to binary class matrices.
                Y_train = np_utils.to_categorical(y_train, self.nb_classes)
                Y_test = np_utils.to_categorical(y_test, self.nb_classes)

                X_train = rawdata_conv.astype('float32')
                X_test = test_rawdata_conv.astype('float32')

                # subtract mean and normalize
                mean_image = np.mean(X_train, axis=0)
                X_train -= mean_image
                X_test -= mean_image
                X_train /= 128.
                X_test /= 128.

                model.compile(loss='categorical_crossentropy',
                              optimizer='adam',
                              metrics=['accuracy'])

                if not self.data_augmentation:
                    print('Not using data augmentation.')
                    model.fit(X_train, Y_train,
                              batch_size=self.batch_size,
                              nb_epoch=self.nb_epoch,
                              validation_data=(X_test, Y_test),
                              shuffle=True,
                              callbacks=[lr_reducer, early_stopper, csv_logger, history])
                else:
                    print('Using real-time data augmentation.')
                    # This will do preprocessing and realtime data augmentation:
                    datagen = ImageDataGenerator(
                        featurewise_center=False,  # set input mean to 0 over the dataset
                        samplewise_center=False,  # set each sample mean to 0
                        featurewise_std_normalization=False,  # divide inputs by std of the dataset
                        samplewise_std_normalization=False,  # divide each input by its std
                        zca_whitening=False,  # apply ZCA whitening
                        rotation_range=0,  # randomly rotate images in the range (degrees, 0 to 180)
                        width_shift_range=0.1,  # randomly shift images horizontally (fraction of total width)
                        height_shift_range=0.1,  # randomly shift images vertically (fraction of total height)
                        horizontal_flip=True,  # randomly flip images
                        vertical_flip=False)  # randomly flip images

                    # Compute quantities required for featurewise normalization
                    # (std, mean, and principal components if ZCA whitening is applied).
                    datagen.fit(X_train)

                    # Fit the model on the batches generated by datagen.flow().
                    model.fit_generator(datagen.flow(X_train, Y_train, batch_size=self.batch_size),
                                        steps_per_epoch=X_train.shape[0] // self.batch_size,
                                        validation_data=(X_train, Y_train),
                                        epochs=self.nb_epoch, verbose=1, max_q_size=100,
                                        callbacks=[lr_reducer, early_stopper, csv_logger])
                train_data_set.next()

            os.makedirs(self.md_store_path+'/'+self.batch, exist_ok=True)
            keras.models.save_model(model,''.join([self.md_store_path+'/'+self.batch, '/model.bin']))
            config = {"nn_id": conf_data["nn_id"],
                      "nn_wf_ver_id": conf_data["wf_ver"], "nn_batch_ver_id": self.batch}
            result = TrainSummaryAccLossInfo(config)
            result.loss_info["loss"] = history.losses
            result.acc_info["acc"] = history.acc
            self.save_accloss_info(result)
        except Exception as e:
            raise Exception(e)
        finally:
            keras.backend.clear_session()
        return None

    def _init_node_parm(self, node_id):
        wf_conf = WorkFlowNetConfReNet(node_id)
        self.wf_state_id = wf_conf.get_state_id(node_id).pk
        netconfig = wf_conf.get_view_obj(node_id)
        self.md_store_path = netconfig['model_path']
        self.train_feed_node = netconfig['train_feed_node']
        self.eval_feed_node = netconfig['eval_feed_node']
        self.labels = netconfig['labels']
        self.batch_size = netconfig['batch_size']
        self.nb_classes = netconfig['nb_classes']
        self.nb_epoch = netconfig['nb_epoch']
        self.data_augmentation = (netconfig['data_augmentation'] == 'True')
        self.pred_cnt = netconfig['pred_cnt']

    def _set_progress_state(self):
        return None

    def predict(self, node_id, parm):
        try:
            # init parms
            self._init_node_parm(node_id)
            self.batch = self.get_active_batch(node_id)

            if (os.path.exists(''.join([self.md_store_path+'/'+self.batch, '/model.bin'])) == True):
                model = keras.models.load_model(''.join([self.md_store_path+'/'+self.batch, '/model.bin']))
                filelist = sorted(parm.items(), key=operator.itemgetter(0))
                data = {}
                for file in filelist:
                    value = file[1]
                    filename = file[1].name
                    data_node_name = self._get_backward_node_with_type(node_id, 'data')
                    data_config = WorkFlowDataImage().get_step_source(data_node_name[0])
                    preprocess = data_config['preprocess']

                    # input image dimensions
                    x_size, y_size = preprocess['x_size'], preprocess['y_size']

                    img = image.load_img(value, target_size=(x_size, y_size))
                    x = image.img_to_array(img)
                    x = np.expand_dims(x, axis=0)
                    x = preprocess_input(x)
                    return_value = model.predict(x)

                    one = np.zeros((len(self.labels), 2))
                    for i in range(len(self.labels)):
                        one[i][0] = i
                        one[i][1] = return_value[0][i]
                    onesort = sorted(one, key=operator.itemgetter(1, 0), reverse=True)
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
                keras.backend.clear_session()
                return data
            else:
                raise Exception('No Model')
        except Exception as e:
            raise Exception(e)

    def eval(self, node_id, parm, data=None, result=None):
        """

        :param node_id:
        :param parm:
        :return:
        """
        try:
            eval_config_data = WorkFlowEvalConfig().get_view_obj(node_id)
            data_node = self.get_linked_prev_node_with_grp('data')
            data_node_name = data_node[0].get_node_name()
            data_config_data = WorkFlowDataImage().get_step_source(data_node_name)
            self.cls_pool = parm['cls_pool']
            self._init_node_parm(self.get_node_name())
            eval_data_set = self.cls_pool[self.wf_state_id + '_' + self.eval_feed_node]
            total_cnt = eval_data_set.data_size()
            self.batch = self.get_eval_batch(node_id)
            config = {"type": eval_config_data["type"], "labels": self.labels, "nn_id": parm["nn_id"],
                      "nn_wf_ver_id": parm["wf_ver"], "nn_batch_ver_id" : self.batch}
            train = TrainSummaryInfo(conf=config)
            if (os.path.exists(''.join([self.md_store_path+'/'+self.batch, '/model.bin'])) == True):
                model = keras.models.load_model(''.join([self.md_store_path+'/'+self.batch, '/model.bin']))
            else:
                raise Exception('No Model')
            preprocess = data_config_data['preprocess']
            # input image dimensions
            img_rows, img_cols = preprocess['x_size'], preprocess['y_size']
            # The CIFAR10 images are RGB.
            img_channels = preprocess['channel']
            true_cnt = 0
            while (eval_data_set.has_next()):
                for i in range(0, eval_data_set.data_size(), 1):
                    data_set = eval_data_set[i:i+1]
                    X_train = data_set[0]
                    targets = data_set[1]
                    rawdata_conv = np.zeros((X_train.size, X_train[0].size))
                    r = 0
                    for j in X_train:
                        j = j.tolist()
                        rawdata_conv[r] = j
                        r += 1
                    rawdata_conv = np.reshape(rawdata_conv, (-1, img_rows, img_cols, img_channels))

                    X_train = preprocess_input(rawdata_conv)

                    return_values = model.predict(X_train)

                    one = np.zeros((len(self.labels), 2))
                    for i in range(len(self.labels)):
                        one[i][0] = i
                        one[i][1] = return_values[0][i]
                    onesort = sorted(one, key=operator.itemgetter(1, 0), reverse=True)
                    data_sub_key = []
                    for i in range(self.pred_cnt):
                        data_sub_key.append(self.labels[int(onesort[i][0])])
                    if str(targets[0],'UTF-8') in data_sub_key:
                        true_cnt = true_cnt + 1

                    return_value = self.labels[np.argmax(return_values)]
                    train.set_result_info(str(targets[0],'UTF-8'),return_value)
                eval_data_set.next()
            print("Accuracy : " + str(true_cnt / total_cnt * 100))
            return train
        except Exception as e:
            raise Exception(e)
        finally:
            keras.backend.clear_session()