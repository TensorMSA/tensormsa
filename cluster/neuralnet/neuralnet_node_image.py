from cluster.neuralnet.neuralnet_node import NeuralNetNode
from common.utils import *
from master.workflow.netconf.workflow_netconf import WorkFlowNetConf
from master.network.nn_common_manager import NNCommonManager
import tensorflow as tf
import numpy as np
import os
import operator
import logging
from cluster.common.train_summary_info import TrainSummaryInfo
import keras
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import ReduceLROnPlateau, CSVLogger, EarlyStopping
from cluster.neuralnet import resnet
from common.graph.nn_graph_manager import NeuralNetModel
from cluster.common.train_summary_accloss_info import TrainSummaryAccLossInfo
from cluster.neuralnet_model.inception_v4 import create_inception_v4
from cluster.neuralnet_model.inception_resnet_v1 import create_inception_resnet_v1
from cluster.neuralnet_model.inception_resnet_v2 import create_inception_resnet_v2
from cluster.neuralnet_model.resnet import create_resnet

class NeuralNetNodeImage(NeuralNetNode):
    def get_model(self):
        keras.backend.tensorflow_backend.clear_session()
        self.lr_reducer = ReduceLROnPlateau(monitor='val_loss', factor=np.sqrt(0.1), cooldown=0, patience=5,
                                            min_lr=0.5e-6)
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
        last_chk_path = self.model_path + "/" + self.load_batch + self.file_end

        try:
            self.model = keras.models.load_model(last_chk_path)
            logging.info("Train Restored checkpoint from:" + last_chk_path)
        except Exception as e:
            logging.info("None to restore checkpoint. Initializing variables instead." + last_chk_path)
            logging.info(e)
            if self.net_type == 'inceptionv4':
                self.model = create_inception_v4()
            elif self.net_type == 'inception_resnet_v1':
                self.model = create_inception_resnet_v1()
            elif self.net_type == 'inception_resnet_v2':
                self.model = create_inception_resnet_v2()
            elif self.net_type == 'resnet':
                self.model = resnet(numoutputs,channel,x_size,y_size,num_classes)

        self.model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])

    def run(self, conf_data):
        '''
        Train run init
        :param conf_data: 
        :return: 
        '''
        try :
            logging.info("run NeuralNetNodeImage Train")

            # init value
            self = NeuralNetNode()._init_node_parm(self, conf_data)

            # netconf & dataconf & get data
            netconf = WorkFlowNetConf().get_view_obj(self.node_id, 'netconf_node')
            input_data, dataconf_train = self.get_input_data(self.feed_node, self.cls_pool, self.train_feed_name)
            test_data, dataconf_eval = self.get_input_data(self.feed_node, self.cls_pool, self.eval_feed_name)

            # get model
            self.get_model()

            return ''
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


            return ''
        except Exception as e :
            logging.info("===Error on Eval  : {0}".format(e))

    ####################################################################################################################
    def predict(self, node_id, filelist):
        '''
        predict
        :param node_id: 
        :param filelist: 
        :return: 
        '''
        try :
            logging.info("run NeuralNetNodeImage predict")


            return ''
        except Exception as e :
            logging.info("===Error on Predict  : {0}".format(e))