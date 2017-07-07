from cluster.neuralnet.neuralnet_node import NeuralNetNode
from master.workflow.netconf.workflow_netconf_autoencoder import WorkFlowNetConfAutoEncoder as WFNetConfAuto
import tensorflow as tf
import numpy as np
from scipy import spatial
from common.utils import *
from konlpy.tag import Mecab
from common.graph.nn_graph_manager import NeuralNetModel
import logging

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
            with  tf.Session() as sess :
                sess.run(init)

                saver = tf.train.Saver(tf.all_variables())

                # load trained model
                if (self.check_batch_exist(conf_data['node_id'])):
                    path = ''.join([self.md_store_path, '/', self.get_eval_batch(node_id), '/'])
                    set_filepaths(path)
                    saver.restore(sess, path)

                # feed data and train
                for _ in range(self.iter_size) :
                    while (train_data_set.has_next()):
                        for i in range(0, train_data_set.data_size(), self.batch_size):
                            data_set = train_data_set[i:i + self.batch_size]
                            if(len(data_set) >= self.batch_size) :
                                self._run_train(sess, data_set)
                        train_data_set.next()
                    train_data_set.reset_pointer()

                # save model and close session
                path = ''.join([self.md_store_path, '/', self.make_batch(node_id)[1], '/'])
                set_filepaths(path)
                saver.save(sess, path)
            return node_id
        except Exception as e:
            logging.info("[Stacked AutoEncoder Train Process] : {0}".format(e))
            raise Exception(e)
        finally :
            # copy data feeder's parm to netconf
            self._copy_node_parms(train_data_set, self)

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
            self.init_val = tf.initialize_all_variables()
            self.saver = tf.train.Saver(tf.all_variables())
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
            self.init_val = tf.initialize_all_variables()
            self.saver = tf.train.Saver(tf.all_variables())
        except Exception as e :
            raise Exception ("error on build autoencoder train graph")

    def _run_train(self, sess, data_set):
        """

        :return:
        """
        try :
            _, cost_val = sess.run([self.optimizer, self.cost], feed_dict={self.x: data_set})
            logging.info('Avg. cost = {0}'.format(cost_val / self.n_input))
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
            self.pre_type = wf_conf.get_feeder_pre_type()
            self.n_hidden = wf_conf.get_n_hidden()

            if (wf_conf.get_n_input()):
                self.n_input = wf_conf.get_n_input()
            else :
                raise Exception ("input number is required! ")

            if(self.pre_type in ['frame']) :
                if (self.embed_type == 'onehot'):
                    self.encode_onehot = {}
                    self.word_vector_size = wf_conf.get_vocab_size() + 4
                    self.encode_col = wf_conf.get_encode_column()
                    self.encode_dtype = wf_conf.get_encode_dtype()
                    if (wf_conf.get_vocab_list()):
                        encoder_value_list = wf_conf.get_vocab_list()
                        for col_name in list(encoder_value_list.keys()):
                            self.encode_onehot[col_name] = OneHotEncoder(self.word_vector_size)
                            self.encode_onehot[col_name].restore(encoder_value_list.get(col_name))
            elif(self.pre_type in ['mecab', 'twitter', 'kkma']):
                if(self.embed_type == 'onehot') :
                    self.word_len = wf_conf.get_encode_len()
                    self.word_vector_size = wf_conf.get_vocab_size() + 4
                    self.onehot_encoder = OneHotEncoder(self.word_vector_size)
                    if (wf_conf.get_vocab_list()):
                        self.onehot_encoder.restore(wf_conf.get_vocab_list())
        except Exception as e :
            raise Exception (e)

    def predict(self, node_id, parm = {"input_data" : {}, "type": "encoder"}, internal=False, raw_flag=False):
        """

        :param node_id:
        :param parm:
        :return:
        """
        try :
            # get unique key
            unique_key = '_'.join([node_id , self.get_eval_batch(node_id)])

            # set init params
            self._init_node_parm(node_id)
            ## create tensorflow graph
            if (NeuralNetModel.dict.get(unique_key)):
                self = NeuralNetModel.dict.get(unique_key)
                graph = NeuralNetModel.graph.get(unique_key)
            else:
                self._set_predict_model()
                NeuralNetModel.dict[unique_key] = self
                NeuralNetModel.graph[unique_key] = tf.get_default_graph()
                graph = tf.get_default_graph()

            # off onehot to add dict on predict time
            if (raw_flag) :
                input_arr = parm['input_data']
            elif (self.pre_type in ['frame']):
                input_arr = []
                if (self.embed_type == 'onehot'):
                    for col_name  in self.encode_col :
                        if(self.encode_dtype[col_name] != 'object') :
                            input_arr = input_arr + [int(parm['input_data'].get(col_name))]
                        elif(col_name in list(parm['input_data'].keys())) :
                            input_arr = input_arr + self.encode_onehot[col_name].get_vector(parm['input_data'].get(col_name)).tolist()
                        else :
                            input_arr = input_arr + self.encode_onehot[col_name].get_vector('').tolist()
                input_arr = [input_arr]
            elif (self.pre_type in ['mecab', 'twitter', 'kkma']):
                if (self.embed_type == 'onehot'):
                    self.onehot_encoder.off_edit_mode()
                    input_arr = [self._pos_tag_predict_data(parm['input_data'], self.word_len)]
                    input_arr = self._word_embed_data(self.embed_type, np.array(input_arr))
                else :
                    raise Exception ("AutoEncoder : Unknown embed type error ")

            with tf.Session(graph=graph) as sess :
                sess.run(self.init_val)
                # load trained model
                if (self.check_batch_exist(self.node_id)):
                    path = ''.join([self.md_store_path, '/', self.get_eval_batch(node_id), '/'])
                    set_filepaths(path)
                    self.saver.restore(sess, path)
                else:
                    raise Exception("Autoencoder error : no pretrained model exist")

                # decide which layer to return
                if (parm['type'] == 'encoder'):
                    result = sess.run(self.comp_vec, feed_dict={self.x: input_arr})
                if (parm['type'] == 'decoder'):
                    result = sess.run(self.recov_vec, feed_dict={self.x: input_arr})

                # for eval purpose return original data together
                if (internal) :
                    return result.tolist(), input_arr
                else :
                    return result.tolist()
        except Exception as e :
            raise Exception (e)
        finally :
            sess.close()

    def anomaly_detection(self, node_id, parm = {"input_data" : {}, "type": "encoder"}, raw_flag=False):
        """
        this is a function that judge requested data is out lier of not
        :param node_id: string
        :param parm: dict (include input data)
        :return: boolean
        """
        try :
            parm['type'] = 'decoder'
            out_data, in_data = self.predict(node_id, parm,  internal=True, raw_flag=raw_flag)
            dist = 1 - spatial.distance.cosine(in_data[0], out_data[0])
            return dist
        except Exception as e :
            raise Exception ("error on anomaly detection : {0}".format(e))

    def _set_progress_state(self):
        return None

    def eval(self, node_id, conf_data, data=None, result=None, stand=0.1):
        """
        eval process check if model works well (accuracy with cross table)
        :param node_id:
        :param conf_data:
        :param data:
        :param result:
        :return:
        """
        try :
            node_id = self.get_node_name()
            result.set_result_data_format(None)
            result.set_nn_batch_ver_id(self.get_eval_batch(node_id))

            # prepare net conf
            tf.reset_default_graph()
            while (data.has_next()):
                for i in range(0, data.data_size(), 1):
                    data_set = data[i:i + 1]
                    parm = {"input_data": data_set, "type": "decoder"}
                    dist = self.anomaly_detection(node_id, parm, raw_flag=True)
                    result.set_result_info([str(stand)], [str(dist)])
                data.next()
            return result
        except Exception as e :
            raise Exception ("error on eval wcnn : {0}".format(e))