from cluster.neuralnet.neuralnet_node import NeuralNetNode
from gensim.models import word2vec

class NeuralNetNodeWord2Vec(NeuralNetNode):
    """

    """

    def run(self, conf_data):
        self._init_node_parm(conf_data['node_id'])
        data_node_name = self.find_prev_node(conf_data['node_id'], conf_data['node_list'])
        cls_path, cls_name = self.get_cluster_exec_class(data_node_name)
        dyna_cls = self.load_class(cls_path, cls_name)
        input_data = dyna_cls.load_train_data(data_node_name, parm = 'all')

        #sentences = word2vec.Text8Corpus("wiki_seg.txt")
        #model = word2vec.Word2Vec(input_data, size=250)
        #model.save_word2vec_format(u"med250.model.bin", binary=True)
        return None

    def _init_node_parm(self, node_id):
        return None

    def _set_progress_state(self):
        return None