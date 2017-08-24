from cluster.neuralnet.neuralnet_node import NeuralNetNode
from common.utils import *
from master.workflow.netconf.workflow_netconf_cnn import WorkFlowNetConfCNN
from master.workflow.init.workflow_init_simple import WorkFlowSimpleManager
import tensorflow as tf
import numpy as np
import os
import operator
import datetime, logging
from cluster.common.train_summary_info import TrainSummaryInfo
from cluster.common.train_summary_accloss_info import TrainSummaryAccLossInfo
from common.graph.nn_graph_manager import NeuralNetModel

class NeuralNetNodeCnn(NeuralNetNode):
    """
    """
    def _init_train_parm(self, conf_data):
        # get initial value
        self.conf_data = conf_data
        self.cls_pool = conf_data["cls_pool"]
        self.nn_id = conf_data["nn_id"]
        self.wf_ver = conf_data["wf_ver"]
        self.node_id = conf_data["node_id"]
        self.node = WorkFlowSimpleManager().get_train_node()

        # get feed name
        self.train_feed_name = self.nn_id + "_" + self.wf_ver + "_" + WorkFlowSimpleManager().get_train_feed_node()
        self.eval_feed_name = self.nn_id + "_" + self.wf_ver + "_" + WorkFlowSimpleManager().get_eval_feed_node()
        self.feed_node = self.get_prev_node()

    def _init_value(self):
        self.g_ffile_print = "N"
        self.g_train_cnt = 0
        self.g_epoch_cnt = 0
        self.step_gap = 1
        self.file_end = '.h5'
        self.train_return_data = {}
        self.train_return_arr = ["Trainning .................................................."]
        self.pred_return_data = {}

    ####################################################################################################################
    def _set_netconf_parm(self):
        netconf = WorkFlowNetConfCNN().get_view_obj(self.node_id)
        try:
            netconf = WorkFlowNetConfCNN().set_num_classes_predcnt(self.nn_id, self.wf_ver, self.node, self.node_id, netconf)
        except:
            None
        self.netconf = netconf

        self.train_cnt = self.netconf["param"]["traincnt"]
        self.epoch = self.netconf["param"]["epoch"]
        self.batch_size = self.netconf["param"]["batch_size"]
        self.model_path = self.netconf["modelpath"]
        self.modelname = self.netconf["modelname"]

    def _set_dataconf_parm(self, dataconf):
        self.dataconf = dataconf

    ####################################################################################################################
    def get_saver_model(self, sess):
        self.model_path = self.netconf["modelpath"]
        self.modelname = self.netconf["modelname"]
        last_chk_path = tf.train.latest_checkpoint(checkpoint_dir=self.model_path)

        saver = None
        try:
            step = last_chk_path.split("-")
            self.step_gap = int(step[1]) + 1
            saver = tf.train.Saver()
            saver.restore(sess, save_path=last_chk_path)
            logging.info("Train Restored checkpoint from:" + last_chk_path)
        except:
            self.step_gap = 1
            logging.info("None to restore checkpoint. Initializing variables instead.")

        self.save_path = self.model_path + "/" + self.modelname + "-" + str(self.step_gap)

        return sess

    def set_saver_model(self, sess):
        saver = tf.train.Saver()
        saver.save(sess, save_path=self.save_path)

        batch_accR = round(self.batch_acc * 100, 2)
        msg = "Global Step: " + str(self.step_gap) + ", Training Batch Accuracy: " + str(
            batch_accR) + "%" + ", Cost: " + str(self.i_cost)
        logging.info(msg)

        config = {"nn_id": self.nn_id, "nn_wf_ver_id": self.wf_ver, "nn_batch_ver_id": self.batch}
        result = TrainSummaryAccLossInfo(config)
        result.loss_info["loss"] = str(self.i_cost)
        result.acc_info["acc"] = str(batch_accR)
        self.save_accloss_info(result)

        result = [msg]

        self.step_gap = self.step_gap + self.g_epoch_cnt
        self.save_path = self.model_path + "/" + self.modelname + "-" + str(self.step_gap)

        # self.model_file_delete(self.model_path, self.modelname)

        self.train_return_arr.append(result)

        self.eval(self.node_id, self.conf_data, None, None)

    def get_model_cnn(self, type=None):
        prenumoutputs = 1
        num_classes = self.netconf["config"]["num_classes"]
        learnrate = self.netconf["config"]["learnrate"]
        numoutputs = self.netconf["config"]["layeroutputs"]
        optimizer = self.netconf["config"]["optimizer"]
        node_out = self.netconf["out"]["node_out"]

        x_size = self.dataconf["preprocess"]["x_size"]
        y_size = self.dataconf["preprocess"]["y_size"]
        channel = self.dataconf["preprocess"]["channel"]
        ################################################################
        X = tf.placeholder(tf.float32, shape=[None, x_size, y_size, channel], name='x')
        Y = tf.placeholder(tf.float32, shape=[None, num_classes], name='y')
        ################################################################
        stopper = 1
        model = X

        while True:
            try:
                layer = self.netconf["layer" + str(stopper)]
            except Exception as e:
                if stopper == 1:
                    return "Error[100] layer is None ..............................."
                break
            stopper += 1

            try:
                layercnt = layer["layercnt"]
                for i in range(layercnt):
                    # logging.info(layer)
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

                    # logging.info(model)
            except Exception as e:
                logging.info("Error[200] Model Create Fail.")
                logging.info(e)

        reout = int(model.shape[1]) * int(model.shape[2]) * int(model.shape[3])
        model = tf.reshape(model, [-1, reout])
        # logging.info(model)
        W1 = tf.Variable(tf.truncated_normal([reout, node_out], stddev=0.1))
        model = tf.nn.relu(tf.matmul(model, W1))

        W5 = tf.Variable(tf.truncated_normal([node_out, num_classes], stddev=0.1))
        model = tf.matmul(model, W5)
        # logging.info(model)
        if type == "P":
            model = tf.nn.softmax(model)
        cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=model, labels=Y))
        if optimizer == "AdamOptimizer":
            optimizer = tf.train.AdamOptimizer(learning_rate=learnrate).minimize(cost)
        else:
            optimizer = tf.train.RMSPropOptimizer(learnrate, 0.9).minimize(cost)
        y_pred_cls = tf.argmax(model, 1)
        check_prediction = tf.equal(y_pred_cls, tf.argmax(Y, 1))
        accuracy = tf.reduce_mean(tf.cast(check_prediction, tf.float32))

        self.model = model
        self.X = X
        self.Y = Y
        self.optimizer = optimizer
        self.y_pred_cls = y_pred_cls
        self.accuracy = accuracy
        self.cost = cost

    ####################################################################################################################
    def train_run_cnn(self, sess, input_data, test_data):
        try:
            while (input_data.has_next()):
                for i in range(self.train_cnt):
                    for i in range(0, input_data.size(), self.batch_size):
                        data_set = input_data[i:i + self.batch_size]
                        x_batch, y_batch, n_batch = self.get_batch_img_data(data_set, "T")

                        for i in range(self.epoch):
                            feed_dict_train = {self.X: x_batch, self.Y: y_batch}

                            _, self.i_cost, self.batch_acc = sess.run([self.optimizer, self.cost, self.accuracy], feed_dict=feed_dict_train)

                            self.g_epoch_cnt += 1
                            logging.info("Epoch Count=" + str(self.g_epoch_cnt))

                        self.g_train_cnt += 1
                        logging.info("Save Train Count=" + str(self.g_train_cnt))
                        self.set_saver_model(sess)

                input_data.next()
        except Exception as e:
            logging.info("Error[400] ..............................................")
            logging.info(e)

        return self.train_return_data

    def run(self, conf_data):
        try :
            logging.info("run NeuralNetNodeCnn Train")
            # init data setup
            self._init_train_parm(conf_data)
            self._init_value()
            # set batch
            self.train_batch, self.batch = self.make_batch(self.node_id)

            # get data & dataconf
            test_data, dataconf = self.get_input_data(self.feed_node, self.cls_pool, self.eval_feed_name)
            input_data, dataconf = self.get_input_data(self.feed_node, self.cls_pool, self.train_feed_name)

            # set netconf, dataconf
            self._set_netconf_parm()
            self._set_dataconf_parm(dataconf)

            self.get_model_cnn("T")

            # train
            with tf.Session() as sess:
                sess = self.get_saver_model(sess)
                sess.run(tf.global_variables_initializer())
                self.train_run_cnn(sess, input_data, test_data)

            self.train_return_data["TrainResult"] = self.train_return_arr

            if self.epoch == 0 or self.train_cnt == 0:
                self.eval(self.node_id, self.conf_data, None, None)

            return self.train_return_data
        except Exception as e :
            logging.info("[Basic CNN Train Process] : {0}".format(e))

    ####################################################################################################################
    def eval_run(self, sess, input_data):
        self.batch_size = self.netconf["param"]["batch_size"]
        labels = self.netconf["labels"]
        pred_cnt = self.netconf["param"]["predictcnt"]
        try:
            predlog = self.netconf["param"]["predlog"]
        except:
            predlog = "N"
        # logging.info(labels)
        t_cnt_arr = []
        f_cnt_arr = []
        for i in range(len(labels)):
            t_cnt_arr.append(0)
            f_cnt_arr.append(0)

        input_data.pointer = 0
        while (input_data.has_next()):
            for i in range(0, input_data.size(), self.batch_size):
                data_set = input_data[i:i + self.batch_size]
                x_batch, y_batch, n_batch = self.get_batch_img_data(data_set, "E")

                try:
                    logits = sess.run([self.model], feed_dict={self.X: x_batch})
                    logits = logits[0]

                    for i in range(len(logits)):
                        true_name = y_batch[i]
                        file_name = n_batch[i]

                        logit = []
                        logit.append(logits[i])
                        #
                        idx = labels.index(true_name)
                        retrun_data = self.set_predict_return_cnn_img(labels, logit, pred_cnt)
                        pred_name =  retrun_data["key"][0]

                        if self.eval_flag == "E":
                            if true_name == pred_name:
                                t_cnt_arr[idx] = t_cnt_arr[idx] + 1
                                strLog = "[True] : "
                                if (predlog == "TT"):
                                    logging.info(strLog + true_name + " FileName=" + file_name)
                                    logging.info(retrun_data["key"])
                                    logging.info(retrun_data["val"])
                            else:
                                f_cnt_arr[idx] = f_cnt_arr[idx] + 1
                                strLog = "[False] : "
                                if (predlog == "FF"):
                                    logging.info(strLog + true_name + " FileName=" + file_name)
                                    logging.info(retrun_data["key"])
                                    logging.info(retrun_data["val"])
                            if (predlog == "AA"):
                                logging.info(strLog + true_name + " FileName=" + file_name)
                                logging.info(retrun_data["key"])
                                logging.info(retrun_data["val"])
                        else:
                            try:
                                listTF = retrun_data["key"].index(true_name)
                                t_cnt_arr[idx] = t_cnt_arr[idx] + 1
                                strLog = "[True] : "
                                if (predlog == "T"):
                                    logging.info(strLog + true_name + " FileName=" + file_name)
                                    logging.info(retrun_data["key"])
                                    logging.info(retrun_data["val"])
                            except:
                                f_cnt_arr[idx] = f_cnt_arr[idx] + 1
                                strLog = "[False] : "
                                if (predlog == "F"):
                                    logging.info(strLog + true_name + " FileName=" + file_name)
                                    logging.info(retrun_data["key"])
                                    logging.info(retrun_data["val"])
                            if(predlog == "A"):
                                logging.info(strLog + true_name + " FileName=" + file_name)
                                logging.info(retrun_data["key"])
                                logging.info(retrun_data["val"])


                        self.eval_data.set_result_info(true_name, pred_name)

                except Exception as e:
                    logging.info(e)
                    logging.info("None to restore checkpoint. Initializing variables instead.")

            input_data.next()

        self.eval_print(labels, t_cnt_arr, f_cnt_arr)

    def eval_print(self, labels, t_cnt_arr, f_cnt_arr):
        logging.info("####################################################################################################")
        result = []
        strResult = "['Eval ......................................................']"
        result.append(strResult)
        totCnt = 0
        tCnt = 0
        fCnt = 0
        for i in range(len(labels)):
            strResult = "Category : " + self.spaceprint(labels[i], 15) + " "
            strResult += "TotalCnt=" + self.spaceprint(str(t_cnt_arr[i] + f_cnt_arr[i]), 8) + " "
            strResult += "TrueCnt=" + self.spaceprint(str(t_cnt_arr[i]), 8) + " "
            strResult += "FalseCnt=" + self.spaceprint(str(f_cnt_arr[i]), 8) + " "
            if t_cnt_arr[i] + f_cnt_arr[i] != 0:
                strResult += "True Percent(TrueCnt/TotalCnt*100)=" + str(
                    round(t_cnt_arr[i] / (t_cnt_arr[i] + f_cnt_arr[i]) * 100)) + "%"
            totCnt += t_cnt_arr[i] + f_cnt_arr[i]
            tCnt += t_cnt_arr[i]
            fCnt += f_cnt_arr[i]
            logging.info(strResult)
            result.append(strResult)
        strResult = "---------------------------------------------------------------------------------------------------"
        logging.info(strResult)
        strResult = "Total Category=" + self.spaceprint(str(len(labels)), 11) + " "
        strResult += "TotalCnt=" + self.spaceprint(str(totCnt), 8) + " "
        strResult += "TrueCnt=" + self.spaceprint(str(tCnt), 8) + " "
        strResult += "FalseCnt=" + self.spaceprint(str(fCnt), 8) + " "
        if totCnt != 0:
            strResult += "True Percent(TrueCnt/TotalCnt*100)=" + str(round(tCnt / totCnt * 100)) + "%"
        logging.info(strResult)
        result.append(strResult)
        logging.info("###################################################################################################")

    def eval(self, node_id, conf_data, data=None, result=None):
        logging.info("run NeuralNetNodeCnn eval")
        if data == None:
            self.eval_flag = "T"
        else:
            self.eval_flag = "E"

        # eval
        self.batch = self.get_eval_batch(node_id)
        config = {"type": self.netconf["config"]["eval_type"], "labels": self.netconf["labels"], "nn_id": self.nn_id,
                  "nn_wf_ver_id": self.wf_ver, "nn_batch_ver_id": self.batch}
        self.eval_data = TrainSummaryInfo(conf=config)

        # get data & dataconf
        test_data, dataconf = self.get_input_data(self.feed_node, self.cls_pool, self.eval_feed_name)

        with tf.Session() as sess:
            sess = self.get_saver_model(sess)
            sess.run(tf.global_variables_initializer())

            self.eval_run(sess, test_data)

        return self.eval_data

    ####################################################################################################################
    def _run_predict(self, sess, filelist):
        sess.run(tf.global_variables_initializer())

        # data shape change MultiValuDict -> nd array
        filename_arr, filedata_arr = self.change_predict_fileList(filelist, self.dataconf)

        for i in range(len(filename_arr)):
            file_name = filename_arr[i]
            file_data = filedata_arr[i]

            logits = sess.run([self.model], feed_dict={self.X: file_data})
            logits = logits[0]

            labels = self.netconf["labels"]
            pred_cnt = self.netconf["param"]["predictcnt"]
            retrun_data = self.set_predict_return_cnn_img(labels, logits, pred_cnt)
            self.pred_return_data[file_name] = retrun_data
            logging.info("Return Data.......................................")
            logging.info(self.pred_return_data)

    def predict(self, node_id, filelist):
        """
        """
        logging.info("run NeuralNetNodeCnn Predict")
        # init data setup
        self.node_id = node_id
        self._init_value()
        # net, data config setup
        data_node_name = self._get_backward_node_with_type(node_id, 'data')
        dataconf = WorkFlowNetConfCNN().get_view_obj(data_node_name[0])
        self._set_netconf_parm()
        self._set_dataconf_parm(dataconf)
        self.net_type = self.netconf["config"]["net_type"]

        # get unique key
        unique_key = '_'.join([node_id, self.get_eval_batch(node_id)])

        # prepare net conf
        tf.reset_default_graph()

        ## create tensorflow graph
        if (NeuralNetModel.dict.get(unique_key)):
            self = NeuralNetModel.dict.get(unique_key)
            graph = NeuralNetModel.graph.get(unique_key)

            with tf.Session(graph=graph) as sess:
                self._run_predict(sess, filelist)
        else:
            self.get_model_cnn("P")
            NeuralNetModel.dict[unique_key] = self
            NeuralNetModel.graph[unique_key] = tf.get_default_graph()
            graph = tf.get_default_graph()

            with tf.Session() as sess:
                self._run_predict(sess, filelist)

        return self.pred_return_data

