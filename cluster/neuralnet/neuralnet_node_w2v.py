from cluster.neuralnet.neuralnet_node import NeuralNetNode
from gensim.models import word2vec
from master.workflow.netconf.workflow_netconf_w2v import WorkFlowNetConfW2V
import os, json, logging
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
            model = word2vec.Word2Vec(size=self.vector_size , window=self.window_size, min_count=self.min_count, workers=4)
            if (os.path.exists(self._get_model_path()) == True):
                model = word2vec.Word2Vec.load(self._get_model_path())
                update_flag = True

            # build vocab first by batch size
            while(train_data_set.has_next()) :
                # Iteration is to improve for Model Accuracy
                for x in range(0, self.iter_size) :
                    # Per Line in file
                    for i in range(0, train_data_set.data_size(), self.batch_size):
                        data_set = train_data_set[i:i + self.batch_size]
                        if (update_flag == False):
                            model.build_vocab(data_set, update=False)
                            update_flag = True
                        else:
                            model.build_vocab(data_set, update=True)
                train_data_set.next()

            # after all new vocab stacked on voacb start train
            train_data_set.reset_pointer()
            while (train_data_set.has_next()):
                # Iteration is to improve for Model Accuracy
                for x in range(0, self.iter_size):
                    # Per Line in file
                    for i in range(0, train_data_set.data_size(), self.batch_size):
                        data_set = train_data_set[i:i + self.batch_size]
                        model.train(data_set)
                train_data_set.next()

            os.makedirs(self.md_store_path, exist_ok=True)
            model.save(self._get_model_path())
            return True
        except Exception as e:
            logging.info("[Word2vec Train Process] : {0}".format(e))
            raise Exception(e)

    def _init_node_parm(self, node_id):
        wf_conf = WorkFlowNetConfW2V(node_id)
        self.md_store_path = wf_conf.get_model_store_path()
        self.window_size = wf_conf.get_window_size()
        self.vector_size = wf_conf.get_vector_size()
        self.batch_size = wf_conf.get_batch_size()
        self.iter_size = wf_conf.get_iter_size()
        self.min_count = wf_conf.get_min_count()
        self.preprocess = wf_conf.preprocess_type()

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
                if ('val_1' in parm) :
                    parm['val_1'] = np.array(self._preprocess(parm['val_1'], type=self.preprocess)).flatten().tolist()
                if ('val_2' in parm) :
                    parm['val_2'] = np.array(self._preprocess(parm['val_2'], type=self.preprocess)).flatten().tolist()

            if(parm['type'] in ['vector','train']) :
                return_val = self._predict_word2vec(parm, return_val, model)
            elif(parm['type'] in ['sim']) :
                return_val = self._predict_sim(parm, return_val, model)
            elif(parm['type'] in ['similarity']) :
                return_val.append(model.similarity(parm['val_1'][0], parm['val_2'][0]))
            elif(parm['type'] in ['dict'] or parm['type'] in ['vocab2index']) :
                return_val = self._predict_vocab2index(parm, return_val, model)
            elif(parm['type'] in ['index2vocab']):
                return_val = self._predict_index2vocab(parm, return_val, model)
            elif(parm['type'] in ['povb2vocab']) :
                return_val = self._predict_prob2vocab(parm, return_val, model)
            elif(parm['type'] in ['vec2word']):
                return_val = self._predict_vector2word(parm, return_val, model)
            elif (parm['type'] in ['vocablen']):
                return len(model.wv.vocab) - 1
            elif (parm['type'] in ['model']):
                return model
            else :
                raise Exception ("Not available type : {0}".format(parm['type']))
            return return_val
        except Exception as e :
            raise Exception (e)

    def _predict_word2vec(self, parm, return_val, model):
        """
        get word and return with embeded vector
        :param parm:
        :param return_val:
        :param model:
        :return:
        """
        for key in parm['val_1']:
            if key in ['#']:
                return_val.append([0.0005] * self.vector_size)
            elif key in ['@']:
                return_val.append([0.0009] * self.vector_size)
            elif key in model:
                return_val.append(model[key].tolist())
            else:
                return_val.append([0.0002] * self.vector_size)
        return return_val

    def _predict_sim(self, parm, return_val, model):
        """
        return most similar vocabs (close to each other)
        :param parm:
        :param return_val:
        :param model:
        :return:
        """
        try :
            return_val.append(model.most_similar(positive=parm['val_1'], negative=parm['val_2'], topn=5))
            return return_val
        except Exception as e :
            return return_val.append(e)


    def _predict_vocab2index(self, parm, return_val, model):
        """
        find vocab index num
        :param parm:
        :param return_val:
        :param model:
        :return:
        """
        for key in parm['val_1']:
            if key in ['#']:  # padding
                return_val.append(len(model.wv.index2word))
            elif key in ['@']:  # starting
                return_val.append(len(model.wv.index2word) + 1)
            elif key in model:  # word on vocab
                return_val.append(model.wv.vocab[key].index)
            else:  # unknown
                return_val.append(len(model.wv.index2word) + 2)
        return return_val

    def _predict_index2vocab(self, parm, return_val, model):
        """
        convert index number to word
        :param parm:
        :param return_val:
        :param model:
        :return:
        """
        for key in parm['val_1']:
            if len(model.wv.index2word) > key:
                return_val.append(model.wv.index2word[key])
        return return_val

    def _predict_prob2vocab(self, parm, return_val, model):
        """
        prob matrix to max arg matched vocab
        :param parm:
        :param return_val:
        :param model:
        :return:
        """
        for key in parm['val_1']:
            # set ignore char set
            filter_list = []
            for filter_set in filter_list:
                if filter_set in model:
                    key[model.wv.vocab[filter_set].index] = 0.0

            # set ignore char set with index
            filter_index = []
            for idx in filter_index:
                key[idx] = 0.0
            if 'prob_idx' in parm :
                sorted_list = sorted(key, reverse=True)
                index = key.index(sorted_list[parm.get['prob_idx']])
            else :
                index = key.argmax(axis=0)

            if len(model.wv.index2word) > index:
                return_val.append(model.wv.index2word[index])
            elif len(model.wv.index2word) == index:
                return_val.append("PAD")
            elif len(model.wv.index2word) + 1 == index:
                return_val.append("START")
            elif len(model.wv.index2word) + 2 == index:
                return_val.append("UNKNOWN")
        return return_val

    def _predict_vector2word(self, parm, return_val, model):
        """
        embeded vector to most sim word
        :param parm:
        :param return_val:
        :param model:
        :return:
        """
        for key in parm['val_1']:
            for guess in model.similar_by_vector(key):
                if guess[0] not in ['\n', '#', './SF'] and guess[1] > 0:
                    return_val = return_val + [guess[0]]
                    break
        return return_val

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

    def eval(self, node_id, conf, data=None, result=None):
        """

        :param node_id:
        :param parm:
        :return:
        """
        result.set_result_data_format({})
        return result