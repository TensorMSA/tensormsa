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
            # init parms
            node_id = conf_data['node_id']
            self._init_node_parm(conf_data['node_id'])
            self.cls_pool = conf_data['cls_pool']

            data_node_name = self._get_backward_node_with_type(conf_data['node_id'], 'preprocess')
            train_data_set = self.cls_pool[data_node_name[0]]

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
            return True
        except Exception as e:
            raise Exception(e)
        finally :
            if (self.embed_type == 'onehot'):
                self.wf_conf.set_vocab_list(self.onehot_encoder.dics())

    def _set_train_model(self):
        """
        set train model for autoencoder
        :return:
        """
        self.x = tf.placeholder(tf.float32, shape=[self.batch_size, self.n_input], name='x')
        self.y = self.x
        W_encode = tf.Variable(tf.random_normal([self.n_input, self.n_hidden]))
        b_encode = tf.Variable(tf.random_normal([self.n_hidden]))

        W_decode = tf.Variable(tf.random_normal([self.n_hidden, self.n_input]))
        b_decode = tf.Variable(tf.random_normal([self.n_input]))

        # TODO:need to make activation func able to be changed with parms
        encoder = tf.nn.sigmoid(tf.add(tf.matmul(self.x, W_encode), b_encode))
        decoder = tf.nn.sigmoid(tf.add(tf.matmul(encoder, W_decode), b_decode))

        self.cost = tf.reduce_mean(tf.pow(self.y - decoder, 2))
        self.optimizer = tf.train.RMSPropOptimizer(self.learning_rate).minimize(self.cost)

    def _set_predict_model(self):
        """
        set train model for autoencoder
        :return:
        """
        self.x = tf.placeholder(tf.float32, shape=[1, self.n_input], name='x')
        self.y = self.x
        W_encode = tf.Variable(tf.random_normal([self.n_input, self.n_hidden]))
        b_encode = tf.Variable(tf.random_normal([self.n_hidden]))

        W_decode = tf.Variable(tf.random_normal([self.n_hidden, self.n_input]))
        b_decode = tf.Variable(tf.random_normal([self.n_input]))

        # TODO:need to make activation func able to be changed with parms
        self.encoder = tf.nn.sigmoid(tf.add(tf.matmul(self.x, W_encode), b_encode))
        self.decoder = tf.nn.sigmoid(tf.add(tf.matmul(self.encoder, W_decode), b_decode))

    def _run_train(self, sess, data_set):
        """

        :return:
        """
        try :
            for epoch in range(self.iter_size):
                total_cost = 0
                _, cost_val = sess.run([self.optimizer, self.cost], feed_dict={self.x: self._word_embed_data(data_set)})
                total_cost += cost_val
                print('Epoch:', '%04d' % (epoch + 1), 'Avg. cost =', '{:.6f}'.format(total_cost / self.n_input))
        except Exception as e :
            raise Exception ('autoencoder run_train step error : {0}'.foramt(e) )

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
            self.n_hidden = wf_conf.get_n_hidden()
            self.n_input = wf_conf.get_n_input()
            self.word_len = int(self.n_input/wf_conf.get_vocab_size())
            self.embed_type = wf_conf.get_embed_type()
            self.word_vector_size = wf_conf.get_vocab_size() + 4
            self.onehot_encoder = OneHotEncoder(self.word_vector_size)
            if (wf_conf.get_vocab_list()):
                self.onehot_encoder.restore(wf_conf.get_vocab_list())
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
                raise Exception("error : no pretrained model exist")

            word_list = [self._pos_tag_predict_data(parm['input_data'])]
            if (parm['type'] == 'encoder'):
                result = sess.run(self.encoder, feed_dict={self.x: self._word_embed_data(np.array(word_list))})
            if (parm['type'] == 'decoder'):
                result = sess.run(self.decoder, feed_dict={self.x: self._word_embed_data(np.array(word_list))})
            return result.tolist()
        except Exception as e :
            raise Exception (e)
        finally :
            sess.close()

    def _word_embed_data(self, input_data):
        """
        change word to vector
        :param input_data:
        :return:
        """
        return_arr = []
        if(self.embed_type == 'onehot'):
            for data in input_data:
                row_arr = []
                for row in data :
                    row_arr = row_arr + self.onehot_encoder.get_vector(row).tolist()
                return_arr.append(row_arr)
            return return_arr
        elif(self.embed_type == None) :
            return []
        else :
            raise Exception ("[Error] seq2seq train - word embeding : not defined type {0}".format(self.word_embed_type))

    def _pos_tag_predict_data(self, x_input):
        """

        :param x_input:
        :return:
        """
        word_list = []
        mecab = Mecab('/usr/local/lib/mecab/dic/mecab-ko-dic')
        for word_tuple in self._pad_predict_input(mecab.pos(x_input)):
            if (len(word_tuple[1]) > 0):
                word = ''.join([word_tuple[0], "/", word_tuple[1]])
            else:
                word = word_tuple[0]
            word_list.append(word)
        return word_list

    def _pad_predict_input(self, input_tuple):
        """
        pad chars for prediction
        :param input_tuple:
        :return:
        """
        pad_size = self.word_len - (len(input_tuple) + 1)
        if(pad_size >= 0 ) :
            input_tuple = pad_size * [('#', '')] + input_tuple[0: self.word_len -1] + [('SF', '')]
        else :
            input_tuple = input_tuple[0: self.word_len-1] + [('SF', '')]
        return input_tuple

    def _set_progress_state(self):
        return None

    def eval(self, node_id, parm={}):
        """

        :param node_id:
        :param parm:
        :return:
        """
        pass