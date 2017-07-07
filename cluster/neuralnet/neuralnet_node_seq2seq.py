from cluster.neuralnet.neuralnet_node import NeuralNetNode
from master.workflow.netconf.workflow_netconf_seq2seq import WorkFlowNetConfSeq2Seq as WfNetconfSeq2Seq
from cluster.service.service_predict_w2v import PredictNetW2V
import numpy as np
import tensorflow as tf
import logging
from common.utils import *
from konlpy.tag import Mecab
from common.graph.nn_graph_manager import NeuralNetModel

class NeuralNetNodeSeq2Seq(NeuralNetNode):
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
            logging.info("[BasicSeq2Seq Train Process] : {0}".format(e))
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
                wf_conf = WfNetconfSeq2Seq(node_id)
                self.md_store_path = wf_conf.get_model_store_path()
                self.cell_type = wf_conf.get_cell_type()
                self.decoder_num_layers = wf_conf.get_decoder_depth()
                self.decoder_seq_length = wf_conf.get_decoder_len()
                self.drop_out = wf_conf.get_drop_out()
                self.encoder_num_layers = wf_conf.get_encoder_depth()
                self.encoder_seq_length = wf_conf.get_encoder_len()
                self.word_embed_type = wf_conf.get_word_embed_type()
                self.cell_size = wf_conf.get_cell_size()
                if(self.word_embed_type == 'w2v') :
                    self.word_embed_id = wf_conf.get_word_embed_id()
                    self.word_vector_size = self._get_w2v_vector_size(self.word_embed_id)
                    if (wf_conf.get_vocab_size() != None and wf_conf.get_vocab_size() == self._get_vocab_size()):
                        self.vocab_size = wf_conf.get_vocab_size() + 4
                    else:
                        del_filepaths(self.md_store_path)
                        wf_conf.set_vocab_size(self._get_vocab_size())
                        self.vocab_size = self._get_vocab_size() + 4
                elif (self.word_embed_type == 'onehot'):
                    self.word_vector_size = wf_conf.get_vocab_size() + 4
                    self.vocab_size = wf_conf.get_vocab_size() + 4
                    self.onehot_encoder = OneHotEncoder(self.word_vector_size)
                    if (wf_conf.get_vocab_list()) :
                        self.onehot_encoder.restore(wf_conf.get_vocab_list())
                self.grad_clip = 5.
                self.learning_rate = wf_conf.get_learn_rate()
                self.decay_rate = wf_conf.get_learn_rate()
                self.num_epochs = wf_conf.get_iter_size()
                self.batch_size = wf_conf.get_batch_size()
                self.predict_batch = 1
            except Exception as e :
                raise Exception ("seq2seq netconf parms not set")

        except Exception as e :
            raise Exception (e)

    def _get_w2v_vector_size(self, nn_id):
        """
        get active version word2vec networks config
        :param nn_id:
        :return:
        """
        node_id = self._find_netconf_node_id(nn_id)
        _path, _cls = self.get_cluster_exec_class(node_id)
        cls = self.load_class(_path, _cls)
        cls._init_node_parm(node_id)
        if('vector_size' in cls.__dict__) :
            return cls.vector_size
        return 10

    def _get_linked_prev_node_has_vector(self):
        """
        get linked node prev with condition sent_max_len exists
        :param type:
        :return:
        """
        objs = self.get_linked_prev_node_with_cond('sent_max_len')
        if(len(objs) > 0 ) :
            return objs[0].sent_max_len
        return 100

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

    def _word_embed_data(self, input_data):
        """
        change word to vector
        :param input_data:
        :return:
        """
        return_arr = []
        if(self.word_embed_type == 'w2v'):
            for data in input_data :
                parm =  {"type" : "train", "val_1" : {}, "val_2" : []}
                parm['val_1'] = data
                return_arr.append(PredictNetW2V().run(self.word_embed_id, parm))
            return return_arr
        elif(self.word_embed_type == 'onehot') :
            for data in input_data:
                row_arr = []
                for row in data :
                    row_arr.append(self.onehot_encoder.get_vector(row))
                return_arr.append(row_arr)
            return return_arr
        else :
            raise Exception ("[Error] seq2seq train - word embeding : not defined type {0}".format(self.word_embed_type))

    def _get_dict_id(self, input_data):
        """
        change word to vector
        :param input_data:
        :return:
        """
        return_arr = []
        if(self.word_embed_type == 'w2v') :
            for data in input_data :
                parm =  {"type" : "dict", "val_1" : {}, "val_2" : []}
                parm['val_1'] = data
                return_arr.append(PredictNetW2V().run(self.word_embed_id, parm))
            return return_arr
        elif(self.word_embed_type == 'onehot') :
            for data in input_data:
                row_arr = []
                for row in data:
                    row_arr.append(self.onehot_encoder.get_idx(row))
                return_arr.append(row_arr)
            return return_arr
        else :
            raise Exception ("[Error] seq2seq train - word embeding : not defined type {0}".format(self.word_embed_type))

    def _get_vec2word(self, input_data):
        """
        change word to vector
        :param input_data:
        :return:
        """
        return_arr = []
        if(self.word_embed_type == 'w2v'):
            for data in input_data :
                parm =  {"type" : "vec2word", "val_1" : {}, "val_2" : []}
                parm['val_1'] = data
                return_arr.append(PredictNetW2V().run(self.word_embed_id, parm))
            return return_arr
        else :
            raise Exception ("[Error] seq2seq train - word embeding : not defined type {0}".format(self.word_embed_type))

    def _get_index2vocab(self, input_data, prob_idx = 0):
        """
        change word to vector
        :param input_data:
        :return:
        """
        return_arr = []
        if(self.word_embed_type == 'w2v'):
            for data in input_data :
                parm =  {"type" : "povb2vocab", "val_1" : {}, "val_2" : [], "prob_idx" :  prob_idx}
                parm['val_1'] = data
                return_arr.append(PredictNetW2V().run(self.word_embed_id, parm))
            return return_arr
        elif (self.word_embed_type == 'onehot'):
            for data in input_data:
                row_arr = []
                for row in data:
                    row_arr.append(self.onehot_encoder.get_vocab(row, prob_idx = prob_idx))
                return_arr.append(row_arr)
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

    def _set_weight_vectors(self):
        """
        set weight vecotrs seperatly for sharing weight with preidicts logic
        :return:
        """
        # Weigths
        with tf.variable_scope('rnnlm') as scope:
            self.softmax_w = tf.get_variable("softmax_w", [self.cell_size, self.vocab_size])
            self.softmax_b = tf.get_variable("softmax_b", [self.vocab_size])

    def _set_train_model(self):
        """
        set tensorflow seq2seq model for train and predict
        :return:
        """
        try :
            # Construct RNN model
            cells = []
            for _ in range(self.encoder_num_layers) :
                unitcell = tf.contrib.rnn.BasicLSTMCell(self.cell_size)
                dropcell = tf.contrib.rnn.DropoutWrapper(unitcell,
                                                         input_keep_prob=1.0,
                                                         output_keep_prob=self.drop_out)
                cells.append(dropcell)
            mul_cell = tf.contrib.rnn.MultiRNNCell(cells)
            self.input_data = tf.placeholder(tf.float32, [self.batch_size, self.encoder_seq_length, self.word_vector_size])
            self.output_data = tf.placeholder(tf.float32, [self.batch_size, self.decoder_seq_length, self.word_vector_size])
            self.targets = tf.placeholder(tf.int32, [self.batch_size, self.decoder_seq_length])
            self.istate = mul_cell.zero_state(self.batch_size, tf.float32)

            # set weight vectors
            self._set_weight_vectors()

            # reshape data matirx
            inputs = tf.split(self.input_data, self.encoder_seq_length, 1)
            inputs = [tf.squeeze(_input, [1]) for _input in inputs]
            outputs = tf.split(self.output_data, self.decoder_seq_length, 1)
            outputs = [tf.squeeze(_output, [1]) for _output in outputs]

            self.outputs, last_state = tf.contrib.legacy_seq2seq.basic_rnn_seq2seq(inputs,
                                                                                   outputs,
                                                                                   mul_cell,
                                                                                   dtype=tf.float32,
                                                                                   scope='rnnlm')

            self.output = tf.reshape(tf.concat(self.outputs, 1), [-1, self.cell_size])
            self.logits = tf.nn.xw_plus_b(self.output, self.softmax_w, self.softmax_b)
            self.probs = tf.nn.softmax(self.logits)

            # Loss
            self.loss = tf.contrib.legacy_seq2seq.sequence_loss([self.logits],  # Input
                                                                [tf.reshape(self.targets, [-1])],  # Target
                                                                [tf.ones([self.batch_size * self.decoder_seq_length])],  # Weight
                                                                self.vocab_size)
            # Optimizer
            self.cost = tf.reduce_sum(self.loss) / self.batch_size / self.decoder_seq_length
            self.final_state = last_state

            _opt = tf.train.AdamOptimizer(
                learning_rate=self.learning_rate,
                beta1=0.9,
                beta2=0.999,
                epsilon=1e-08
            )
            self.optm = _opt.minimize(self.loss)

        except Exception as e :
            raise Exception (e)

    def _run_train(self, sess, xbatch, ybatch, target):
        """

        :return:
        """
        try :

            # Learning rate scheduling
            #sess.run(tf.assign(self.lr, self.learning_rate * (self.decay_rate ** epoch)))
            state = sess.run(self.istate)
            train_loss, state, _ = sess.run([self.cost, self.final_state, self.optm]
                                            , feed_dict={self.input_data: xbatch,
                                                         self.output_data: ybatch,
                                                         self.targets: target,
                                                         self.istate: state})
            print("[{0}] train_loss : {1}".format(self.epoch, train_loss))
            return sess
        except Exception as e :
            raise Exception(e)

    def _set_predict_model(self):
        """prob_idx
        set tensorflow seq2seq model for train and predict
        :return:
        """
        try :
            # off onehot to add dict on predict time
            if (self.word_embed_type == 'onehot'):
                self.onehot_encoder.off_edit_mode()

            # Construct RNN model
            cells = []
            for _ in range(self.encoder_num_layers) :
                unitcell = tf.contrib.rnn.BasicLSTMCell(self.cell_size)
                cells.append(unitcell)
            self.mul_cell = tf.contrib.rnn.MultiRNNCell(cells)
            self.input_data = tf.placeholder(tf.float32, [self.predict_batch, self.encoder_seq_length, self.word_vector_size])
            self.output_data = tf.placeholder(tf.float32, [self.predict_batch, self.decoder_seq_length, self.word_vector_size])
            self.istate = self.mul_cell.zero_state(self.predict_batch, tf.float32)

            # set weight vectors
            self._set_weight_vectors()

            # Weigths
            inputs = tf.split(self.input_data, self.encoder_seq_length, 1)
            inputs = [tf.squeeze(_input, [1]) for _input in inputs]
            outputs = tf.split(self.output_data, self.decoder_seq_length, 1)
            outputs = [tf.squeeze(_output, [1]) for _output in outputs]

            self.outputs, self.last_state = tf.contrib.legacy_seq2seq.basic_rnn_seq2seq(inputs,
                                                                                   outputs,
                                                                                   self.mul_cell,
                                                                                   dtype=tf.float32,
                                                                                   scope='rnnlm')

            self.output = tf.reshape(tf.concat(self.outputs, 1), [-1, self.cell_size])
            self.logits = tf.nn.xw_plus_b(self.output, self.softmax_w, self.softmax_b)
            self.probs = tf.nn.softmax(self.logits)
            self.init_val = tf.initialize_all_variables()
            self.saver = tf.train.Saver(tf.all_variables())
        except Exception as e :
            raise Exception (e)

    def _run_predict(self, sess, x_input, type='raw', clean_ans=True, predict_num=0, batch_ver='eval', saver=None):
        """
        run actual predict
        :return:
        """
        try :
            #restore model
            if(saver == None) :
                saver = tf.train.Saver(tf.all_variables())
            if (batch_ver == 'eval') :
                batch_ver_name = self.get_eval_batch(self.node_id)
            else :
                batch_ver_name = self.get_active_batch(self.node_id)

            if (self.check_batch_exist(self.node_id)):
                saver.restore(sess, ''.join([self.md_store_path , '/', batch_ver_name, '/']))
            else :
                raise Exception ("error : no pretrained model exist")

            #preprocess input data if necessary
            word_list = []
            if(type == 'raw') :
                word_list = [self._pos_tag_predict_data(x_input)]
            elif(type=='pre'):
                word_list = [x_input]
            else :
                raise Exception ("Wrong predict data type error!")

            # run predict
            output = ['@'] + [''] * (self.decoder_seq_length - 1)
            responses = []
            state = sess.run(self.mul_cell.zero_state(1, tf.float32))
            outputs, probs, state = sess.run([self.outputs, self.probs, self.last_state] ,
                                     feed_dict={self.input_data: self._word_embed_data(np.array(word_list)),
                                                self.output_data: self._word_embed_data(np.array([output])),
                                                self.istate: state})
            for idx in range(0, predict_num + 1) :
                response = None
                if(clean_ans) :
                    #prepare clean answer
                    response = ""
                    start_flag = False
                    for i in range(0,self.decoder_seq_length) :
                        word = self._get_index2vocab(np.array([[probs[i]]]), prob_idx = idx)[0][0]
                        response, flag, start_flag = self._clean_predict_result(word, response, start_flag)
                        if(flag == False) :
                            break
                else :
                    #return vector
                    response = []
                    for i in range(0, self.decoder_seq_length):
                        word = self._get_index2vocab(np.array([[probs[i]]]), prob_idx = idx)[0][0]
                        response.append(word)
                responses.append(response)
            return responses
        except Exception as e :
            raise Exception(e)

    def _pad_predict_input(self, input_tuple):
        """
        pad chars for prediction
        :param input_tuple:
        :return:
        """
        pad_size = self.encoder_seq_length - (len(input_tuple) + 1)
        if(pad_size >= 0 ) :
            input_tuple = pad_size * [('#', '')] + input_tuple[0: self.encoder_seq_length-1] + [('SF', '')]
        else :
            input_tuple = input_tuple[0: self.encoder_seq_length-1] + [('SF', '')]
        return input_tuple

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

    def _clean_predict_result(self, word, respone, start_flag):
        """
        clean predict result
        :param word:
        :return:
        """
        if (word in ['START', '@']):
            start_flag = True
        if (word not in ['PAD', 'UNKNOWN', 'START', '#', '@', 'SF', '.'] and start_flag == True and len(word) > 0):
            if ('/' in word):
                return respone + ' ' + word.split('/')[0] , True, start_flag
            if ('/' not in word):
                return respone + ' ' + word , True, start_flag
        if (word in ['SF', './SF', '?/SF']):
            return respone , False, start_flag
        return respone, True, start_flag