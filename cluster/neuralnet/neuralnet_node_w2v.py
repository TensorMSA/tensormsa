from cluster.neuralnet.neuralnet_node import NeuralNetNode
from gensim.models import word2vec
from master.workflow.netconf.workflow_netconf_w2v import WorkFlowNetConfW2V
import os, json
import numpy as np
from konlpy.tag import Mecab

class NeuralNetNodeWord2Vec(NeuralNetNode):

    def run(self, conf_data):
        try :
            # init parms for word2vec node
            self._init_node_parm(conf_data['node_id'])
            self.cls_pool = conf_data['cls_pool']

            # get prev node for load data
            data_node_name = self._get_backward_node_with_type(conf_data['node_id'], 'preprocess')
            train_data_set = self.cls_pool[data_node_name[0]]

            # load model for train
            update_flag = False
            model = word2vec.Word2Vec(size=self.vector_size , window=self.window_size, min_count=5, workers=4)
            if (os.path.exists(self._get_model_path()) == True):
                model = word2vec.Word2Vec.load(self._get_model_path())
                update_flag = True


            # train per files in folder
            while(train_data_set.has_next()) :
                # Iteration is to improve for Model Accuracy
                for x in range(0, self.iter_size) :
                    # Per Line in file
                    for i in range(0, train_data_set.data_size(), self.batch_size):
                        data_set = train_data_set[i:i + self.batch_size]
                        filtered_data = [data_set[np.logical_not(data_set == '#')].tolist()]
                        if (update_flag == False):
                            model.build_vocab(filtered_data, update=False)
                            update_flag = True
                        else:
                            model.build_vocab(filtered_data, update=True)
                        model.train(filtered_data)
                #Select Next file
                train_data_set.next()

            os.makedirs(self.md_store_path, exist_ok=True)
            model.save(self._get_model_path())
            return len(model.raw_vocab)
        except Exception as e:
            raise Exception(e)

    def _init_node_parm(self, node_id):
        wf_conf = WorkFlowNetConfW2V(node_id)
        self.md_store_path = wf_conf.get_model_store_path()
        self.window_size = wf_conf.get_window_size()
        self.vector_size = wf_conf.get_vector_size()
        self.batch_size = wf_conf.get_batch_size()
        self.iter_size = wf_conf.get_iter_size()

    def _get_model_path(self):
        return ''.join([self.md_store_path, '/model.bin'])


    def _set_progress_state(self):
        return None

    def predict(self, node_id, parm = {"type" : "vector", "val_1" : [], "val_2" : []}):
        """
        predict service _get_model_path
        1. type (vector) : return vector
        2. type (sim) : positive list & negative list
        :param node_id:
        :param parm:
        :return:
        """

        try :
            self._init_node_parm(node_id)
            return_val = []
            if (os.path.exists(self._get_model_path()) == False):
                raise Exception ("No pretrained model exist")

            model = word2vec.Word2Vec.load(self._get_model_path())
            if(parm['type'] in ['vector', 'sim', 'similarity']):
                if ('val_1' in parm): parm['val_1'] = self._pos_raw_data(parm['val_1'])
                if ('val_2' in parm): parm['val_2'] = self._pos_raw_data(parm['val_2'])

            if(parm['type'] in ['vector','train']) :
                for key in parm['val_1'] :
                    if key in ['#'] :
                        return_val.append([0.] * self.vector_size)
                    elif key in model :
                        return_val.append(model[key])
                    else :
                        return_val.append([0.] * self.vector_size)
            elif(parm['type'] == 'sim') :
                return_val.append(model.most_similar(positive=parm['val_1'], negative=parm['val_2'] , topn=5))
            elif(parm['type'] == 'similarity') :
                return_val.append(model.similarity(parm['val_1'][0], parm['val_2'][0]))
            elif(parm['type'] == 'dict' or parm['type'] == 'vocab2index') :
                for key in parm['val_1'] :
                    if key in model : return_val.append(model.wv.vocab[key].index)
                    else : return_val.append(0)
            elif(parm['type'] == 'index2vocab'):
                for key in parm['val_1']:
                    if len(model.wv.index2word) >= key:
                        return_val.append(model.wv.index2word[key])
            elif(parm['type'] == 'povb2vocab') :
                for key in parm['val_1']:
                    filter_list = []
                    for filter_set in filter_list :
                        if filter_set in model :
                            key[model.wv.vocab[filter_set].index] = 0.0
                    index = key.argmax(axis=0)
                    if len(model.wv.index2word) >= index:
                        return_val.append(model.wv.index2word[index])
            elif(parm['type'] == 'vec2word'):
                for key in parm['val_1']:
                    for guess in model.similar_by_vector(key) :
                        if guess[0] not in ['\n', '#', './SF'] and guess[1] > 0:
                            return_val = return_val + [guess[0]]
                            break
            elif (parm['type'] == 'vocablen'):
                return len(model.wv.vocab) - 1
            else :
                raise Exception ("Not available type : {0}".format(parm['type']))
            return return_val
        except Exception as e :
            raise Exception (e)

    def _pos_raw_data(self, lt):
        """

        :param lt: list type value
        :return:
        """
        mecab = Mecab('/usr/local/lib/mecab/dic/mecab-ko-dic')
        return_arr= []
        for raw in lt :
            pos = mecab.pos(raw)
            for word, tag in pos:
                return_arr.append("{0}/{1}".format(word, tag))
        return return_arr

    def eval(self, node_id, parm={}):
        """

        :param node_id:
        :param parm:
        :return:
        """
        pass