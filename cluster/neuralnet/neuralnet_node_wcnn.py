from cluster.neuralnet.neuralnet_node import NeuralNetNode
from common.utils import *
from master.workflow.netconf.workflow_netconf_wcnn import WorkFlowNetConfWideCnn as WFConf
import tensorflow as tf
import io, logging
from cluster.common.train_summary_info import TrainSummaryInfo
from common.graph.nn_graph_manager import NeuralNetModel

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
        # set data parm
        self.dataconf = dataconf
        self.x_size = dataconf.word_vector_size
        self.y_size = dataconf.encode_len
        self.channel = dataconf.encode_channel
        self.num_classes = dataconf.lable_size
        self.embed_type = dataconf.embed_type
        self.lable_onehot = dataconf.lable_onehot
        self.input_onehot = dataconf.input_onehot

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
                sess.run(tf.initialize_all_variables())

                # restore saved model
                saver = tf.train.Saver(tf.all_variables())
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
        except Exception as e :
            raise Exception ("error on train : {0}".format(e))
        finally :
            # copy data feeder's parm to netconf
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
            prenumoutputs = 1
            global_step = tf.Variable(initial_value=10, name='global_step', trainable=False)
            X = tf.placeholder(tf.float32, shape=[None, self.x_size, self.y_size, self.channel], name='x')
            Y = tf.placeholder(tf.float32, shape=[None, self.num_classes], name='y')
            stopper = 1
            model = X
            numoutputs = self.numoutputs

            layers = netconf.get_layer_info
            for layer in layers :
                layercnt = layer["layercnt"]
                for i in range(layercnt):
                    if prenumoutputs == 1:
                        prenumoutputs = numoutputs
                    else:
                        numoutputs = prenumoutputs * 2
                        prenumoutputs = numoutputs
                    active = str(layer["active"])
                    convkernelsize = [int((layer["cnnfilter"][0])), int((layer["cnnfilter"][1]))]
                    maxpkernelsize = [int((layer["maxpoolmatrix"][0])), int((layer["maxpoolmatrix"][1]))]
                    stride = [int((layer["maxpoolstride"][0])), int((layer["maxpoolstride"][1]))]
                    padding = str((layer["padding"]))

                    if active == 'relu':
                        activitaion = tf.nn.relu
                    else:
                        activitaion = tf.nn.relu

                    if str(layer["droprate"]) is not "":
                        droprate = float((layer["droprate"]))
                    else:
                        droprate = 0.0

                    model = tf.contrib.layers.conv2d(inputs=model
                                                     , num_outputs=numoutputs
                                                     , kernel_size=convkernelsize
                                                     , activation_fn=activitaion
                                                     , weights_initializer=tf.contrib.layers.xavier_initializer_conv2d()
                                                     , padding=padding)

                    model = tf.contrib.layers.max_pool2d(inputs=model
                                                         , kernel_size=maxpkernelsize
                                                         , stride=stride
                                                         , padding=padding)

                    if droprate > 0.0 and type == "T":
                        model = tf.nn.dropout(model, droprate)


            reout = int(model.shape[1]) * int(model.shape[2]) * int(model.shape[3])
            model = tf.reshape(model, [-1, reout])

            W1 = tf.Variable(tf.truncated_normal([reout, self.fclayer["node_out"]], stddev=0.1))
            model = tf.nn.relu(tf.matmul(model, W1))

            W5 = tf.Variable(tf.truncated_normal([self.fclayer["node_out"], self.num_classes], stddev=0.1))
            model = tf.matmul(model, W5)

            if type == "P":
                model = tf.nn.softmax(model)
            cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=model, labels=Y))
            optimizer = tf.train.AdamOptimizer(learning_rate=self.learnrate).minimize(cost, global_step=global_step)
            y_pred_cls = tf.argmax(model, 1)
            check_prediction = tf.equal(y_pred_cls, tf.argmax(Y, 1))
            accuracy = tf.reduce_mean(tf.cast(check_prediction, tf.float32))

            self.model = model
            self.X = X
            self.Y = Y
            self.optimizer = optimizer
            self.y_pred_cls = y_pred_cls
            self.accuracy = accuracy
            self.global_step = global_step
            self.cost = cost

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
                        print(i_cost)
                        # TODO : save loss, acc on train preprocess
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
            lables =  self.dataconf.wf_conf.get_lable_list
            result.set_result_data_format({"labels":lables})
            tf.reset_default_graph()
            with tf.Session() as sess :
                sess.run(tf.initialize_all_variables())
                # prepare net conf
                self.get_model(self.netconf, "P")
                self.node_id = node_id

                while (data.has_next()):
                    for i in range(0, data.data_size(), self.predict_batch):
                        data_set = data[i:i + self.predict_batch]
                        if (len(data_set[0]) != self.predict_batch): break
                        predict = self._run_predict(sess,
                                                    data_set[0][0],
                                                    tf=tf)
                        result.set_result_info(lables[data_set[1][0].index(1.0)],
                                               lables[predict[0][0]])
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
            unique_key = '_'.join([node_id, self.get_eval_batch(node_id)])

            # set init params
            self.node_id = node_id
            self._init_node_parm(self.node_id)

            # prepare net conf
            tf.reset_default_graph()

            ## create tensorflow graph
            if (NeuralNetModel.dict.get(unique_key)):
                self.__dict__ = NeuralNetModel.dict
            else:
                self.get_model(self.netconf, "P")
                NeuralNetModel.dict = self.__dict__

            # create session
            if (NeuralNetModel.tf.get(unique_key)):
                # case1 : cache reuse step
                m_tf = NeuralNetModel.tf.get(unique_key)
                init = m_tf.global_variables_initializer()
                sess = m_tf.Session()
                sess.run(init)
                temp_tf = m_tf
            else:
                # case2 : initialize step
                init = tf.global_variables_initializer()
                sess = tf.Session()
                sess.run(init)
                NeuralNetModel.tf[unique_key] = tf
                temp_tf = tf
            return self._run_predict(sess, parm['input_data'], tf=temp_tf, type='raw')
        except Exception as e :
            raise Exception ("wcnn predict prepare process error : {0}".format(e))
        finally :
            sess.close()

    def _run_predict(self, sess, x_input, tf=None, batch_ver='eval', type='pre'):
        """

        :param filelist:
        :return:
        """
        try :
            #restore model
            saver = tf.train.Saver(tf.all_variables())
            if (batch_ver == 'eval') :
                batch_ver_name = self.get_eval_batch(self.node_id)
            else :
                batch_ver_name = self.get_active_batch(self.node_id)

            if (self.check_batch_exist(self.node_id)):
                saver.restore(sess, ''.join([self.model_path , '/', batch_ver_name, '/']))
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
            responses = []
            logits, outputs = sess.run([self.model, self.y_pred_cls], feed_dict={self.X: word_list})
            responses.append(outputs)
            return responses
        except Exception as e :
            raise Exception(e)


