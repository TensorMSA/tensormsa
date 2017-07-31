import os
import datetime

class NeuralNetModel :
    variable = {}
    dict = {}
    graph = {}
    sess = {}
    tf = {}
    init = {}
    saver = {}


    def check_duplicate(key, data, target, extra=None):
        """
        check duplicate nn_id for none necessary memory use
        :param key: insert key
        :param data: inert data 
        :param target: target variable to update
        :param extra: if there is extra action to do
        :return boolean : always return True  
        """
        try :
            dicts = list(map(lambda x : x.split('__')[0] ,list(target.keys())))
            for dict in dicts :
                if key.split('__')[0] == dict :
                    if (extra == 'sess') :
                        target[key].close()
                    del target[key]
        except Exception as e :
            pass
        finally :
            target[key] = data
            return True

    def set_variable(key, data):
        NeuralNetModel.check_duplicate(key, data, NeuralNetModel.variable)

    def set_dict(key, data):
        NeuralNetModel.check_duplicate(key, data, NeuralNetModel.dict)

    def set_graph(key, data):
        NeuralNetModel.check_duplicate(key, data, NeuralNetModel.graph)

    def set_sess(key, data):
        NeuralNetModel.check_duplicate(key, data, NeuralNetModel.sess, extra='sess')

    def set_tf(key, data):
        NeuralNetModel.check_duplicate(key, data, NeuralNetModel.tf)

    def set_init(key, data):
        NeuralNetModel.check_duplicate(key, data, NeuralNetModel.init)

    def set_saver(key, data):
        NeuralNetModel.check_duplicate(key, data, NeuralNetModel.saver)