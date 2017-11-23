import os, keras
from keras.callbacks import ReduceLROnPlateau, CSVLogger, EarlyStopping
import logging
from cluster.neuralnet import resnet

def create_resnet(numoutputs,channel,x_size,y_size,num_classes):
    '''
    get Network Model
    :return: 
    '''
    try:
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

        return model

    except Exception as e:
        logging.error("===Error on Residualnet build model : {0}".format(e))