from cluster.neuralnet.neuralnet_node import NeuralNetNode
from common.utils import *
from master.workflow.netconf.workflow_netconf_cnn import WorkFlowNetConfCNN
import tensorflow as tf
import time
import numpy as np
from datetime import timedelta
from cluster.data.data_node_image import DataNodeImage
import os
import operator
import json
import datetime
import matplotlib.pyplot as plt
########################################################################
def plot_image(image, cls_true):
    # Create figure with sub-plots.
    fig, axes = plt.subplots(1, 1)

    if cls_true != None:
        axes.set_xlabel(cls_true)
    axes.imshow(image)

    plt.show()
########################################################################
def one_hot_encoded(num_classes):
    one = np.zeros((num_classes, num_classes))

    for i in range(num_classes):
        for j in range(num_classes):
            if i == j:
                one[i][j] = 1
    return one
########################################################################
def spaceprint(str, cnt):
    leng = len(str)
    cnt = cnt - leng
    restr = ""
    for i in range(cnt):
        restr += " "
    return restr
########################################################################
def model_file_delete(model_path, save_name):
    existcnt = 20
    filelist = os.listdir(model_path)

    flist = []
    i = 0
    for filename in filelist:
        filetime = datetime.datetime.fromtimestamp(os.path.getctime(model_path + '/' +filename)).strftime('%Y%m%d%H%M%S')
        tmp = [filename, filetime]
        if filename.find(save_name) > -1:
            flist.append(tmp)
        i += 1
        flistsort = sorted(flist, key=operator.itemgetter(1), reverse=True)
    # print(flistsort)

    for i in range(len(flistsort)):
        if i > existcnt * 3:
            os.remove(model_path + "/" + flistsort[i][0])
########################################################################
def get_model(netconf, dataconf, type):
    x_size = dataconf["preprocess"]["x_size"]
    y_size = dataconf["preprocess"]["y_size"]
    channel = dataconf["preprocess"]["channel"]
    num_classes = netconf["config"]["num_classes"]

    learnrate = netconf["config"]["learnrate"]
    global_step = tf.Variable(initial_value=10, name='global_step', trainable=False)
    ################################################################
    X = tf.placeholder(tf.float32, shape=[None, x_size, y_size, channel], name='x')
    Y = tf.placeholder(tf.float32, shape=[None, num_classes], name='y')
    ################################################################
    net_check = "S"
    stopper = 1
    model = X
    try:
        while True:
            try:
                layer = netconf["layer" + str(stopper)]
            except Exception as e:
                if stopper == 1:
                    net_check = "Error[100] .............................................."
                    model = "layer is None."
                    return net_check, model
                break
            println(layer)

            try:
                if str(layer["active"]) == 'relu':
                    activitaion = tf.nn.relu
                else:
                    activitaion = tf.nn.relu

                model = tf.contrib.layers.conv2d(inputs=model
                                              , num_outputs=int(layer["node_out"])
                                              , kernel_size=[int((layer["cnnfilter"][0])), int((layer["cnnfilter"][1]))]
                                              , activation_fn=activitaion
                                              , weights_initializer=tf.contrib.layers.xavier_initializer_conv2d()
                                              , padding=str((layer["padding"])))

                model = tf.contrib.layers.max_pool2d(inputs=model
                                                  , kernel_size=[int((layer["maxpoolmatrix"][0])),
                                                                 int((layer["maxpoolmatrix"][1]))]
                                                  , stride=[int((layer["maxpoolstride"][0])),
                                                            int((layer["maxpoolstride"][1]))]
                                                  , padding=str((layer["padding"])))

                if str(layer["droprate"]) is not "":
                    droprate = float((layer["droprate"]))
                else:
                    droprate = 0.0

                if droprate > 0.0 and type == "T":
                    model = tf.nn.dropout(model, droprate)

                println(model)
            except Exception as e:
                net_check = "Error[200] .............................................."
                model = e
                return net_check, model

            stopper += 1
            if (stopper >= 1000):
                break

        fclayer = netconf["out"]

        # 1. softmax
        reout = int(model.shape[1])*int(model.shape[2])*int(model.shape[3])
        model = tf.reshape(model, [-1, reout])
        println(model)
        W1 = tf.Variable(tf.truncated_normal([reout, fclayer["node_out"]], stddev=0.1))
        model = tf.nn.relu(tf.matmul(model, W1))
        println(model)
        W5 = tf.Variable(tf.truncated_normal([fclayer["node_out"], num_classes], stddev=0.1))
        model = tf.matmul(model, W5)
        println(model)
        #     # # 2. tf.contrib.layers.fully_connected
        #     model = tf.contrib.layers.flatten(model)
        #     model = tf.contrib.layers.fully_connected(model, fclayer["node_out"],
        #                                            normalizer_fn=tf.contrib.layers.batch_norm)
        #     model = tf.contrib.layers.fully_connected(model, num_classes)

        cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=model, labels=Y))
        optimizer = tf.train.AdamOptimizer(learning_rate=learnrate).minimize(cost, global_step=global_step)
        y_pred_cls = tf.argmax(model, 1)
        check_prediction = tf.equal(y_pred_cls, tf.argmax(Y, 1))
        accuracy = tf.reduce_mean(tf.cast(check_prediction, tf.float32))

    except Exception as e:
        net_check = "Error[300] .............................................."
        println(net_check)
        println(e)
        model = e

    return net_check, model, X, Y, optimizer, y_pred_cls, accuracy, global_step
########################################################################
def get_batch_data(data_set, dataconf, num_classes):
    x_size = dataconf["preprocess"]["x_size"]
    y_size = dataconf["preprocess"]["y_size"]
    channel = dataconf["preprocess"]["channel"]
    labels = dataconf["labels"]

    labelsHot = one_hot_encoded(num_classes)

    label_data_batch = data_set[1]
    img_data_batch = data_set[0]

    y_batch = np.zeros((len(label_data_batch), num_classes))
    r = 0
    for j in label_data_batch:
        j = j.decode('UTF-8')
        k = labels.index(j)
        y_batch[r] = labelsHot[k]
        r += 1

    x_batch = np.zeros((len(img_data_batch), len(img_data_batch[0])))
    r = 0
    for j in img_data_batch:
        j = j.tolist()
        x_batch[r] = j
        r += 1

    x_batch = np.reshape(x_batch, (-1, x_size, y_size, channel))

    # println("Image Label ////////////////////////////////////////////////")
    # println(label_data_batch)
    # println(y_batch)
    # println("Image /////////////////////////////////////////////////")
    # println(x_batch)

    return x_batch, y_batch
########################################################################
def train_cnn(input_data, netconf, dataconf, X, Y, optimizer, accuracy, global_step):
    batchsize = netconf["config"]["batch_size"]
    num_classes = netconf["config"]["num_classes"]
    start_time = time.time()

    try:
        return_arr = []
        while (input_data.has_next()):
            for i in range(0, input_data.size(), batchsize):
                data_set = input_data[i:i + batchsize]
                x_batch, y_batch = get_batch_data(data_set, dataconf, num_classes)
                return_data = train_run(x_batch, y_batch, netconf, X, Y, optimizer, accuracy, global_step, return_arr)
            input_data.next()
    except Exception as e:
        net_check = "Error[400] .............................................."
        println(net_check)
        println(e)
    # Ending time.
    end_time = time.time()

    # Difference between start and end-times.
    time_dif = end_time - start_time

    # Print the time-usage.
    println("Time usage: " + str(timedelta(seconds=int(round(time_dif)))))
    return_data = return_arr
    return return_data

def train_run(x_batch, y_batch, netconf, X, Y, optimizer, accuracy, global_step, return_arr):
    modelname = netconf["modelname"]
    train_cnt = netconf["config"]["traincnt"]
    model_path = netconf["modelpath"]
    save_path = model_path + "/" + modelname

    with tf.Session() as sess:
        try:
            last_chk_path = tf.train.latest_checkpoint(checkpoint_dir=model_path)
            saver = tf.train.Saver()
            saver.restore(sess, save_path=last_chk_path)
            println("Restored checkpoint from:" + last_chk_path)
        except:
            println("None to restore checkpoint. Initializing variables instead.")
            sess.run(tf.initialize_all_variables())

        for i in range(train_cnt):
            feed_dict_train = {X: x_batch, Y: y_batch}

            i_global, _ = sess.run([global_step, optimizer], feed_dict=feed_dict_train)

            # Print status to screen every 10 iterations (and last).
            if (i_global % 10 == 0) or (i == train_cnt - 1):
                # Calculate the accuracy on the training-batch.
                batch_acc = sess.run(accuracy, feed_dict=feed_dict_train)
                msg = "Global Step: {0:>6}, Training Batch Accuracy: {1:>6.1%}"
                println(msg.format(i_global, batch_acc))
                result = "Global Step:     "+str(i_global)+", Training Batch Accuracy:  "+str(batch_acc*100)+"%"
                return_arr.append(result)

            # Save a checkpoint to disk every 100 iterations (and last).
            if (i_global % 100 == 0) or (i == train_cnt - 1):
                println("Save model_path=" + model_path)
                saver.save(sess, save_path=save_path, global_step=global_step)
                model_file_delete(model_path, modelname)

    println("Saved checkpoint.")
    return return_arr
########################################################################
def eval_cnn(input_data, netconf, dataconf, X, Y, model, y_pred_cls):
    batchsize = netconf["config"]["batch_size"]
    num_classes = netconf["config"]["num_classes"]
    start_time = time.time()

    labels = dataconf["labels"]
    t_cnt_arr = []
    f_cnt_arr = []
    for i in range(len(labels)):
        t_cnt_arr.append(0)
        f_cnt_arr.append(0)

    try:
        while (input_data.has_next()):
            for i in range(0, input_data.size(), batchsize):
                data_set = input_data[i:i + batchsize]
                x_batch, y_batch = get_batch_data(data_set, dataconf, num_classes)
                t_cnt_arr, f_cnt_arr = eval_run(x_batch, y_batch, netconf, X, Y, model, y_pred_cls, labels, t_cnt_arr, f_cnt_arr)
            input_data.next()
    except Exception as e:
        net_check = "Error[500] .............................................."
        println(net_check)
        println(e)

    println("###################################################################################################")
    println(labels)
    for i in range(len(labels)):
        println("Category : " + labels[i] + spaceprint(labels[i], 15)
                + "TrueCnt=" + str(t_cnt_arr[i]) + spaceprint(str(t_cnt_arr[i]), 15)
                + "FalseCnt=" + str(f_cnt_arr[i]) + spaceprint(str(f_cnt_arr[i]), 15)
                + "TotalCnt=" + str(t_cnt_arr[i] + f_cnt_arr[i]) + spaceprint(str(t_cnt_arr[i] + f_cnt_arr[i]), 15)
                + "True Percent(TrueCnt/TotalCnt*100)=" + str(
            round(t_cnt_arr[i] / (t_cnt_arr[i] + f_cnt_arr[i]) * 100)) + "%")
    println("###################################################################################################")
    # println("TotalCnt=" + str(totalcnt) + " TrueCnt=" + str(t_cnt) + " FalseCnt=" + str(f_cnt))
    # percent = round(t_cnt / totalcnt * 100, 2)
    # println("Total Percent=" + str(percent) + "%")

    # Ending time.
    end_time = time.time()

    # Difference between start and end-times.
    time_dif = end_time - start_time

    # Print the time-usage.
    println("Time usage: " + str(timedelta(seconds=int(round(time_dif)))))

def eval_run(x_batch, y_batch, netconf, X, Y, model, y_pred_cls, labels, t_cnt_arr, f_cnt_arr):
    model_path = netconf["modelpath"]
    with tf.Session() as sess:
        try:
            last_chk_path = tf.train.latest_checkpoint(checkpoint_dir=model_path)
            saver = tf.train.Saver()
            saver.restore(sess, save_path=last_chk_path)
            println("Restored checkpoint from:" + last_chk_path)

            logits, y_pred_true = sess.run([model, y_pred_cls], feed_dict={X: x_batch})
            # # println(logits)
            for i in range(len(logits)):
                true_name = y_batch[i].decode('UTF-8')
                pred_name = labels[y_pred_true[i]]
                println("True Category=" + true_name + " Predict Category=" + pred_name)
                println(logits[i])
                idx = labels.index(true_name)
                if true_name == pred_name:
                    t_cnt_arr[idx] = t_cnt_arr[idx] + 1
                else:
                    f_cnt_arr[idx] = f_cnt_arr[idx] + 1
        except Exception as e:
            println("None to restore checkpoint. Initializing variables instead.")
            println(e)

########################################################################
def predict_run(filelist, netconf, dataconf, model, y_pred_cls, X):
    x_size = dataconf["preprocess"]["x_size"]
    y_size = dataconf["preprocess"]["y_size"]
    channel = dataconf["preprocess"]["channel"]
    pred_cnt = netconf["config"]["predictcnt"]
    model_path = netconf["modelpath"]

    filelist = sorted(filelist.items(), key=operator.itemgetter(0))
    # println(filelist)
    data = {}
    labels = dataconf["labels"]
    # println(labels)
    # labelsDictHot = one_hot_encoded(num_classes)
    with tf.Session() as sess:
        try:
            last_chk_path = tf.train.latest_checkpoint(checkpoint_dir=model_path)
            saverss = tf.train.Saver()
            saverss.restore(sess, save_path=last_chk_path)
            println("Restored checkpoint from:" + last_chk_path)

            for file in filelist:
                # println(file)
                value = file[1]
                filename = file[1].name

                for value in value.chunks():
                    # decoded_image = tf.image.decode_jpeg(chunk, channels=channel)
                    # resized_image = tf.image.resize_images(decoded_image, [x_size, y_size])
                    # resized_image = tf.cast(resized_image, tf.uint8)
                    decoded_image = tf.image.decode_image(contents=value, channels=channel, name="img")
                    resized_image = tf.image.resize_image_with_crop_or_pad(decoded_image, x_size, y_size)

                    try:
                        image = sess.run(resized_image)
                        image = image.reshape([-1, x_size, y_size, channel])
                        # println(image)

                        logits, y_pred_true = sess.run([model, y_pred_cls], feed_dict={X: image})
                        # println(logits)
                        # println(y_pred_true)
                        # cls_name = labels[y_pred_true[0]]
                        # println(cls_name)

                        one = np.zeros((len(labels), 2))

                        for i in range(len(labels)):
                            one[i][0] = i
                            one[i][1] = logits[0][i]

                        onesort = sorted(one, key=operator.itemgetter(1, 0), reverse=True)
                        # println("############################################")
                        println("filename=" + filename + " predict=" + labels[int(onesort[0][0])])
                        # println(onesort)
                        data_sub = {}
                        for i in range(pred_cnt):
                            key = str(i) + "key"
                            val = str(i) + "val"
                            data_sub[key] = labels[int(onesort[i][0])]
                            data_sub[val] = onesort[i][1]
                        data[filename] = data_sub
                        # println(file)
                        println(data_sub)
                    except:
                        data_sub = {}
                        for i in range(pred_cnt):
                            key = str(i) + "key"
                            val = str(i) + "val"
                            data_sub[key] = "Fail"
                            data_sub[val] = "Fail"
                        println(file)
                        println(data_sub)
                        data[filename] = data_sub
            println(
                "###################################################################################################")
            println(labels)
            # for i in range(len(labels)):
            #     println("Category : " + labels[i] +spaceprint(labels[i],15)
            #             + "TrueCnt=" + str(t_cnt_arr[i]) + spaceprint(str(t_cnt_arr[i]),15)
            #             + "FalseCnt=" + str(f_cnt_arr[i]) + spaceprint(str(f_cnt_arr[i]),15)
            #             + "TotalCnt=" + str(t_cnt_arr[i]+f_cnt_arr[i]) + spaceprint(str(t_cnt_arr[i]+f_cnt_arr[i]),15)
            #             + "True Percent(TrueCnt/TotalCnt*100)=" + str(round(t_cnt_arr[i] / (t_cnt_arr[i] + f_cnt_arr[i]) * 100))+ "%")
            # println("###################################################################################################")
            # println("TotalCnt=" + str(totalcnt) + " TrueCnt=" + str(t_cnt) + " FalseCnt=" + str(f_cnt))
            # percent = round(t_cnt/totalcnt*100,2)
            # println("Total Percent="+str(percent)+"%")
        except Exception as e:
            println("None to restore checkpoint. Initializing variables instead.")
            println(e)
    return data

class NeuralNetNodeCnn(NeuralNetNode):
    """
    """
    def _init_node_parm(self, node_id):
        wf_conf = WorkFlowNetConfCNN(node_id)
        # self.md_store_path = wf_conf.get_model_store_path()
        # self.window_size = wf_conf.get_window_size()
        # self.vector_size = wf_conf.get_vector_size()
        # self.batch_size = wf_conf.get_batch_size()
        # self.iter_size = wf_conf.get_iter_size()

    def _set_progress_state(self):
        return None

    def run(self, conf_data):
        println("run NeuralNetNodeCnn Train")
        println(conf_data)
        node_id = conf_data['node_id']
        self._init_node_parm(node_id)
        feed_node = self.get_prev_node()

        for feed in feed_node:
            feed_name = feed.get_node_name()
            data_node = feed.get_prev_node()
            for data in data_node:
                data_name = data.get_node_name()
                ################################################################
                netconf = WorkFlowNetConfCNN().get_view_obj(node_id)
                dataconf = WorkFlowNetConfCNN().get_view_obj(data_name)
                netconf = WorkFlowNetConfCNN().set_num_classes_predcnt(netconf, dataconf)

                net_check, model, X, Y, optimizer, y_pred_cls, accuracy, global_step = get_model(netconf, dataconf, "T")
                println(model)

                if net_check == "S":
                    cls_pool = conf_data['cls_pool']
                    input_data = cls_pool[feed_name]
                    return_arr = train_cnn(input_data, netconf, dataconf, X, Y, optimizer, accuracy, global_step)
                else:
                    println("net_check=" + net_check)

        println("end NeuralNetNodeCnn Train")
        return_data = {}
        return_data["TrainReult"] = return_arr
        return return_data

    def eval(self, conf_data):
    # def predict(self, node_id, filelist):
        println("run NeuralNetNodeCnn eval")
        println(conf_data)

        node_id = conf_data['node_id']
        self._init_node_parm(node_id)
        feed_node = self.get_prev_node()

        # for feed in feed_node:
        #     feed_name = feed.get_node_name()
        #     data_node = feed.get_prev_node()
        #     for data in data_node:
        #         data_name = data.get_node_name()

        feed_node = "nn00004_8_data_eval_feeder"
        data_name = "nn00004_8_evaldata"
        ################################################################
        # netconf = WorkFlowNetConfCNN().get_view_obj(node_id)
        # dataconf = WorkFlowNetConfCNN().get_view_obj(data_name)
        # netconf = WorkFlowNetConfCNN().set_num_classes_predcnt(netconf, dataconf)

        # net_check, model, X, Y, optimizer, y_pred_cls, accuracy, global_step = get_model(netconf, dataconf, "P")
        # println(model)
        #
        # if net_check == "S":
        #     cls_pool = conf_data['cls_pool']
        #     input_data = cls_pool[feed_node_name[0]]
        #     eval_cnn(input_data, netconf, dataconf, X, Y, optimizer, accuracy)
        # else:
        #     println("net_check=" + net_check)
        #
        # println("eval end........")

        println("end NeuralNetNodeCnn eval")
        return None

    def predict(self, node_id, filelist):
        """
        predict service method
        1. type (vector) : return vector
        2. type (sim) : positive list & negative list
        :param node_id:
        :param parm:
        :return:
        """
        println("run NeuralNetNodeCnn Predict")
        println(node_id)
        self._init_node_parm(node_id)
        ################################################################
        data_node_name = self._get_backward_node_with_type(node_id, 'data')
        netconf = WorkFlowNetConfCNN().get_view_obj(node_id)
        dataconf = WorkFlowNetConfCNN().get_view_obj(data_node_name[0])

        net_check, model, X, Y, optimizer, y_pred_cls, accuracy, global_step = get_model(netconf, dataconf, "P")
        println(model)

        if net_check == "S":
            data = predict_run(filelist, netconf, dataconf, model, y_pred_cls, X)
        else:
            println("net_check=" + net_check)

        println("end NeuralNetNodeCnn Predict")
        # NeuralNetNodeCnn().eval_cnn(conf_data)
        return data




