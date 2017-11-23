from cluster.neuralnet.neuralnet_node import NeuralNetNode
from common.utils import *
from master.workflow.netconf.workflow_netconf_cnn import WorkFlowNetConfCNN
from master.network.nn_common_manager import NNCommonManager
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

class NeuralNetNodeNlp(NeuralNetNode):
    def run(self, conf_data):
        '''
        Train run init
        :param conf_data: 
        :return: 
        '''
        try :
            logging.info("run NeuralNetNodeNlp Train")


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
            logging.info("run NeuralNetNodeNlp eval")


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
            logging.info("run NeuralNetNodeNlp predict")


            return ''
        except Exception as e :
            logging.info("===Error on Predict  : {0}".format(e))