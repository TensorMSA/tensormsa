from cluster.neuralnet.neuralnet_node import NeuralNetNode
from gensim.models import word2vec
from master.workflow.netconf.workflow_netconf_w2v import WorkFlowNetConfW2V
import os, json
from konlpy.tag import Mecab

class NeuralNetNodeWord2Vec(NeuralNetNode):
    """

    """

    def run(self, conf_data):
        try :
            # init parms for word2vec node
            self._init_node_parm(conf_data['node_id'])

            # get prev node for load data
            data_node_name = self.find_prev_node(conf_data['node_id'], conf_data['node_list'])
            cls_path, cls_name = self.get_cluster_exec_class(data_node_name)
            dyna_cls = self.load_class(cls_path, cls_name)
            input_data = dyna_cls.load_train_data(data_node_name, parm = 'all')

            # train
            #model = word2vec.Word2Vec(input_data, size=100, window=5, min_count=5, workers=4)
            model = word2vec.Word2Vec()
            if (os.path.exists(''.join([self.md_store_path, '/model.bin'])) == True):
                model = word2vec.Word2Vec.load(''.join([self.md_store_path, '/model.bin']))
            model.build_vocab(input_data)
            model.train(input_data)
            os.makedirs(self.md_store_path, exist_ok=True)
            model.save(''.join([self.md_store_path, '/model.bin']))

            return len(model.raw_vocab)
        except Exception as e:
            raise Exception(e)

    def _init_node_parm(self, node_id):
        wf_conf = WorkFlowNetConfW2V(node_id)
        self.md_store_path = wf_conf.get_model_store_path()


    def _set_progress_state(self):
        return None

    def predict(self, node_id, parm = {"type" : "vector", "val_1" : [], "val_2" : []}):
        """
        predict service method
        1. type (vector) : return vector
        2. type (sim) : positive list & negative list
        :param node_id:
        :param parm:
        :return:
        """

        try :
            self._init_node_parm(node_id)
            return_val = []
            if (os.path.exists(''.join([self.md_store_path, '/model.bin'])) == False):
                raise Exception ("No pretrained model exist")

            if('val_1' in parm):
                parm['val_1'] = self._pos_raw_data(parm['val_1'])
            if ('val_2' in parm):
                parm['val_2'] = self._pos_raw_data(parm['val_2'])

            model = word2vec.Word2Vec.load(''.join([self.md_store_path, '/model.bin']))
            if(parm['type'] == 'vector') :
                for key in parm['val_1'] :
                    return_val.append(model[key])
            elif(parm['type'] == 'sim') :
                return_val.append(model.most_similar(positive=parm['val_1'], negative=parm['val_2'] , topn=1))
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