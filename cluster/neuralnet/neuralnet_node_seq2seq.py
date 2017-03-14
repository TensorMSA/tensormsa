from cluster.neuralnet.neuralnet_node import NeuralNetNode
from master.workflow.netconf.workflow_netconf_seq2seq import WorkFlowNetConfSeq2Seq as WfNetconfSeq2Seq
import numpy as np
import tensorflow as tf
from cluster.service.service_predict_w2v import PredictNetW2V

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

            # get vector size
            if(len(decode_data) > 0) :
                self.vector_size = len(decode_data[0]['rawdata'][0:1].tolist()[0])
            else :
                raise Exception ('[error] NeuralNetNodeSeq2Seq : no train data exist')

            for encode, decode  in zip(encode_data, decode_data):
                encode_raw = encode['rawdata']
                decode_raw = decode['rawdata']
                for i in range(0, encode_raw.len(), 100):
                    encode_batch = self._word_embed_data(encode_raw[i:i + 100].tolist())
                    edcode_batch = self._word_embed_data(decode_raw[i:i + 100].tolist())

            # prepare net conf
            conf = self._set_net_conf()

            # run on session
        except Exception as e :
            raise Exception (e)

    def _init_node_parm(self, node_id):
        wf_conf = WfNetconfSeq2Seq(node_id)
        self.md_store_path = wf_conf.get_model_store_path()
        self.cell_type = wf_conf.get_cell_type()
        self.decoder_depth = wf_conf.get_decoder_depth()
        self.decoder_len = wf_conf.get_decoder_len()
        self.drop_out = wf_conf.get_drop_out()
        self.encoder_depth = wf_conf.get_encoder_depth()
        self.encoder_len = wf_conf.get_encoder_len()
        self.word_embed_type = wf_conf.get_word_embed_type()
        self.word_embed_id = wf_conf.get_word_embed_id()
        self.cell_size = wf_conf.get_cell_size()

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
                parm =  {"type" : "vector", "val_1" : data, "val_2" : []}
                return_arr.append(PredictNetW2V().run(self.word_embed_id, parm))
            return return_arr
        else :
            raise Exception ("[Error] seq2seq train - word embeding : not defined type {0}".format(self.word_embed_type))

    def _set_net_conf(self):
        """

        :return:
        """
        # Important RNN parameters
        vocab_size = self.vector_size
        rnn_size = self.cell_size
        num_layers = self.decoder_depth
        grad_clip = 5.
        batch_size = self.encoder_len
        seq_length = self.encoder_len

        # Construct RNN model
        unitcell = tf.nn.rnn_cell.BasicLSTMCell(rnn_size)
        cell = tf.nn.rnn_cell.MultiRNNCell([unitcell] * num_layers)
        input_data = tf.placeholder(tf.int32, [batch_size, seq_length])
        targets = tf.placeholder(tf.int32, [batch_size, seq_length])
        istate = cell.zero_state(batch_size, tf.float32)
        # Weigths
        with tf.variable_scope('rnnlm'):
            softmax_w = tf.get_variable("softmax_w", [rnn_size, vocab_size])
            softmax_b = tf.get_variable("softmax_b", [vocab_size])
            with tf.device("/cpu:0"):
                embedding = tf.get_variable("embedding", [vocab_size, rnn_size])
                inputs = tf.split(1, seq_length, tf.nn.embedding_lookup(embedding, input_data))
                inputs = [tf.squeeze(_input, [1]) for _input in inputs]

        # Output
        def loop(prev, _):
            prev = tf.nn.xw_plus_b(prev, softmax_w, softmax_b)
            prev_symbol = tf.stop_gradient(tf.argmax(prev, 1))
            return tf.nn.embedding_lookup(embedding, prev_symbol)

        """
            loop_function: If not None, this function will be applied to the i-th output
            in order to generate the i+1-st input, and decoder_inputs will be ignored,
            except for the first element ("GO" symbol).
        """
        outputs, last_state = tf.nn.seq2seq.rnn_decoder(inputs, istate, cell
                                                        , loop_function=None, scope='rnnlm')
        output = tf.reshape(tf.concat(1, outputs), [-1, rnn_size])
        logits = tf.nn.xw_plus_b(output, softmax_w, softmax_b)
        probs = tf.nn.softmax(logits)
        # Loss
        loss = tf.nn.seq2seq.sequence_loss_by_example([logits],  # Input
                                                      [tf.reshape(targets, [-1])],  # Target
                                                      [tf.ones([batch_size * seq_length])],  # Weight
                                                      vocab_size)
        # Optimizer
        cost = tf.reduce_sum(loss) / batch_size / seq_length
        final_state = last_state
        lr = tf.Variable(0.0, trainable=False)
        tvars = tf.trainable_variables()
        grads, _ = tf.clip_by_global_norm(tf.gradients(cost, tvars), grad_clip)
        _optm = tf.train.AdamOptimizer(lr)
        optm = _optm.apply_gradients(zip(grads, tvars))

        print("Network Ready")