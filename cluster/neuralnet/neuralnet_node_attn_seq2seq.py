from cluster.neuralnet.neuralnet_node import NeuralNetNode
from master.workflow.netconf.workflow_netconf_seq2seq import WorkFlowNetConfSeq2Seq as WfNetconfSeq2Seq
from cluster.service.service_predict_w2v import PredictNetW2V
import numpy as np
import tensorflow as tf
from common.utils import *
from konlpy.tag import Mecab
from common.graph.nn_graph_manager import NeuralNetModel
import tensorflow as tf
import tensorflow.contrib.seq2seq as seq2seq
from tensorflow.contrib.rnn import LSTMCell, LSTMStateTuple, GRUCell, MultiRNNCell
from tensorflow.contrib.rnn.python.ops.rnn_cell import _linear
from tensorflow.python.ops.rnn_cell_impl import _zero_state_tensors
from tensorflow.python.layers.core import Dense

class NeuralNetNodeAttnSeq2Seq(NeuralNetNode):
    """

    """

    def run(self, conf_data):
        try :
            # init parms for word2vec node
            node_id = conf_data['node_id']
            self._init_node_parm(node_id)

            # get prev node for load data
            train_data_set = self.get_linked_prev_node_with_grp('preprocess')[0]

            # prepare net conf
            tf.reset_default_graph()
            self._set_train_model()

            # create session
            with tf.Session() as sess:
                sess.run(tf.initialize_all_variables())
                saver = tf.train.Saver(tf.all_variables())
                if (self.check_batch_exist(conf_data['node_id'])):
                    path = ''.join([self.md_store_path, '/', self.get_eval_batch(node_id), '/'])
                    set_filepaths(path)
                    saver.restore(sess, path)

                for self.epoch in range(self.num_epochs):
                    # run train
                    while(train_data_set.has_next()) :
                        for i in range(0, train_data_set.data_size(), self.batch_size):
                            data_set = train_data_set[i:i + self.batch_size]
                            if(len(data_set[0]) != self.batch_size) : break
                            targets = self._get_dict_id(data_set[1])
                            decode_batch = self._word_embed_data(data_set[1])
                            encode_batch = self._word_embed_data(data_set[0])
                            self._run_train(sess, encode_batch, decode_batch, targets)
                        train_data_set.next()
                    train_data_set.reset_pointer()

                # save model and close session
                path = ''.join([self.md_store_path, '/', self.make_batch(node_id)[1], '/'])
                set_filepaths(path)
                saver.save(sess, path)
        except Exception as e :
            raise Exception (e)
        finally :
            if (self.word_embed_type == 'onehot'):
                self.wf_conf.set_vocab_list(self.onehot_encoder.dics())

    def _init_node_parm(self, node_id):
        """
        init necessary parameters
        :param node_id:
        :return:
        """
        try :
            try :
                self.wf_conf = WfNetconfSeq2Seq(node_id)
                wf_conf = self.wf_conf
                self.bidirectional = wf_conf.bidirectional
                self.attention = wf_conf.attention
                self.input_vocab_size = wf_conf.input_vocab_size
                self.target_vocab_size = wf_conf.target_vocab_size
                self.enc_hidden_size = wf_conf.enc_hidden_size
                self.enc_num_layers = wf_conf.enc_num_layers
                self.dec_hidden_size = wf_conf.dec_hidden_size
                self.dec_num_layers = wf_conf.dec_num_layers
                self.batch_size = wf_conf.batch_size
                self.learning_rate = tf.Variable(float(wf_conf.learning_rate), trainable=False)
                self.learning_rate_decay_op = self.learning_rate.assign(
                    self.learning_rate * wf_conf.learning_rate_decay_factor)
                self.global_step = tf.Variable(0, trainable=False)
                self.max_gradient_norm = wf_conf.max_gradient_norm
                self.buckets = wf_conf.buckets
            except Exception as e :
                raise Exception ("seq2seq netconf parms not set")

        except Exception as e :
            raise Exception (e)

    def _set_progress_state(self):
        return None

    def predict(self, node_id, parm = {"input_data" : {}, "num" : 0, "clean_ans": True}):
        """

        :param node_id:
        :param parm:
        :return:
        """
        try :
            # get unique key
            unique_key = '_'.join([node_id, self.get_eval_batch(node_id)])

            # set init params
            self.node_id = node_id
            self._init_node_parm(self.node_id)

            # prepare net conf
            tf.reset_default_graph()

            ## create tensorflow graph
            if (NeuralNetModel.dict.get(unique_key)):
                self = NeuralNetModel.dict.get(unique_key)
                graph = NeuralNetModel.graph.get(unique_key)
            else:
                self._set_predict_model()
                NeuralNetModel.dict[unique_key] = self
                NeuralNetModel.graph[unique_key] = tf.get_default_graph()
                graph = tf.get_default_graph()

            with tf.Session(graph=graph) as sess :
                sess.run(self.init_val)
                result = self._run_predict(sess, parm['input_data'],
                                           predict_num=parm.get("num") if parm.get("num") != None else 0,
                                           clean_ans = parm.get("clean_ans") if parm.get("clean_ans") != None else True,
                                           batch_ver='eval', # TODO : need to be predict version
                                           saver=self.saver)
            return result
        except Exception as e :
            raise Exception ("seq2seq predict error : {0}".format(e))
        finally:
            sess.close()

    def eval(self, node_id, conf, data=None, result=None):
        """
        eval result wit test data
        :param node_id:
        :param parm:
        :return:
        """
        try :
            result.set_result_data_format({})
            tf.reset_default_graph()
            sess = tf.Session()
            sess.run(tf.initialize_all_variables())
            # prepare net conf
            self._set_predict_model()
            self.node_id = node_id

            while (data.has_next()):
                for i in range(0, data.data_size(), self.predict_batch):
                    data_set = data[i:i + self.predict_batch]
                    if (len(data_set[0]) != self.predict_batch): break
                    predict = self._run_predict(sess, data_set[0][0], type='pre', clean_ans=False)
                    result.set_result_info(' '.join(data_set[1][0]), ' '.join(predict[0]), input=' '.join(data_set[0][0]), acc=None)
                data.next()
            return result
        except Exception as e :
            raise Exception("seq2seq eval error : {0}".format(e))
        finally:
            sess.close()

    def _set_train_model(self):
        """
        define train graph
        :return:
        """
        # Create the internal multi-layer cell for our RNN.
        if use_lstm:
            single_cell1 = LSTMCell(self.enc_hidden_size)
            single_cell2 = LSTMCell(self.dec_hidden_size)
        else:
            single_cell1 = GRUCell(self.enc_hidden_size)
            single_cell2 = GRUCell(self.dec_hidden_size)
        enc_cell = MultiRNNCell([single_cell1 for _ in range(self.enc_num_layers)])
        dec_cell = MultiRNNCell([single_cell2 for _ in range(self.dec_num_layers)])

        self.encoder_cell = enc_cell
        self.decoder_cell = dec_cell

        self._make_graph(forward_only)
        self.saver = tf.train.Saver(tf.global_variables())

