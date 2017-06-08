from cluster.neuralnet.neuralnet_node import NeuralNetNode
from master.workflow.netconf.workflow_netconf_w2v import WorkFlowNetConfW2V
import os, json
import numpy as np
from konlpy.tag import Mecab
from gensim.models.wrappers import FastText

class NeuralNetNodeFastText(NeuralNetNode):

    def run(self, conf_data):
        try :
            print("not implemented yet!")
            # TODO : implement fasttext with gensim for better word embedding
        except Exception as e :
            raise Exception ("error on fast text tain process : {0}".format(e))