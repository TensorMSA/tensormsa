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
from PIL import Image
from cluster.data.data_node_image import DataNodeImage
from master.workflow.evalconf.workflow_evalconf import WorkFlowEvalConfig

class NeuralNetNodeReNet(NeuralNetNode):
    """

    """

    def run(self, conf_data):
        #return
        try:
            # init parms
            self._init_node_parm(conf_data['node_id'])
            self.cls_pool = conf_data['cls_pool']

            # get prev node for load data
            feed_node_name = self._get_backward_node_with_type(conf_data['node_id'], 'preprocess')
            train_data_set = self.cls_pool[feed_node_name[0]]
            data_node_name = self._get_backward_node_with_type(conf_data['node_id'], 'data')

            """
            Adapted from keras example cifar10_cnn.py
            Train ResNet-18 on the CIFAR10 small images dataset.

            GPU run command with Theano backend (with TensorFlow, the GPU is automatically used):
                THEANO_FLAGS=mode=FAST_RUN,device=gpu,floatX=float32 python cifar10.py
            """
            lr_reducer = ReduceLROnPlateau(monitor='val_loss', factor=np.sqrt(0.1), cooldown=0, patience=5, min_lr=0.5e-6)
            early_stopper = EarlyStopping(monitor='val_acc', min_delta=0.001, patience=10)
            csv_logger = CSVLogger('resnet18_cifar10.csv')

            netconfig = WorkFlowNetConfReNet().get_view_obj(conf_data['node_id'])
            batch_size = netconfig['batch_size']
            nb_classes = netconfig['nb_classes']
            nb_epoch = netconfig['nb_epoch']
            data_augmentation = (netconfig['data_augmentation']=='True')

            # The data, shuffled and split between train and test sets:
            #(x_train, y_train), (X_test, y_test) = cifar10.load_data()

            data_config = WorkFlowDataImage().get_step_source(data_node_name[0])
            labels = data_config['labels']
            preprocess = data_config['preprocess']

            # input image dimensions
            img_rows, img_cols = preprocess['x_size'], preprocess['y_size']
            # The CIFAR10 images are RGB.
            img_channels = preprocess['channel']

            # load model for train
            if (os.path.exists(''.join([self.md_store_path, '/model.bin'])) == True):
                model = keras.models.load_model(''.join([self.md_store_path, '/model.bin']))
            else:
                model = resnet.ResnetBuilder.build_resnet_18((img_channels, img_rows, img_cols), nb_classes)

            while (train_data_set.has_next()):
                for i in range(0, train_data_set.data_size(), batch_size):
                    data_set = train_data_set[i:i + batch_size]
                    X_train = data_set[0]
                    targets = data_set[1]
                    targets_conv = []
                    len = 0
                    if data_set[0].size < batch_size:
                        len = data_set[0].size
                    else:
                        len = i + batch_size
                    rawdata_conv = np.zeros((X_train.size, X_train[0].size))
                    for j in range(i, len, 1):
                        targets_conv.append(labels.index(str(targets[j], 'utf-8')))
                    r = 0
                    for j in X_train:
                        j = j.tolist()
                        rawdata_conv[r] = j
                        r += 1
                    rawdata_conv = np.reshape(rawdata_conv, (-1, img_rows, img_cols, img_channels))
                    y_train = targets_conv[i:i + batch_size]

                    # Convert class vectors to binary class matrices.
                    Y_train = np_utils.to_categorical(y_train, nb_classes)
                    #Y_test = np_utils.to_categorical(y_test, nb_classes)

                    X_train = rawdata_conv.astype('float32')
                    #X_test = X_test.astype('float32')

                    # subtract mean and normalize
                    mean_image = np.mean(X_train, axis=0)
                    X_train -= mean_image
                    #X_test -= mean_image
                    X_train /= 128.
                    #X_test /= 128.

                    model.compile(loss='categorical_crossentropy',
                                  optimizer='adam',
                                  metrics=['accuracy'])

                    if not data_augmentation:
                        print('Not using data augmentation.')
                        model.fit(X_train, Y_train,
                                  batch_size=batch_size,
                                  nb_epoch=nb_epoch,
                                  validation_data=None,#(X_train, Y_train),
                                  shuffle=True,
                                  callbacks=None)#[lr_reducer], early_stopper, csv_logger])
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
                        model.fit_generator(datagen.flow(X_train, Y_train, batch_size=batch_size),
                                            samples_per_epoch=X_train.shape[0]//batch_size,
                                            #validation_data=(X_test, Y_test),
                                            nb_epoch=nb_epoch, verbose=1, max_q_size=100,
                                            callbacks=[lr_reducer, early_stopper, csv_logger])
                train_data_set.next()

            os.makedirs(self.md_store_path, exist_ok=True)
            keras.models.save_model(model,''.join([self.md_store_path, '/model.bin']))
        except Exception as e:
            raise Exception(e)
        finally:
            keras.backend.clear_session()
        return None

    def _init_node_parm(self, node_id):
        wf_conf = WorkFlowNetConfReNet(node_id)
        self.md_store_path = wf_conf.get_model_store_path()

    def _set_progress_state(self):
        return None

    def predict(self, node_id, parm):
        try:
            # init parms
            self._init_node_parm(node_id)

            if (os.path.exists(''.join([self.md_store_path, '/model.bin'])) == True):
                    netconfig = WorkFlowNetConfReNet().get_view_obj(node_id)
                    batch_size = netconfig['batch_size']
                    model = keras.models.load_model(''.join([self.md_store_path, '/model.bin']))
                    filelist = sorted(parm.items(), key=operator.itemgetter(0))
                    data = {}
                    data_sub = {}
                    pred_cnt = netconfig['pred_cnt']
                    for file in filelist:
                        value = file[1]
                        filename = file[1].name
                        data_node_name = self._get_backward_node_with_type(node_id, 'data')
                        data_config = WorkFlowDataImage().get_step_source(data_node_name[0])
                        labels = data_config['labels']
                        preprocess = data_config['preprocess']

                        # input image dimensions
                        x_size, y_size = preprocess['x_size'], preprocess['y_size']
                        # The CIFAR10 images are RGB.
                        channel = preprocess['channel']

                        im = Image.open(value)
                        image = np.array(DataNodeImage()._resize_file_image(im, preprocess))
                        image = image.transpose(2, 0, 1)
                        image = image.flatten()
                        rawdata_conv = np.zeros((image.size, image[0].size))
                        r = 0
                        for j in image:
                            j = j.tolist()
                            rawdata_conv[r] = j
                            r += 1
                        rawdata_conv = np.reshape(rawdata_conv, (-1, x_size, y_size, channel))
                        image = rawdata_conv.astype('float32')
                        mean_image = np.mean(image, axis=0)
                        image -= mean_image
                        image /= 128.
                        return_value = model.predict(image, batch_size, 0)
                        one = np.zeros((len(labels), 2))
                        for i in range(len(labels)):
                            one[i][0] = i
                            one[i][1] = return_value[0][i]
                        onesort = sorted(one, key=operator.itemgetter(1, 0), reverse=True)
                        for i in range(pred_cnt):
                            key = str(i) + "key"
                            val = str(i) + "val"
                            data_sub[key] = labels[int(onesort[i][0])]
                            data_sub[val] = onesort[i][1]
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
        print('nneval')
        try:
            eval_config_data = WorkFlowEvalConfig().get_view_obj(node_id)
            data_node = self.get_linked_prev_node_with_grp('data')
            data_node_name = data_node[0].get_node_name()
            data_config_data = WorkFlowDataImage().get_step_source(data_node_name)
            labels = data_config_data["labels"]
            config = {"type" : eval_config_data["type"], "labels" : labels}
            train = TrainSummaryInfo(conf=config)
            self.cls_pool = parm['cls_pool']
            eval_node = self.cls_pool[node_id]
            prev_node = eval_node.get_prev_node()
            if prev_node[0].get_node_grp() == 'preprocess':
                feed_node_name = prev_node[0].get_node_name()
            else:
                feed_node_name = prev_node[1].get_node_name()
            eval_data_set = self.cls_pool[feed_node_name]
            self._init_node_parm(self.get_node_name())
            if (os.path.exists(''.join([self.md_store_path, '/model.bin'])) == True):
                model = keras.models.load_model(''.join([self.md_store_path, '/model.bin']))
            else:
                raise Exception('No Model')
            netconfig = WorkFlowNetConfReNet().get_view_obj(self.get_node_name())
            batch_size = 1#netconfig['batch_size']
            nb_classes = netconfig['nb_classes']
            preprocess = data_config_data['preprocess']
            # input image dimensions
            img_rows, img_cols = preprocess['x_size'], preprocess['y_size']
            # The CIFAR10 images are RGB.
            img_channels = preprocess['channel']
            while (eval_data_set.has_next()):
                for i in range(0, eval_data_set.data_size(), batch_size):
                    data_set = eval_data_set[i:i + batch_size]
                    X_train = data_set[0]
                    targets = data_set[1]
                    targets_conv = []
                    len = 0
                    if data_set[0].size < batch_size:
                        len = data_set[0].size
                    else:
                        len = i + batch_size
                    rawdata_conv = np.zeros((X_train.size, X_train[0].size))
                    # for j in range(i, len, 1):
                    #     targets_conv.append(labels.index(str(targets[j], 'utf-8')))
                    r = 0
                    for j in X_train:
                        j = j.tolist()
                        rawdata_conv[r] = j
                        r += 1
                    rawdata_conv = np.reshape(rawdata_conv, (-1, img_rows, img_cols, img_channels))
                    y_train = targets_conv[i:i + batch_size]

                    # Convert class vectors to binary class matrices.
                    Y_train = np_utils.to_categorical(y_train, nb_classes)
                    # Y_test = np_utils.to_categorical(y_test, nb_classes)

                    X_train = rawdata_conv.astype('float32')
                    # X_test = X_test.astype('float32')

                    # subtract mean and normalize
                    mean_image = np.mean(X_train, axis=0)
                    X_train -= mean_image
                    # X_test -= mean_image
                    X_train /= 128.
                    # X_test /= 128.
                    #result = model.evaluate(X_train, Y_train,1,None)
                    return_value = labels[np.argmax(model.predict(X_train, batch_size, 0))]
                    train.set_result_info(str(targets[0],'UTF-8'),return_value)
                eval_data_set.next()
            return train
        except Exception as e:
            raise Exception(e)
        finally:
            keras.backend.clear_session()