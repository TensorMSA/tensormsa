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

class NeuralNetNodeReNet(NeuralNetNode):
    """

    """

    def run(self, conf_data):
        try:
            # init parms
            self._init_node_parm(conf_data['node_id'])

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
            # get prev node for load data
            data_node_name = self.find_prev_node(conf_data['node_id'], conf_data['node_list'])
            cls_path, cls_name = self.get_cluster_exec_class(data_node_name)
            dyna_cls = self.load_class(cls_path, cls_name)
            data_config = WorkFlowDataImage().get_step_source(data_node_name)
            labels = data_config['labels']
            input_data = dyna_cls.load_train_data(data_node_name, parm='all')
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

            for data in input_data:
                rawdata = data['image_features']
                targets = data['targets']
                targets_conv = []

                for i in range(0, rawdata.len(), batch_size):
                    len = 0
                    if rawdata.len() < batch_size:
                        len = rawdata.len()
                    else:
                        len = i + batch_size
                    X_train = rawdata[i:i + batch_size]
                    rawdata_conv = np.zeros((X_train.size, X_train[0].size))
                    for j in range(i, len, 1):
                        targets_conv.append(labels.index(str(targets[j], 'utf-8')))
                    r = 0
                    for j in X_train:
                        j = j.tolist()
                        rawdata_conv[r] = j
                        r += 1
                    rawdata_conv = np.reshape(rawdata_conv, (-1, 32, 32, 3))
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
                                  validation_data=(X_train, Y_train),
                                  shuffle=True,
                                  callbacks=[lr_reducer, early_stopper, csv_logger])
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
                                            samples_per_epoch=X_train.shape[0],
                                            #validation_data=(X_test, Y_test),
                                            nb_epoch=nb_epoch, verbose=1, max_q_size=100,
                                            callbacks=[lr_reducer, early_stopper, csv_logger])

            os.makedirs(self.md_store_path, exist_ok=True)
            keras.models.save_model(model,''.join([self.md_store_path, '/model.bin']))
            #model.save(''.join([self.md_store_path, '/model.bin']))
        except Exception as e:
            raise Exception(e)
        return None

    def _init_node_parm(self, node_id):
        wf_conf = WorkFlowNetConfReNet(node_id)
        self.md_store_path = wf_conf.get_model_store_path()

    def _set_progress_state(self):
        return None

    def predict(self, node_id, parm = {}):
        pass

    def eval(self, node_id, parm={}):
        """

        :param node_id:
        :param parm:
        :return:
        """
        pass