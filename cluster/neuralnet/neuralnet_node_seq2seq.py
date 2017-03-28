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
from common.utils import *
import os
from konlpy.tag import Mecab

class NeuralNetNodeSeq2Seq(NeuralNetNode):
    """

    """

    def run(self, conf_data):
        try :
            # init parms for word2vec node
            self._init_node_parm(conf_data['node_id'])
            self.cls_pool = conf_data['cls_pool']

            # get prev node for load data
            data_node_name = self._get_backward_node_with_type(conf_data['node_id'], 'preprocess')
            train_data_set = self.cls_pool[data_node_name[0]]

            # prepare net conf
            self._set_train_model()

            while(train_data_set.has_next()) :
                for i in range(0, train_data_set.len(), self.batch_size):
                    data_set = train_data_set[i:i + self.batch_size]
                    decode_batch = self._get_dict_id(data_set[1])
                    encode_batch = self._word_embed_data(data_set[0])
                    self._run_train(encode_batch, decode_batch)
                train_data_set.next()

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
                self.word_vector_size = 100
            self.vocab_size = self._get_vocab_size()
            self.grad_clip = 5.
            self.learning_rate = wf_conf.get_learn_rate()
            self.decay_rate = wf_conf.get_learn_rate()
            self.num_epochs = wf_conf.get_iter_size()
            self.batch_size = wf_conf.get_batch_size()
            self.num_batches = 1

        except Exception as e :
            raise Exception (e)

    def _set_progress_state(self):
        return None

    def predict(self, node_id, parm = {"input_data" : {}}):
        """

        :param node_id:
        :param parm:
        :return:
        """
        # set init params
        self._init_node_parm(node_id)
        # prepare net conf
        self._set_predict_model()
        # predict network
        return self._run_predict(parm['input_data'])

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

    def _get_vec2word(self, input_data):
        """
        change word to vector
        :param input_data:
        :return:
        """
        if(self.word_embed_type == 'w2v'):
            return_arr = []
            for data in input_data :
                parm =  {"type" : "vec2word", "val_1" : {}, "val_2" : []}
                parm['val_1'] = data
                return_arr.append(PredictNetW2V().run(self.word_embed_id, parm))
            return return_arr
        else :
            raise Exception ("[Error] seq2seq train - word embeding : not defined type {0}".format(self.word_embed_type))

    def _get_vocab_size(self):
        """
        change word to vector
        :param input_data:
        :return:
        """
        if(self.word_embed_type == 'w2v'):
            parm =  {"type" : "vocablen", "val_1" : {}, "val_2" : []}
            return PredictNetW2V().run(self.word_embed_id, parm)
        else :
            raise Exception ("[Error] seq2seq train - word embeding : not defined type {0}".format(self.word_embed_type))

    def _set_train_model(self):
        """
        set tensorflow seq2seq model for train and predict
        :return:
        """
        try :
            # Construct RNN model
            unitcell = tf.contrib.rnn.BasicLSTMCell(self.cell_size)
            cell = tf.contrib.rnn.MultiRNNCell([unitcell] * self.encoder_num_layers)
            self.input_data = tf.placeholder(tf.float32, [self.batch_size, self.encoder_seq_length, self.word_vector_size])
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
            if(len(get_filepaths(self.md_store_path)) > 0):
                saver.restore(sess, ''.join([self.md_store_path , '/']))
            for epoch in range(self.num_epochs):
                # Learning rate scheduling
                sess.run(tf.assign(self.lr, self.learning_rate * (self.decay_rate ** epoch)))
                state = sess.run(self.istate)
                train_loss, state, _ = sess.run([self.cost, self.final_state, self.optm]
                                                , feed_dict={self.input_data: xbatch,
                                                             self.targets: ybatch,
                                                             self.istate: state})
                print("[{0}] train_loss : {1}".format(epoch, train_loss))
            saver.save(sess, ''.join([self.md_store_path , '/']))
            sess.close()
        except Exception as e :
            raise Exception(e)



    def _set_predict_model(self):
        """
        set tensorflow seq2seq model for train and predict
        :return:
        """
        encoder_seq_length = 1
        try :
            # Construct RNN model
            unitcell = tf.contrib.rnn.BasicLSTMCell(self.cell_size)
            self.cell = tf.contrib.rnn.MultiRNNCell([unitcell] * self.encoder_num_layers)
            self.input_data = tf.placeholder(tf.float32, [self.batch_size, encoder_seq_length, self.word_vector_size])
            self.istate = self.cell.zero_state(self.batch_size, tf.float32)

            # Weigths
            with tf.variable_scope('rnnlm'):
                softmax_w = tf.get_variable("softmax_w", [self.cell_size, self.word_vector_size])
                softmax_b = tf.get_variable("softmax_b", [self.word_vector_size])
                inputs = tf.split(self.input_data, encoder_seq_length, 1)
                inputs = [tf.squeeze(_input, [1]) for _input in inputs]

            self.outputs, self.last_state = tf.contrib.legacy_seq2seq.rnn_decoder(inputs, self.istate, self.cell
                                                                        , loop_function=None, scope='rnnlm')

            self.output = tf.reshape(tf.concat(self.outputs, 1), [-1, self.cell_size])
            self.logits = tf.nn.xw_plus_b(self.output, softmax_w, softmax_b)
            self.probs = tf.nn.softmax(self.logits)

        except Exception as e :
            raise Exception (e)

    def _run_predict(self, x_input):
        """

        :return:
        """
        try :
            # create session
            sess = tf.Session()
            sess.run(tf.initialize_all_variables())
            saver = tf.train.Saver(tf.all_variables())

            #restore model
            if (len(get_filepaths(self.md_store_path)) > 0):
                saver.restore(sess, ''.join([self.md_store_path , '/']))
            else :
                raise Exception ("error : no pretrained model exist")

            mecab = Mecab('/usr/local/lib/mecab/dic/mecab-ko-dic')
            state = sess.run(self.cell.zero_state(1,tf.float32))
            last_word = ""
            output = []

            for word_tuple in mecab.pos(x_input):
                word = ''.join([word_tuple[0], "/" , word_tuple[1]])
                state = sess.run(self.last_state, feed_dict={self.input_data: self._word_embed_data(np.array([[word]])), self.istate: state})
                last_word = word

            word = last_word
            for num in range(self.decoder_seq_length):
                [probsval, state] = sess.run([self.probs, self.last_state]
                                             , feed_dict={self.input_data: self._word_embed_data(np.array([[word]])), self.istate: state})

                output = output + self._get_vec2word(np.array([[probsval[0]]]))
            sess.close()
            return output
        except Exception as e :
            raise Exception(e)