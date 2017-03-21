from cluster.neuralnet.neuralnet_node import NeuralNetNode
from master.workflow.netconf.workflow_netconf_seq2seq import WorkFlowNetConfSeq2Seq as WfNetconfSeq2Seq
from master.workflow.netconf.workflow_netconf_w2v import WorkFlowNetConfW2V
import numpy as np
import tensorflow as tf
from cluster.service.service_predict_w2v import PredictNetW2V
import numpy as np
import tensorflow as tf
import collections
import argparse
import time
import os


class NeuralNetNodeSeq2Seq(NeuralNetNode):
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
            encode_data, decode_data = dyna_cls.load_train_data(data_node_name, parm='all')

            # prepare net conf
            self._set_net_model()

            for encode, decode  in zip(encode_data, decode_data):
                encode_raw = encode['rawdata']
                decode_raw = decode['rawdata']
                for i in range(0, encode_raw.len(), self.batch_size):
                    encode_batch = self._word_embed_data(encode_raw[i:i + self.batch_size])
                    decode_batch = self._get_dict_id(decode_raw[i:i + self.batch_size])
                    self._run_train(encode_batch, decode_batch)

        except Exception as e :
            raise Exception (e)

    def _init_node_parm(self, node_id):
        """
        init necessary parameters
        :param node_id:
        :return:
        """
        try :
            wf_conf = WfNetconfSeq2Seq(node_id)
            self.md_store_path = wf_conf.get_model_store_path()
            self.cell_type = wf_conf.get_cell_type()
            self.decoder_num_layers = wf_conf.get_decoder_depth()
            self.decoder_seq_length = wf_conf.get_decoder_len()
            self.drop_out = wf_conf.get_drop_out()
            self.encoder_num_layers = wf_conf.get_encoder_depth()
            self.encoder_seq_length = wf_conf.get_encoder_len()
            self.word_embed_type = wf_conf.get_word_embed_type()
            self.word_embed_id = wf_conf.get_word_embed_id()
            self.cell_size = wf_conf.get_cell_size()

            if(self.word_embed_type == 'w2v') :
                #w2v_conf = WorkFlowNetConfW2V(self.word_embed_id)
                #self.vocab_size = w2v_conf.get_vector_size()
                self.vocab_size = 100

            self.grad_clip = 5.
            self.learning_rate = 0.01
            self.decay_rate = 0.01
            self.num_epochs = 10
            self.batch_size = 1
            self.num_batches = 1

        except Exception as e :
            raise Exception (e)

    def _set_progress_state(self):
        return None

    def predict(self, node_id, parm = {}):
        pass

    def eval(self, node_id, parm={}):
        """

        :param node_id:
        :param parm:
        :return:
        """
        pass

    def _word_embed_data(self, input_data):
        """
        change word to vector
        :param input_data:
        :return:
        """
        if(self.word_embed_type == 'w2v'):
            return_arr = []
            for data in input_data :
                parm =  {"type" : "train", "val_1" : {}, "val_2" : []}
                parm['val_1'] = data
                return_arr.append(PredictNetW2V().run(self.word_embed_id, parm))
            return return_arr
        else :
            raise Exception ("[Error] seq2seq train - word embeding : not defined type {0}".format(self.word_embed_type))

    def _get_dict_id(self, input_data):
        """
        change word to vector
        :param input_data:
        :return:
        """
        if(self.word_embed_type == 'w2v'):
            return_arr = []
            for data in input_data :
                parm =  {"type" : "dict", "val_1" : {}, "val_2" : []}
                parm['val_1'] = data
                return_arr.append(PredictNetW2V().run(self.word_embed_id, parm))
            return return_arr
        else :
            raise Exception ("[Error] seq2seq train - word embeding : not defined type {0}".format(self.word_embed_type))

    def _set_net_model(self):
        """
        set tensorflow seq2seq model for train and predict
        :return:
        """
        try :
            # Construct RNN model
            unitcell = tf.contrib.rnn.BasicLSTMCell(self.cell_size)
            cell = tf.contrib.rnn.MultiRNNCell([unitcell] * self.encoder_num_layers)
            self.input_data = tf.placeholder(tf.float32, [self.batch_size, self.encoder_seq_length, self.vocab_size])
            self.targets = tf.placeholder(tf.int32, [self.batch_size, self.encoder_seq_length])
            self.istate = cell.zero_state(self.batch_size, tf.float32)

            # Weigths
            with tf.variable_scope('rnnlm'):
                softmax_w = tf.get_variable("softmax_w", [self.cell_size, self.vocab_size])
                softmax_b = tf.get_variable("softmax_b", [self.vocab_size])
                inputs = tf.split(self.input_data, self.encoder_seq_length, 1)
                inputs = [tf.squeeze(_input, [1]) for _input in inputs]

            self.outputs, last_state = tf.contrib.legacy_seq2seq.rnn_decoder(inputs, self.istate, cell
                                                                        , loop_function=None, scope='rnnlm')

            self.output = tf.reshape(tf.concat(self.outputs, 1), [-1, self.cell_size])
            self.logits = tf.nn.xw_plus_b(self.output, softmax_w, softmax_b)
            self.probs = tf.nn.softmax(self.logits)

            # Loss
            self.loss = tf.contrib.legacy_seq2seq.sequence_loss_by_example([self.logits],  # Input
                                                                      [tf.reshape(self.targets, [-1])],  # Target
                                                                      [tf.ones([self.batch_size * self.encoder_seq_length])],  # Weight
                                                                      self.vocab_size)
            # Optimizer
            self.cost = tf.reduce_sum(self.loss) / self.batch_size / self.encoder_seq_length
            self.final_state = last_state

            self.lr = tf.Variable(0.0, trainable=False)
            self.tvars = tf.trainable_variables()
            self.grads, _ = tf.clip_by_global_norm(tf.gradients(self.cost, self.tvars), self.grad_clip)
            _optm = tf.train.AdamOptimizer(self.lr)
            self.optm = _optm.apply_gradients(zip(self.grads, self.tvars))
        except Exception as e :
            raise Exception (e)


    def _run_train(self, xbatch, ybatch):
        """

        :return:
        """
        try :
            sess = tf.Session()
            sess.run(tf.initialize_all_variables())
            saver = tf.train.Saver(tf.all_variables())
            if(os.path.exists(self.md_store_path) == True):
                saver.restore(sess, self.md_store_path)
            for epoch in range(self.num_epochs):
                # Learning rate scheduling
                sess.run(tf.assign(self.lr, self.learning_rate * (self.decay_rate ** epoch)))
                state = sess.run(self.istate)
                train_loss, state, _ = sess.run([self.cost, self.final_state, self.optm]
                                                , feed_dict={self.input_data: xbatch,
                                                             self.targets: ybatch,
                                                             self.istate: state})
                print("[{0}] train_loss : {1}".format(epoch, train_loss))
            saver.save(sess, self.md_store_path)
            sess.close()
        except Exception as e :
            raise Exception(e)