import logging

from cluster.neuralnet.neuralnet_node import NeuralNetNode


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