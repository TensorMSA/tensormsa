from cluster.neuralnet.neuralnet_node import NeuralNetNode
from master.workflow.netconf.workflow_netconf_fasttext import WorkFlowNetConfFastText as ft_conf
import os, json,logging
import numpy as np
from konlpy.tag import Mecab
from gensim.models.wrappers import FastText

class NeuralNetNodeFastText(NeuralNetNode):

    def run(self, conf_data):
        try :
            # init parms for word2vec node
            self._init_node_parm(conf_data['node_id'])
            self.cls_pool = conf_data['cls_pool']

            # get prev node for load data
            data_node_name = self._get_backward_node_with_type(conf_data['node_id'], 'preprocess')
            train_data_set = self.cls_pool[data_node_name[0]]

            # build vocab first by batch size
            while (train_data_set.has_next()):
                for i in range(0, train_data_set.data_size(), 1):
                    data_set = train_data_set[i:i + 1]
                    print(data_set)

        except Exception as e :
            logging.info("[FastText Train Process] : {0}".format(e))
            raise Exception ("error on fast text tain process : {0}".format(e))