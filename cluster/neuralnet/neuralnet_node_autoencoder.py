from cluster.neuralnet.neuralnet_node import NeuralNetNode
from master.workflow.netconf.workflow_netconf_autoencoder import WorkFlowNetConfAutoEncoder as WFNetConfAuto
import tensorflow as tf
import numpy as np
from common.utils import *
from konlpy.tag import Mecab

class NeuralNetNodeAutoEncoder(NeuralNetNode):
    """
    this is a network class for Autoencoder
    Autoencoder provide two types of service
    1. provide matrix size of input matrix
    2. provide compressed matrix
    """

    def run(self, conf_data):
        try:

            node_id = conf_data['node_id']
            # get prev node for load data
            train_data_set = self.get_linked_prev_node_with_grp('preprocess')[0]

            # copy data feeder's parm to netconf
            self._copy_node_parms(train_data_set, self)

            # init parms
            self._init_node_parm(conf_data['node_id'])

            # set autoencoder graph
            self._set_train_model()

            # create tensorflow session
            init = tf.global_variables_initializer()
            sess = tf.Session()
            sess.run(init)
            saver = tf.train.Saver(tf.all_variables())

            # load trained model
            if (self.check_batch_exist(conf_data['node_id'])):
                path = ''.join([self.md_store_path, '/', self.get_eval_batch(node_id), '/'])
                set_filepaths(path)
                saver.restore(sess, path)

            # feed data and train
            while (train_data_set.has_next()):
                for i in range(0, train_data_set.data_size(), self.batch_size):
                    data_set = train_data_set[i:i + self.batch_size]
                    if(len(data_set) >= self.batch_size) :
                        self._run_train(sess, data_set)
                train_data_set.next()

            # save model and close session
            path = ''.join([self.md_store_path, '/', self.make_batch(node_id)[1], '/'])
            set_filepaths(path)
            saver.save(sess, path)
            sess.close()
            return node_id
        except Exception as e:
            raise Exception(e)

    def _set_train_model(self):
        """
        set train model for autoencoder
        :return:
        """
        try :
            self.x = tf.placeholder(tf.float32, shape=[self.batch_size, self.n_input], name='x')
            self.y = self.x
            W_encode = {}
            b_encode = {}
            W_decode = {}
            b_decode = {}
            encoder = {}
            decoder = {}

            self.n_hidden = [self.n_input] + self.n_hidden
            encoder_input = self.x
            for cnt in range(len(self.n_hidden)) :
                if(len(self.n_hidden) > cnt+1) :
                    W_encode[cnt] = tf.Variable(tf.random_normal([self.n_hidden[cnt], self.n_hidden[cnt+1]]))
                    b_encode[cnt] = tf.Variable(tf.random_normal([self.n_hidden[cnt+1]]))
                    encoder[cnt] = tf.nn.sigmoid(tf.add(tf.matmul(encoder_input, W_encode[cnt]), b_encode[cnt]))
                    encoder_input = encoder[cnt]
                    decoder_input = encoder[cnt]

            for cnt in reversed(range(len(self.n_hidden))):
                if (cnt - 1 >= 0):
                    W_decode[cnt] = tf.Variable(tf.random_normal([self.n_hidden[cnt], self.n_hidden[cnt-1]]))
                    b_decode[cnt] = tf.Variable(tf.random_normal([self.n_hidden[cnt-1]]))
                    decoder[cnt] = tf.nn.sigmoid(tf.add(tf.matmul(decoder_input, W_decode[cnt]), b_decode[cnt]))
                    decoder_input = decoder[cnt]

            self.cost = tf.reduce_mean(tf.pow(self.y - decoder[1], 2))
            self.optimizer = tf.train.RMSPropOptimizer(self.learning_rate).minimize(self.cost)
        except Exception as e :
            raise Exception ("error on build autoencoder train graph")

    def _set_predict_model(self):
        """
        set train model for autoencoder
        :return:
        """
        try :
            self.x = tf.placeholder(tf.float32, shape=[1, self.n_input], name='x')
            self.y = self.x
            W_encode = {}
            b_encode = {}
            W_decode = {}
            b_decode = {}
            encoder = {}
            decoder = {}

            self.n_hidden = [self.n_input] + self.n_hidden
            encoder_input = self.x
            for cnt in range(len(self.n_hidden)) :
                if(len(self.n_hidden) > cnt+1) :
                    W_encode[cnt] = tf.Variable(tf.random_normal([self.n_hidden[cnt], self.n_hidden[cnt+1]]))
                    b_encode[cnt] = tf.Variable(tf.random_normal([self.n_hidden[cnt+1]]))
                    encoder[cnt] = tf.nn.sigmoid(tf.add(tf.matmul(encoder_input, W_encode[cnt]), b_encode[cnt]))
                    encoder_input = encoder[cnt]
                    decoder_input = encoder[cnt]

            for cnt in reversed(range(len(self.n_hidden))):
                if (cnt - 1 >= 0):
                    W_decode[cnt] = tf.Variable(tf.random_normal([self.n_hidden[cnt], self.n_hidden[cnt-1]]))
                    b_decode[cnt] = tf.Variable(tf.random_normal([self.n_hidden[cnt-1]]))
                    decoder[cnt] = tf.nn.sigmoid(tf.add(tf.matmul(decoder_input, W_decode[cnt]), b_decode[cnt]))
                    decoder_input = decoder[cnt]

            self.comp_vec = encoder[len(self.n_hidden)-2]
            self.recov_vec = decoder[1]

        except Exception as e :
            raise Exception ("error on build autoencoder train graph")

    def _run_train(self, sess, data_set):
        """

        :return:
        """
        try :
            for epoch in range(self.iter_size):
                total_cost = 0
                _, cost_val = sess.run([self.optimizer, self.cost], feed_dict={self.x: data_set})
                total_cost += cost_val
                print('Epoch:', '%04d' % (epoch + 1), 'Avg. cost =', '{:.6f}'.format(total_cost / self.n_input))
        except Exception as e :
            raise Exception ('autoencoder run_train step error : {0}'.foramt(e) )

    def _get_node_parm(self, node_id):
        """
        return conf master class
        :return:
        """
        return WFNetConfAuto(node_id)

    def _init_node_parm(self, node_id):
        """
        initialze parms for autoencoder
        :param node_id:
        :return:
        """
        try:
            wf_conf = WFNetConfAuto(node_id)
            self.node_id = node_id
            self.md_store_path = wf_conf.get_model_store_path()
            self.iter_size = wf_conf.get_iter_size()
            self.batch_size = wf_conf.get_batch_size()
            self.learning_rate = wf_conf.get_learn_rate()
            self.embed_type = wf_conf.get_embed_type()
            if(self.embed_type == 'onehot') :
                self.word_len = wf_conf.get_encode_len()
                self.word_vector_size = wf_conf.get_vocab_size() + 4
                self.n_input = int(self.word_len) * (self.word_vector_size)
            self.onehot_encoder = OneHotEncoder(self.word_vector_size)
            if (wf_conf.get_vocab_list()):
                self.onehot_encoder.restore(wf_conf.get_vocab_list())

            self.n_hidden = wf_conf.get_n_hidden()
            if(wf_conf.get_n_input()) :
                self.n_input = wf_conf.get_n_input()

        except Exception as e :
            raise Exception (e)

    def predict(self, node_id, parm = {"input_data" : {}, "type": "encoder"}):
        """

        :param node_id:
        :param parm:
        :return:
        """
        try :
            # set init params
            self._init_node_parm(node_id)
            self._set_predict_model()

            # off onehot to add dict on predict time
            if (self.embed_type == 'onehot'):
                self.onehot_encoder.off_edit_mode()
                input_arr = [self._pos_tag_predict_data(parm['input_data'], self.word_len)]
            else :
                raise Exception ("AutoEncoder : Unknown embed type error ")

            # create tensorflow session
            init = tf.global_variables_initializer()
            sess = tf.Session()
            sess.run(init)
            saver = tf.train.Saver(tf.all_variables())

            # load trained model
            if (self.check_batch_exist(self.node_id)):
                path = ''.join([self.md_store_path, '/', self.get_eval_batch(self.node_id), '/'])
                set_filepaths(path)
                saver.restore(sess, path)
            else:
                raise Exception("Autoencoder error : no pretrained model exist")

            if (parm['type'] == 'encoder'):
                result = sess.run(self.comp_vec, feed_dict={self.x: self._word_embed_data(self.embed_type,
                                                                                          np.array(input_arr))})
            if (parm['type'] == 'decoder'):
                result = sess.run(self.recov_vec, feed_dict={self.x: self._word_embed_data(self.embed_type,
                                                                                           np.array(input_arr))})
            return result.tolist()
        except Exception as e :
            raise Exception (e)
        finally :
            sess.close()

    def _set_progress_state(self):
        return None

    def eval(self, node_id, parm={}):
        """

        :param node_id:
        :param parm:
        :return:
        """
        pass