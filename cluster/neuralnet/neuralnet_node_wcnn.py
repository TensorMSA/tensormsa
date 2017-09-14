from cluster.neuralnet.neuralnet_node import NeuralNetNode
from common.utils import *
from master.workflow.netconf.workflow_netconf_wcnn import WorkFlowNetConfWideCnn as WFConf
import tensorflow as tf
import io, logging
from cluster.common.train_summary_info import TrainSummaryInfo
from common.graph.nn_graph_manager import NeuralNetModel
import numpy as np

class NeuralNetNodeWideCnn(NeuralNetNode):
    """
    """
    def _init_node_parm(self, node_id = None):
        """
        init necessary net conf
        :return:
        """
        try :
            # set global parms
            self.conf_data = None
            self.train_feed_name = None
            self.eval_feed_name = None
            if(node_id) :
                self.node_id = node_id
            else :
                self.node_id = self.get_node_name()
                self.node = self.get_node_def()
            self.model = None
            self.X = None
            self.Y = None
            self.optimizer = None
            self.y_pred_cls = None
            self.accuracy = None
            self.global_step = None
            self.cost = None
            self.predict_batch = 1

            #set_netconf_parm
            self.netconf = WFConf(self.node_id)
            self.learnrate = self.netconf.learnrate
            self.numoutputs = self.netconf.layeroutputs
            self.fclayer = self.netconf.out
            self.epoch = self.netconf.epoch
            self.batchsize = self.netconf.batch_size
            self.modelname = self.netconf.modelname
            self.train_cnt = self.netconf.traincnt
            self.model_path = self.netconf.model_path
            self.eval_type = self.netconf.type
            self.pred_cnt = self.netconf.predictcnt
        except Exception as e :
            raise Exception ("error on setting parms for wcnn : {0}".format(e))

    def _set_dataconf_parm(self, dataconf) :
        """
        set parms from data conf
        :param self:
        :return:
        """
        try :
            # set data parm
            self.dataconf = dataconf
            self.x_size = dataconf.word_vector_size
            self.y_size = dataconf.encode_len
            self.word_vector_size = dataconf.word_vector_size
            self.encode_len = dataconf.encode_len
            self.encode_channel = dataconf.encode_channel
            self.num_classes = dataconf.lable_size
            self.embed_type = dataconf.embed_type
            self.lable_onehot = dataconf.lable_onehot
            self.input_onehot = dataconf.input_onehot
            self.char_embed_flag = dataconf.char_embed
            self.vocab_size = dataconf.vocab_size + 4
            self.char_max_len = dataconf.char_max_len
            self.char_embed_size = dataconf.char_embed_size
        except Exception as e :
            raise Exception ("error on set up data conf : {0}".format(e))

    def _get_node_parm(self, node_id):
        """
        return conf master class
        :return:
        """
        return WFConf(node_id)

    def run(self, conf_data):
        """
        run network train task
        :param conf_data:
        :return:
        """
        try :
            logging.debug("run WCNN Train")
            self._init_node_parm()

            # set global
            self.node_id = conf_data['node_id']
            self.conf_data = conf_data
            self.nn_id = conf_data['nn_id']
            self.wfver = conf_data['wf_ver']

            # get prev node for load data
            train_data_set = self.get_linked_prev_node_with_grp('preprocess')[0]

            # get data size from preprocess node
            self._set_dataconf_parm(train_data_set)

            # prepare net conf
            tf.reset_default_graph()
            # get model andn train
            self.get_model(self.netconf, "T")

            # create session and run train
            with tf.Session() as sess:
                # initialize session
                sess.run(self.init_val)

                # restore saved model
                saver = self.saver
                if (self.check_batch_exist(conf_data['node_id'])):
                    path = ''.join([self.model_path, '/', self.get_eval_batch(self.node_id), '/'])
                    set_filepaths(path)
                    saver.restore(sess, path)

                # train model feed data
                for _ in range(self.epoch):
                    self._train_run(train_data_set, sess)

                # save model and close session
                path = ''.join([self.model_path, '/', self.make_batch(self.node_id)[1], '/'])
                set_filepaths(path)
                saver.save(sess, path)
            return ""
        except Exception as e:
            logging.info("[WCNN Train Process] : {0}".format(e))
            raise Exception ("error on train : {0}".format(e))
        finally:
            # copy data feeder's parm to netconf
            self._set_dataconf_parm(train_data_set)
            self._copy_node_parms(train_data_set, self)

    def _set_progress_state(self):
        return None

    def get_model(self, netconf, type):
        """
        create graph
        :param netconf:
        :param type:
        :return:
        """
        try :
            global_step = tf.Variable(initial_value=10, name='global_step', trainable=False)
            # placeholder is used for feeding data.
            x = tf.placeholder("float", shape=[None, self.y_size, self.x_size, 1], name='x')
            y_target = tf.placeholder("float", shape=[None, self.num_classes], name='y_target')
            x_image = tf.reshape(x, [-1, self.y_size, self.x_size, 1], name="x_image")
            # Keeping track of l2 regularization loss (optional)
            l2_loss = tf.constant(0.0)

            layer = netconf.get_layer_info
            filter_sizes = layer["cnnfilter"]
            num_filters = len(filter_sizes)

            pooled_outputs = []
            for i, filter_size in enumerate(filter_sizes):
                with tf.name_scope("conv-maxpool-%s" % filter_size):
                    # Convolution Layer
                    filter_shape = [filter_size, self.x_size, 1, num_filters]
                    W_conv1 = tf.Variable(tf.truncated_normal(filter_shape, stddev=0.1), name="W")
                    b_conv1 = tf.Variable(tf.constant(0.1, shape=[num_filters]), name="b")

                    conv = tf.nn.conv2d(
                        x_image,
                        W_conv1,
                        strides=[1, 1, 1, 1],
                        padding="VALID",
                        name="conv")

                    # Apply nonlinearity
                    h = tf.nn.relu(tf.nn.bias_add(conv, b_conv1), name="relu")
                    # Maxpooling over the outputs
                    pooled = tf.nn.max_pool(
                        h,
                        ksize=[1, self.y_size - filter_size + 1, 1, 1],
                        strides=[1, 1, 1, 1],
                        padding='VALID',
                        name="pool")
                    pooled_outputs.append(pooled)

            # Combine all the pooled features
            num_filters_total = num_filters * len(filter_sizes)
            h_pool = tf.concat(pooled_outputs, 3)
            h_pool_flat = tf.reshape(h_pool, [-1, num_filters_total])

            # Add dropout
            keep_prob = 1.0
            if type == 'T' and str(layer["droprate"]) is not "":
                keep_prob = float(layer["droprate"])
                h_pool_flat = tf.nn.dropout(h_pool_flat, keep_prob)

            # Final (unnormalized) scores and predictions
            W_fc1 = tf.get_variable(
                "W_fc1",
                shape=[num_filters_total, self.num_classes],
                initializer=tf.contrib.layers.xavier_initializer())
            b_fc1 = tf.Variable(tf.constant(0.1, shape=[self.num_classes]), name="b")
            l2_loss += tf.nn.l2_loss(W_fc1)
            l2_loss += tf.nn.l2_loss(b_fc1)
            y = tf.nn.xw_plus_b(h_pool_flat, W_fc1, b_fc1, name="scores")
            predictions = tf.argmax(y, 1, name="predictions")

            # CalculateMean cross-entropy loss
            losses = tf.nn.softmax_cross_entropy_with_logits(logits=y, labels=y_target)
            cross_entropy = tf.reduce_mean(losses)

            train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy, global_step = global_step)

            # Accuracy
            correct_predictions = tf.equal(predictions, tf.argmax(y_target, 1))
            accuracy = tf.reduce_mean(tf.cast(correct_predictions, "float"), name="accuracy")

            self.model = y
            self.X = x
            self.Y = y_target
            self.optimizer = train_step
            self.y_pred_cls = predictions
            self.accuracy = accuracy
            self.global_step = global_step
            self.cost = cross_entropy
            self.init_val = tf.initialize_all_variables()
            self.saver = tf.train.Saver(tf.all_variables())
        except Exception as e:
            raise Exception("WCNN graph prepare error : {0}".format(e))

    def _train_run(self, input_data, sess):
        """
        feed data for net
        :param input_data:
        :param out_data:
        :return:
        """
        try:
            return_arr = []
            g_total_cnt = 0
            while (input_data.has_next()):
                for i in range(0, input_data.data_size(), self.batchsize):
                    x_batch, y_batch  = input_data[i:i + self.batchsize]
                    for i in range(self.train_cnt):
                        i_global, _, i_cost, batch_acc = sess.run([self.global_step, self.optimizer, self.cost, self.accuracy],
                                                                  feed_dict={self.X: x_batch, self.Y: y_batch})
                        g_total_cnt += 1
                    if (g_total_cnt % 1 == 0) :
                        logging.info("count : {0} , Cost : {1}, Acc : {2}".format(i_global, i_cost, batch_acc))
                input_data.next()
            input_data.reset_pointer()
        except Exception as e:
            raise Exception ("WCNN on data feed error : {0}".format(e))
        return return_arr

    def eval(self, node_id, conf_data, data=None, result=None):
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
            lables =  self.dataconf.__dict__['lable_onehot'].dict_list
            lables.append(-1)
            result.set_result_data_format({"labels":lables})
            result.set_nn_batch_ver_id(self.get_eval_batch(node_id))

            tf.reset_default_graph()
            # prepare net conf
            self.get_model(self.netconf, "P")
            with tf.Session() as sess :
                sess.run(self.init_val)
                self.node_id = node_id
                if (self.check_batch_exist(self.node_id)):
                    self.saver.restore(sess, ''.join([self.model_path, '/', self.get_eval_batch(self.node_id), '/']))

                while (data.has_next()):
                    for i in range(0, data.data_size(), self.predict_batch):
                        data_set = data[i:i + self.predict_batch]
                        if (len(data_set[0]) != self.predict_batch): break
                        predict = self._run_predict(sess,
                                                    data_set[0][0],
                                                    saver=self.saver)
                        result.set_result_info(lables[data_set[1][0].index(1.0)],
                                               predict[0] if predict[0] in lables else -1)
                    data.next()
            return result
        except Exception as e :
            raise Exception ("error on eval wcnn : {0}".format(e))

    def predict(self, node_id, parm = {"input_data" : {}, "num" : 0}):
        """
        predict result with pretrained model
        :param node_id:
        :param filelist:
        :return:
        """
        try :
            # init params
            self._init_node_parm(node_id = node_id)

            # get prev node for load data
            self._set_dataconf_parm(self.netconf)

            # get unique key
            unique_key = '__'.join([node_id, self.get_eval_batch(node_id)])

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
                self.get_model(self.netconf, "P")
                graph = tf.get_default_graph()

            if (NeuralNetModel.sess.get(unique_key) == None):
                sess = tf.Session(graph=graph)
                batch_ver_name = self.get_eval_batch(self.node_id)

                if (self.check_batch_exist(self.node_id)):
                    self.saver.restore(sess, ''.join([self.model_path, '/', batch_ver_name, '/']))
                    NeuralNetModel.set_dict(unique_key, self)
                    NeuralNetModel.set_graph(unique_key, graph)
                    NeuralNetModel.set_sess(unique_key,sess)
                else:
                    raise Exception("error : no pretrained model exist")
            else :
                sess = NeuralNetModel.sess.get(unique_key)

            return self._run_predict(sess,
                                     parm['input_data'],
                                     batch_ver='eval',  # TODO : need to manage predict version too
                                     type='raw',
                                     saver=self.saver)

        except Exception as e :
            raise Exception ("wcnn predict prepare process error : {0}".format(e))

    def _run_predict(self, sess, x_input, batch_ver='eval', type='pre', saver=None):
        """

        :param filelist:
        :return:
        """
        try :
            #preprocess input data if necessary
            word_list = []
            if(type == 'raw'):
                if(self.netconf.get_preprocess_type == 'mecab'):
                    word_list = [self._pos_tag_predict_data(x_input, self.y_size)]
                else:
                    pad_size = self.y_size - (len(x_input.split(' ')))
                    if (pad_size >= 0):
                        word_list = [pad_size * [('#')] + list(map(lambda x : x, x_input.split(' ')))]
                    else:
                        word_list = [x_input.split(' ')]

                word_list = self._word_embed_data('onehot',
                                                  np.array(word_list),
                                                  cls=self.input_onehot,
                                                  char_embed=self.char_embed_flag)
                word_list = np.array(word_list).reshape([-1, self.y_size, self.x_size, self.encode_channel])
            elif(type=='pre'):
                word_list = [x_input]
            else :
                raise Exception ("Wrong predict data type error!")

            # run predict
            responses = []
            logits, outputs = sess.run([self.model, self.y_pred_cls], feed_dict={self.X: word_list})
            responses.append(self.lable_onehot.get_vocab(logits[0]))
            return responses
        except Exception as e :
            raise Exception(e)


