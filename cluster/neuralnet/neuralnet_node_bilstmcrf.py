from cluster.neuralnet.neuralnet_node import NeuralNetNode
from master.workflow.netconf.workflow_netconf_bilstmcrf import WorkFlowNetConfBiLstmCrf
import os, json, logging
import numpy as np
import tensorflow as tf
from cluster.common.neural_common_bilismcrf import BiLstmCommon
from common.graph.nn_graph_manager import NeuralNetModel

class NeuralNetNodeBiLstmCrf(NeuralNetNode, BiLstmCommon):

    def run(self, conf_data):
        try :
            self._init_node_parm(conf_data['node_id'])

            # build graph
            self.build_graph()

            # get prev node for load data
            train_data_set = self.get_linked_prev_node_with_grp('preprocess')[0]
            best_score = 0
            with tf.Session() as sess:
                while (train_data_set.has_next()):
                    logging.info("------------------------------")
                    logging.info(train_data_set.get_file_name())
                    logging.info("------------------------------")
                    # create dataset
                    dev = self.CoNLLDataset(train_data_set.get_file_name(),
                                            self.processing_word,
                                            self.processing_tag,
                                            self.max_iter)
                    train = self.CoNLLDataset(train_data_set.get_file_name(),
                                              self.processing_word,
                                              self.processing_tag,
                                              self.max_iter)
                    # train
                    best_score = self.train(train, dev, self.vocab_tags, sess)

                    # save model
                    self.model_output = ''.join([self.md_store_path, '/', self.make_batch(self.node_id)[1], '/'])
                    if not os.path.exists(self.model_output):
                        os.makedirs(self.model_output)
                    self.saver.save(sess, self.model_output)

                    train_data_set.next()
            return [best_score]
        except Exception as e :
            logging.info("[BiLstmCrf Train Process] : {0}".format(e))
            raise Exception ("error on fast text tain process : {0}".format(e))

    def _init_node_parm(self, node_id):
        """
        initialze parms for autoencoder
        :param node_id:
        :return:
        """
        try:
            wf_conf = WorkFlowNetConfBiLstmCrf(node_id)
            self.node_id = node_id
            self.md_store_path = wf_conf.get_model_store_path

            # create dict folder for ner if not exists
            dict_path = ''.join([self.md_store_path, '/dict/'])
            if not os.path.exists(dict_path):
                os.makedirs(dict_path)

            self.trimmed_filename = ''.join([dict_path, 'words.vec'])
            self.charembed_filename = ''.join([dict_path, 'char.vec'])
            self.words_filename = ''.join([dict_path, 'words.txt'])
            self.tags_filename = ''.join([dict_path, 'tags.txt'])
            self.chars_filename = ''.join([dict_path, 'chars.txt'])

            self.embeddings = self.get_trimmed_glove_vectors(self.trimmed_filename)
            self.char_embed = self.get_trimmed_glove_vectors(self.charembed_filename)
            self.vocab_words = self.load_vocab(self.words_filename)
            self.vocab_tags = self.load_vocab(self.tags_filename)
            self.vocab_chars = self.load_vocab(self.chars_filename)

            self.nchars = len(self.vocab_chars)
            self.ntags = len(self.vocab_tags)
            self.lowercase = wf_conf.lowercase
            self.max_iter = wf_conf.max_iter
            self.crf = wf_conf.crf
            self.chars = wf_conf.chars

            self.processing_word = self.get_processing_word(self.vocab_words,
                                                            self.vocab_chars,
                                                            lowercase=self.lowercase,
                                                            chars=self.chars)
            self.processing_tag = self.get_processing_word(self.vocab_tags,
                                                           lowercase=False)

            self.dim = wf_conf.dim
            self.dim_char = wf_conf.dim_char
            self.train_embeddings = wf_conf.train_embeddings
            self.nepochs = wf_conf.nepochs
            self.p_dropout = wf_conf.p_dropout
            self.batch_size = wf_conf.batch_size
            self.p_lr = wf_conf.p_lr
            self.lr_decay = wf_conf.lr_decay
            self.nepoch_no_imprv = wf_conf.nepoch_no_imprv

            self.hidden_size = wf_conf.hidden_size
            self.char_hidden_size = wf_conf.char_hidden_size

            if(self.check_batch_exist(node_id)) :
                self.output_path = ''.join([self.md_store_path, '/', self.get_eval_batch(node_id), '/'])
            else :
                self.output_path = ''.join([self.md_store_path, '/', self.make_batch(node_id)[1], '/'])
            self.model_output = self.output_path
            self.log_path = self.output_path + "/log/log.txt"

        except Exception as e :
            raise Exception (e)

    def add_placeholders(self):
        """
        Adds placeholders to self
        """
        # shape = (batch size, max length of sentence in batch)
        self.word_ids = tf.placeholder(tf.int32, shape=[None, None], name="word_ids")
        # shape = (batch size)
        self.sequence_lengths = tf.placeholder(tf.int32, shape=[None], name="sequence_lengths")
        # shape = (batch size, max length of sentence, max length of word)
        self.char_ids = tf.placeholder(tf.int32, shape=[None, None, None], name="char_ids")
        # shape = (batch_size, max_length of sentence)
        self.word_lengths = tf.placeholder(tf.int32, shape=[None, None], name="word_lengths")
        # shape = (batch size, max length of sentence in batch)
        self.labels = tf.placeholder(tf.int32, shape=[None, None], name="labels")
        # hyper parameters
        self.dropout = tf.placeholder(dtype=tf.float32, shape=[], name="dropout")
        self.lr = tf.placeholder(dtype=tf.float32, shape=[], name="lr")


    def get_feed_dict(self, words, labels=None, lr=None, dropout=None):
        """
        Given some data, pad it and build a feed dictionary
        Args:
            words: list of sentences. A sentence is a list of ids of a list of words.
                A word is a list of ids
            labels: list of ids
            lr: (float) learning rate
            dropout: (float) keep prob
        Returns:
            dict {placeholder: value}
        """
        # perform padding of the given data
        if self.chars:
            char_ids, word_ids = zip(*words)
            word_ids, sequence_lengths = self.pad_sequences(word_ids, 0)
            char_ids, word_lengths = self.pad_sequences(char_ids, pad_tok=0, nlevels=2)
        else:
            word_ids, sequence_lengths = self.pad_sequences(words, 0)

        # build feed dictionary
        feed = {
            self.word_ids: word_ids,
            self.sequence_lengths: sequence_lengths
        }

        if self.chars:
            feed[self.char_ids] = char_ids
            feed[self.word_lengths] = word_lengths

        if labels is not None:
            labels, _ = self.pad_sequences(labels, 0)
            feed[self.labels] = labels

        if lr is not None:
            feed[self.lr] = lr

        if dropout is not None:
            feed[self.dropout] = dropout

        return feed, sequence_lengths


    def add_word_embeddings_op(self):
        """
        Adds word embeddings to self
        """
        with tf.variable_scope("words"):
            _word_embeddings = tf.Variable(self.embeddings, name="_word_embeddings", dtype=tf.float32,
                                trainable=self.train_embeddings)
            word_embeddings = tf.nn.embedding_lookup(_word_embeddings, self.word_ids,
                name="word_embeddings")

        with tf.variable_scope("chars"):
            if self.chars:

                if (self.char_embed is not None):
                    _char_embeddings = tf.Variable(self.char_embed, name="_char_embeddings", dtype=tf.float32,
                                                   trainable=self.train_embeddings)
                    char_embeddings = tf.nn.embedding_lookup(_char_embeddings, self.char_ids,
                                                             name="char_embeddings")
                else :
                    # get embeddings matrix
                    _char_embeddings = tf.get_variable(name="_char_embeddings", dtype=tf.float32,
                        shape=[self.nchars, self.dim_char])
                    char_embeddings = tf.nn.embedding_lookup(_char_embeddings, self.char_ids,
                        name="char_embeddings")
                # put the time dimension on axis=1
                s = tf.shape(char_embeddings)
                char_embeddings = tf.reshape(char_embeddings, shape=[-1, s[-2], self.dim_char])
                word_lengths = tf.reshape(self.word_lengths, shape=[-1])
                # bi lstm on chars
                lstm_frod_cell = tf.contrib.rnn.LSTMCell(self.char_hidden_size,
                                                    state_is_tuple=True)
                lstm_back_cell = tf.contrib.rnn.LSTMCell(self.char_hidden_size,
                                                    state_is_tuple=True)
                _, ((_, output_fw), (_, output_bw)) = tf.nn.bidirectional_dynamic_rnn(lstm_frod_cell,
                                                                                      lstm_back_cell,
                                                                                      char_embeddings,
                                                                                      sequence_length=word_lengths,
                                                                                      dtype=tf.float32)
                output = tf.concat([output_fw, output_bw], axis=-1)
                # shape = (batch size, max sentence length, char hidden size)
                output = tf.reshape(output, shape=[-1, s[1], 2*self.char_hidden_size])

                word_embeddings = tf.concat([word_embeddings, output], axis=-1)

        self.word_embeddings =  tf.nn.dropout(word_embeddings, self.dropout)


    def add_logits_op(self):
        """
        Adds logits to self
        """
        with tf.variable_scope("bi-lstm"):
            lstm_fwrd_cell = tf.contrib.rnn.LSTMCell(self.hidden_size)
            lstm_back_cell = tf.contrib.rnn.LSTMCell(self.hidden_size)
            (output_fw, output_bw), _ = tf.nn.bidirectional_dynamic_rnn(lstm_fwrd_cell,
                                                                        lstm_back_cell,
                                                                        self.word_embeddings,
                                                                        sequence_length=self.sequence_lengths,
                                                                        dtype=tf.float32)
            output = tf.concat([output_fw, output_bw], axis=-1)
            output = tf.nn.dropout(output, self.dropout)

        with tf.variable_scope("proj"):
            W = tf.get_variable("W", shape=[2*self.hidden_size, self.ntags],
                dtype=tf.float32)

            b = tf.get_variable("b", shape=[self.ntags], dtype=tf.float32,
                initializer=tf.zeros_initializer())

            ntime_steps = tf.shape(output)[1]
            output = tf.reshape(output, [-1, 2*self.hidden_size])
            pred = tf.matmul(output, W) + b
            self.logits = tf.reshape(pred, [-1, ntime_steps, self.ntags])

    def add_pred_op(self):
        """
        Adds labels_pred to self
        """
        if not self.crf:
            self.labels_pred = tf.cast(tf.argmax(self.logits, axis=-1), tf.int32)

    def add_loss_op(self):
        """
        Adds loss to self
        """
        if self.crf:
            log_likelihood, self.transition_params = tf.contrib.crf.crf_log_likelihood(
            self.logits, self.labels, self.sequence_lengths)
            self.loss = tf.reduce_mean(-log_likelihood)
        else:
            losses = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=self.logits, labels=self.labels)
            mask = tf.sequence_mask(self.sequence_lengths)
            losses = tf.boolean_mask(losses, mask)
            self.loss = tf.reduce_mean(losses)

        # for tensorboard
        tf.summary.scalar("loss", self.loss)


    def add_train_op(self):
        """
        Add train_op to self
        """
        with tf.variable_scope("train_step"):
            optimizer = tf.train.AdamOptimizer(self.lr)
            self.train_op = optimizer.minimize(self.loss)


    def add_init_op(self):
        self.init = tf.global_variables_initializer()
        self.saver = tf.train.Saver(tf.all_variables())


    def add_summary(self, sess):
        # tensorboard stuff
        self.merged = tf.summary.merge_all()
        self.file_writer = tf.summary.FileWriter(self.output_path, sess.graph)


    def build_graph(self):
        self.add_placeholders()
        self.add_word_embeddings_op()
        self.add_logits_op()
        self.add_pred_op()
        self.add_loss_op()
        self.add_train_op()
        self.add_init_op()



    def predict_batch(self, sess, words):
        """
        Args:
            sess: a tensorflow session
            words: list of sentences
        Returns:
            labels_pred: list of labels for each sentence
            sequence_length
        """
        fd, sequence_lengths = self.get_feed_dict(words, dropout=1.0)

        if self.crf:
            viterbi_sequences = []
            logits, transition_params = sess.run([self.logits, self.transition_params],
                                                 feed_dict=fd)
            # iterate over the sentences
            for logit, sequence_length in zip(logits, sequence_lengths):
                # keep only the valid time steps
                logit = logit[:sequence_length]
                viterbi_sequence, viterbi_score = tf.contrib.crf.viterbi_decode(
                    logit, transition_params)
                viterbi_sequences += [viterbi_sequence]

            return viterbi_sequences, sequence_lengths

        else:
            labels_pred = sess.run(self.labels_pred, feed_dict=fd)

            return labels_pred, sequence_lengths

    def run_epoch(self, sess, train, dev, tags, epoch):
        """
        Performs one complete pass over the train set and evaluate on dev
        Args:
            sess: tensorflow session
            train: dataset that yields tuple of sentences, tags
            dev: dataset
            tags: {tag: index} dictionary
            epoch: (int) number of the epoch
        """
        try :
            nbatches = (len(train) + self.batch_size - 1) / self.batch_size
            for i, (words, labels) in enumerate(self.minibatches(train, self.batch_size)):
                fd, _ = self.get_feed_dict(words, labels, self.p_lr, self.p_dropout)
                _, train_loss, summary = sess.run([self.train_op, self.loss, self.merged], feed_dict=fd)

                # tensorboard
                if i % 10 == 0:
                    self.file_writer.add_summary(summary, epoch * nbatches + i)

            acc, f1, _ = self.run_evaluate(sess, dev, tags)
            logging.info("- dev acc {:04.2f} - f1 {:04.2f}".format(100 * acc, 100 * f1))
            return acc, f1
        except Exception as e :
            print ("Exception on run_epoch {0}".format(e))

    def run_evaluate(self, sess, test, tags, result=None):
        """
        Evaluates performance on test set
        Args:
            sess: tensorflow session
            test: dataset that yields tuple of sentences, tags
            tags: {tag: index} dictionary
        Returns:
            accuracy
            f1 score
        """
        try:
            accs = []
            correct_preds, total_correct, total_preds = 0., 0., 0.
            for words, labels in self.minibatches(test, self.batch_size):
                labels_pred, sequence_lengths = self.predict_batch(sess, words)

                for lab, lab_pred, length in zip(labels, labels_pred, sequence_lengths):
                    lab = lab[:length]
                    lab_pred = lab_pred[:length]
                    accs += map(lambda x: x[0] == x[1], zip(lab, lab_pred))

                    lab_chunks = set(self.get_chunks(lab, tags))
                    lab_pred_chunks = set(self.get_chunks(lab_pred, tags))
                    if(result) :
                        if (len(self.get_chunks(lab_pred, tags)) > 0 and
                            len(self.get_chunks(lab, tags)) > 0 ) :
                            for label, pred in zip (self.get_chunks(lab, tags), self.get_chunks(lab_pred, tags)) :
                                result.set_result_info(label[0], pred[0])
                    correct_preds += len(lab_chunks & lab_pred_chunks)
                    total_preds += len(lab_pred_chunks)
                    total_correct += len(lab_chunks)

            p = correct_preds / total_preds if correct_preds > 0 else 0
            r = correct_preds / total_correct if correct_preds > 0 else 0
            f1 = 2 * p * r / (p + r) if correct_preds > 0 else 0
            acc = np.mean(accs)
            return acc, f1, result
        except Exception as e:
            raise Exception(e)

    def train(self, train, dev, tags, sess):
        """
        Performs training with early stopping and lr exponential decay
        Args:
            train: dataset that yields tuple of sentences, tags
            dev: dataset
            tags: {tag: index} dictionary
        """
        best_score = 0
        saver = tf.train.Saver()

        # for early stopping
        nepoch_no_imprv = 0
        sess.run(self.init)

        # restore model
        if (self.check_batch_exist(self.node_id) and os.path.exists(self.model_output)):
            saver.restore(sess, self.model_output)

        # tensorboard
        self.add_summary(sess)
        for epoch in range(self.nepochs):
            logging.info("Epoch {:} out of {:}".format(epoch + 1, self.nepochs))

            acc, f1 = self.run_epoch(sess, train, dev, tags, epoch)

            # decay learning rate
            self.p_lr *= self.lr_decay

            # early stopping and saving best parameters
            if f1 >= best_score:
                nepoch_no_imprv = 0
                best_score = f1
                logging.info("- new best score!")
            else:
                nepoch_no_imprv += 1
                if nepoch_no_imprv >= self.nepoch_no_imprv:
                    logging.info("- early stopping {} epochs without improvement".format(
                        nepoch_no_imprv))
                    break
        return best_score


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
            lables = list(map(lambda x : x.split('-')[-1], list(self.vocab_tags.keys())))
            result.set_result_data_format({"labels": lables})
            result.set_nn_batch_ver_id(self.get_eval_batch(node_id))

            with tf.Session() as sess:
                # load trained model
                if (self.check_batch_exist(self.node_id) and os.path.exists(self.model_output)):
                    self.saver.restore(sess, self.model_output)
                else:
                    raise Exception("bilstm crf error : no pretrained model exist")

                if(data.has_next() == False) :
                    result.set_result_info([''], [''])
                    logging.info("no test data exists")
                    return result

                while (data.has_next()):
                    test = self.CoNLLDataset(data.get_file_name(),
                                            self.processing_word,
                                            self.processing_tag,
                                            self.max_iter)
                    acc, f1, result = self.run_evaluate(sess, test, self.vocab_tags, result=result)
                    logging.info("- test acc {:04.2f} - f1 {:04.2f}".format(100 * acc, 100 * f1))
                    data.next()
            return result
        except Exception as e :
            raise Exception ("error on eval wcnn : {0}".format(e))


    def predict(self, node_id, parm={"input_data": {}}):
        """
        predict logic for ner
        tockenize input text and find matching tags for each value
        :param node_id:
        :param parm:
        :return:
        """
        try:
            # get unique key
            unique_key = '__'.join([node_id, self.get_eval_batch(node_id)])

            ## create tensorflow graph
            if (NeuralNetModel.dict.get(unique_key)):
                self = NeuralNetModel.dict.get(unique_key)
                graph = NeuralNetModel.graph.get(unique_key)
            else:
                # set init params
                self._init_node_parm(node_id)
                self.idx_to_tag = {idx: tag for tag, idx in iter(self.vocab_tags.items())}
                self.build_graph()
                graph = tf.get_default_graph()

            if (NeuralNetModel.sess.get(unique_key) == None) :
                sess = tf.Session(graph=graph)
                # load trained model
                if (self.check_batch_exist(self.node_id) and os.path.exists(self.model_output)):
                    self.saver.restore(sess, self.model_output)
                    NeuralNetModel.set_dict(unique_key, self)
                    NeuralNetModel.set_graph(unique_key, graph)
                    NeuralNetModel.set_sess(unique_key, sess)
                else:
                    raise Exception("bilstm crf error : no pretrained model exist")
            else :
                sess = NeuralNetModel.sess.get(unique_key)

            input_arr = parm["input_data"].split(' ')
            words = list(map(lambda x: self.processing_word(x), input_arr))
            if type(words[0]) == tuple:
                words = zip(*words)
            pred_ids, _ = self.predict_batch(sess, [words])
            preds = list(map(lambda idx: self.idx_to_tag[idx], list(pred_ids[0])))

            return preds
        except Exception as e:
            raise Exception(e)