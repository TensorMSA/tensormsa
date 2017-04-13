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
from PIL import Image
import io
from cluster.common.train_summary_info import TrainSummaryInfo

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
def spaceprint(val, cnt):
    leng = len(str(val))
    cnt = cnt - leng
    restr = ""
    for i in range(cnt):
        restr += " "
    restr = restr+str(val)
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
    numoutputs = netconf["config"]["layeroutputs"]
    prenumoutputs = 1
    global_step = tf.Variable(initial_value=10, name='global_step', trainable=False)
    ################################################################
    X = tf.placeholder(tf.float32, shape=[None, x_size, y_size, channel], name='x')
    Y = tf.placeholder(tf.float32, shape=[None, num_classes], name='y')
    ################################################################
    stopper = 1
    model = X
    net_check = 'S'

    while True:
        try:
            layer = netconf["layer" + str(stopper)]
        except Exception as e:
            if stopper == 1:
                net_check = "Error[100] layer is None ..............................."
                return net_check
            break
        stopper += 1

        try:
            layercnt = layer["layercnt"]
            for i in range(layercnt):
                # println(layer)
                if prenumoutputs == 1:
                    prenumoutputs = numoutputs
                else:
                    numoutputs = prenumoutputs*2
                    prenumoutputs = numoutputs
                active          = str(layer["active"])
                convkernelsize  = [int((layer["cnnfilter"][0])), int((layer["cnnfilter"][1]))]
                maxpkernelsize  = [int((layer["maxpoolmatrix"][0])), int((layer["maxpoolmatrix"][1]))]
                stride          = [int((layer["maxpoolstride"][0])), int((layer["maxpoolstride"][1]))]
                padding         = str((layer["padding"]))

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

                println(model)
        except Exception as e:
            net_check = "Error[200] Model Create Fail."
            println(net_check)
            println(e)

    fclayer = netconf["out"]
    reout = int(model.shape[1]) * int(model.shape[2]) * int(model.shape[3])
    model = tf.reshape(model, [-1, reout])
    println(model)
    W1 = tf.Variable(tf.truncated_normal([reout, fclayer["node_out"]], stddev=0.1))
    model = tf.nn.relu(tf.matmul(model, W1))

    W5 = tf.Variable(tf.truncated_normal([fclayer["node_out"], num_classes], stddev=0.1))
    model = tf.matmul(model, W5)
    println(model)

    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=model, labels=Y))
    optimizer = tf.train.AdamOptimizer(learning_rate=learnrate).minimize(cost, global_step=global_step)
    y_pred_cls = tf.argmax(model, 1)
    check_prediction = tf.equal(y_pred_cls, tf.argmax(Y, 1))
    accuracy = tf.reduce_mean(tf.cast(check_prediction, tf.float32))

    return net_check, model, X, Y, optimizer, y_pred_cls, accuracy, global_step, cost
########################################################################
def get_batch_data(data_set, dataconf, labels, num_classes, type):
    x_size = dataconf["preprocess"]["x_size"]
    y_size = dataconf["preprocess"]["y_size"]
    channel = dataconf["preprocess"]["channel"]

    labelsHot = one_hot_encoded(num_classes)

    label_data_batch = data_set[1]
    img_data_batch = data_set[0]
    y_batch = None
    if type == "T":
        r = 0
        y_batch = np.zeros((len(label_data_batch), num_classes))
        for j in label_data_batch:
            j = j.decode('UTF-8')
            k = labels.index(j)
            y_batch[r] = labelsHot[k]
            r += 1
    else:
        y_batch = []
        for j in label_data_batch:
            j = j.decode('UTF-8')
            y_batch.append(j)

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
    epoch = netconf["param"]["epoch"]
    batchsize = netconf["param"]["batch_size"]
    num_classes = netconf["config"]["num_classes"]
    labels = netconf["labels"]
    g_total_cnt = 0
    try:
        return_arr = []
        while (input_data.has_next()):
            for i in range(epoch):
                for i in range(0, input_data.size(), batchsize):
                    data_set = input_data[i:i + batchsize]
                    x_batch, y_batch = get_batch_data(data_set, dataconf, labels, num_classes, "T")
                    return_data, g_total_cnt = train_run(x_batch, y_batch, netconf, X, Y, optimizer, accuracy, global_step, return_arr, g_total_cnt)
            input_data.next()
    except Exception as e:
        net_check = "Error[400] .............................................."
        println(net_check)
        println(e)

    return_data = return_arr
    return return_data
def train_run(x_batch, y_batch, netconf, X, Y, optimizer, accuracy, global_step, return_arr, g_total_cnt):
    modelname = netconf["modelname"]
    train_cnt = netconf["param"]["traincnt"]
    model_path = netconf["modelpath"]
    save_path = model_path + "/" + modelname
    result = ["Trainning ................................................."]
    return_arr.append(result)
    with tf.Session() as sess:
        try:
            last_chk_path = tf.train.latest_checkpoint(checkpoint_dir=model_path)
            saver = tf.train.Saver()
            saver.restore(sess, save_path=last_chk_path)
            println("Train Restored checkpoint from:" + last_chk_path)
        except:
            println("None to restore checkpoint. Initializing variables instead.")
            sess.run(tf.initialize_all_variables())

        for i in range(train_cnt):
            feed_dict_train = {X: x_batch, Y: y_batch}

            i_global, _ = sess.run([global_step, optimizer], feed_dict=feed_dict_train)
            g_total_cnt += 1
            println("Train Count="+str(g_total_cnt))
            # Print status to screen every 10 iterations (and last).
            if (i_global % 10 == 0) or (i == train_cnt - 1):
                # Calculate the accuracy on the training-batch.
                batch_acc = sess.run(accuracy, feed_dict=feed_dict_train)
                msg = "Global Step: {0:>6}, Training Batch Accuracy: {1:>6.1%}"
                print(msg.format(i_global, batch_acc))
                batch_acc = round(batch_acc*100,2)
                result = ["Global Step:     "+str(i_global)+", Training Batch Accuracy:  "+str(batch_acc)+"%"]
                return_arr.append(result)

            # Save a checkpoint to disk every 100 iterations (and last).
            if (i_global % 100 == 0) or (i == train_cnt - 1):
                model_checkpoint_path = saver.save(sess, save_path=save_path, global_step=global_step)
                model_file_delete(model_path, modelname)

    result = ''
    return_arr.append(result)

    return return_arr, g_total_cnt
########################################################################
def eval_cnn(input_data, netconf, dataconf, X, Y, optimizer, accuracy, model, y_pred_cls, global_step, eval_data):
    batchsize = netconf["param"]["batch_size"]
    num_classes = netconf["config"]["num_classes"]

    labels = netconf["labels"]
    t_cnt_arr = []
    f_cnt_arr = []
    for i in range(len(labels)):
        t_cnt_arr.append(0)
        f_cnt_arr.append(0)

    while (input_data.has_next()):
        for i in range(0, input_data.size(), batchsize):
            data_set = input_data[i:i + batchsize]
            x_batch, y_batch = get_batch_data(data_set, dataconf, labels, num_classes, "E")
            t_cnt_arr, f_cnt_arr, eval_data = eval_run(x_batch, y_batch, netconf, X, Y, accuracy, model, y_pred_cls, labels, global_step, t_cnt_arr, f_cnt_arr, eval_data)
        input_data.next()

    println("####################################################################################################")
    result = []
    strResult = "['Eval ......................................................']"
    result.append(strResult)
    totCnt = 0
    tCnt = 0
    fCnt = 0
    for i in range(len(labels)):
        strResult  = "Category : " + spaceprint(labels[i], 15)+" "
        strResult += "TotalCnt=" + spaceprint(str(t_cnt_arr[i] + f_cnt_arr[i]), 8)+" "
        strResult += "TrueCnt=" + spaceprint(str(t_cnt_arr[i]), 8)+" "
        strResult += "FalseCnt=" + spaceprint(str(f_cnt_arr[i]), 8)+" "
        if t_cnt_arr[i] + f_cnt_arr[i] != 0:
            strResult += "True Percent(TrueCnt/TotalCnt*100)=" + str(round(t_cnt_arr[i] / (t_cnt_arr[i] + f_cnt_arr[i]) * 100)) + "%"
        totCnt += t_cnt_arr[i] + f_cnt_arr[i]
        tCnt += t_cnt_arr[i]
        fCnt += f_cnt_arr[i]
        println(strResult)
        result.append(strResult)

    strResult = "Total Category="+spaceprint(str(len(labels)), 11)+" "
    strResult += "TotalCnt="+spaceprint(str(totCnt), 8)+" "
    strResult += "TrueCnt="+spaceprint(str(tCnt), 8)+" "
    strResult += "FalseCnt="+spaceprint(str(fCnt), 8)+" "
    if totCnt != 0:
        strResult += "True Percent(TrueCnt/TotalCnt*100)="+ str(round(tCnt / totCnt * 100)) + "%"

    result.append(strResult)
    # println(result)
    return_arr = result
    println("###################################################################################################")
    return return_arr, eval_data

def eval_run(x_batch, y_batch, netconf, X, Y, accuracy, model, y_pred_cls, labels, global_step, t_cnt_arr, f_cnt_arr, eval_data):
    model_path = netconf["modelpath"]
    with tf.Session() as sess:
        try:
            sess.run(tf.initialize_all_variables())
            last_chk_path = tf.train.latest_checkpoint(checkpoint_dir=model_path)
            saver = tf.train.Saver()

            saver.restore(sess, save_path=last_chk_path)
            println("Eval Restored checkpoint from:" + last_chk_path)

            # acc = sess.run(accuracy, feed_dict={X: x_batch, Y: y_batch})
            # println(acc)
            logits, y_pred_true = sess.run([model, y_pred_cls], feed_dict={X: x_batch})
            # println(logits)
            # println(y_pred_true)
            for i in range(len(logits)):
                true_name = y_batch[i]
                pred_name = labels[y_pred_true[i]]
                print("True Category=" + true_name + " Predict Category=" + pred_name)
                idx = labels.index(true_name)
                if true_name == pred_name:
                    t_cnt_arr[idx] = t_cnt_arr[idx] + 1
                else:
                    f_cnt_arr[idx] = f_cnt_arr[idx] + 1

                eval_data.set_result_info(true_name, pred_name)
        except Exception as e:
            println(e)
            println("None to restore checkpoint. Initializing variables instead.")
    return t_cnt_arr, f_cnt_arr, eval_data
########################################################################
def predict_run(filelist, netconf, dataconf, model, y_pred_cls, X):
    x_size = dataconf["preprocess"]["x_size"]
    y_size = dataconf["preprocess"]["y_size"]
    channel = dataconf["preprocess"]["channel"]
    pred_cnt = netconf["param"]["predictcnt"]
    model_path = netconf["modelpath"]

    filelist = sorted(filelist.items(), key=operator.itemgetter(0))

    data = {}
    labels = netconf["labels"]

    with tf.Session() as sess:
        try:
            last_chk_path = tf.train.latest_checkpoint(checkpoint_dir=model_path)
            saverss = tf.train.Saver()
            saverss.restore(sess, save_path=last_chk_path)
            println("Predict Restored checkpoint from:" + last_chk_path)

            for file in filelist:
                # println(file)
                value = file[1]
                filename = file[1].name

                for image in value.chunks():
                    # decoded_image = tf.image.decode_jpeg(chunk, channels=channel)
                    # resized_image = tf.image.resize_images(decoded_image, [x_size, y_size])
                    # resized_image = tf.cast(resized_image, tf.uint8)

                    # decoded_image = tf.image.decode_image(contents=image, channels=channel, name="img")
                    # resized_image = tf.image.resize_image_with_crop_or_pad(decoded_image, x_size, y_size)
                    # image = sess.run(resized_image)

                    image = Image.open(io.BytesIO(image))
                    image = image.resize((x_size, y_size), Image.ANTIALIAS)
                    image = np.array(image)
                    image = image.reshape([-1, x_size, y_size, channel])

                    try:
                        logits, y_pred_true = sess.run([model, y_pred_cls], feed_dict={X: image})
                        println(logits)
                        # println(y_pred_true)
                        # cls_name = labels[y_pred_true[0]]
                        # println(cls_name)

                        one = np.zeros((len(labels), 2))

                        for i in range(len(labels)):
                            one[i][0] = i
                            one[i][1] = logits[0][i]

                        onesort = sorted(one, key=operator.itemgetter(1, 0), reverse=True)
                        # println("############################################")
                        # println(onesort)
                        println("filename=" + filename + " predict=" + labels[int(onesort[0][0])])
                        # println(onesort)
                        data_sub = {}
                        data_sub_key = []
                        data_sub_val = []
                        for i in range(pred_cnt):
                            data_sub_key.append(labels[int(onesort[i][0])])
                            data_sub_val.append(round(onesort[i][1],5))
                        data_sub["key"] = data_sub_key
                        data_sub["val"] = data_sub_val
                        data[filename] = data_sub
                        # # println(file)
                        # println(data_sub)
                    except:
                        data_sub = {}
                        data_sub_key = []
                        data_sub_val = []
                        for i in range(pred_cnt):
                            data_sub_key.append(labels[int(onesort[i][0])])
                            data_sub_val.append(round(onesort[i][1], 5))
                        data_sub["key"] = data_sub_key
                        data_sub["val"] = data_sub_val
                        data[filename] = data_sub

        except Exception as e:
            println("None to restore checkpoint. Initializing variables instead.")
            println(e)
    return data

class NeuralNetNodeCnn(NeuralNetNode):
    """
    """
    def _init_node_parm(self, node_id):
        self.net_check = None
        self.model = None
        self.X = None
        self.Y = None
        self.optimizer = None
        self.y_pred_cls = None
        self.accuracy = None
        self.global_step = None

    def _set_progress_state(self):
        return None

    def run(self, conf_data):
        println("run NeuralNetNodeCnn Train")
        # println(conf_data)
        nn_id = conf_data['nn_id']
        wfver = conf_data['wf_ver']
        node = self.get_node_def()
        node_id = conf_data['node_id']
        self._init_node_parm(node_id)

        netconf = WorkFlowNetConfCNN().get_view_obj(node_id)

        feed_node = self.get_prev_node()
        return_data = {}
        return_arr = None
        for feed in feed_node:
            feed_name = feed.get_node_name()
            data_node = feed.get_prev_node()
            for data in data_node:
                data_name = data.get_node_name()
                ################################################################
                dataconf = WorkFlowNetConfCNN().get_view_obj(data_name)
                netconf = WorkFlowNetConfCNN().set_num_classes_predcnt(nn_id, wfver, node, node_id, netconf)

                net_check, model, X, Y, optimizer, y_pred_cls, accuracy, global_step, cost = get_model(netconf, dataconf, "T")

                self.net_check = net_check
                self.model = model
                self.X = X
                self.Y = Y
                self.optimizer = optimizer
                self.y_pred_cls = y_pred_cls
                self.accuracy = accuracy
                self.global_step = global_step

                if net_check == "S":
                    cls_pool = conf_data['cls_pool']
                    input_data = cls_pool[feed_name]
                    return_arr = train_cnn(input_data, netconf, dataconf, X, Y, optimizer, accuracy, global_step)
                else:
                    println("net_check=" + net_check)
        return_data["TrainResult"] = return_arr

        return return_data

    def eval(self, node_id, conf_data, data=None, result=None):
    # def predict(self, node_id, filelist):
        println("run NeuralNetNodeCnn eval")
        # println(conf_data)
        node_id = conf_data['node_id']
        # return
        return_data = {}
        netconf_node_id = self.get_node_name()
        feed_node = self.get_prev_node()

        for feed in feed_node:
            feed_name = feed.get_node_name()
            data_node = feed.get_prev_node()
            for data in data_node:
                data_name = data.get_node_name()
                ###############################################################
                netconf = WorkFlowNetConfCNN().get_view_obj(netconf_node_id)
                dataconf = WorkFlowNetConfCNN().get_view_obj(data_name)

                config = {"type": netconf["config"]["type"], "labels": netconf["labels"]}
                eval_data = TrainSummaryInfo(conf=config)
                eval_data.set_nn_id(conf_data["nn_id"])
                eval_data.set_nn_wf_ver_id(conf_data["wf_ver"])

                if self.net_check == "S":
                    cls_pool = conf_data['cls_pool']
                    net_node_name = self._get_backward_node_with_type(conf_data['node_id'], 'preprocess')
                    for data_name in net_node_name:
                        if data_name.find("eval") > 0:
                            input_data = cls_pool[data_name]
                            return_arr, eval_data = eval_cnn(input_data, netconf, dataconf, self.X, self.Y, self.optimizer, self.accuracy, self.model, self.y_pred_cls, self.global_step, eval_data)
                else:
                    println("net_check=" + self.net_check)

        return eval_data

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

        net_check, model, X, Y, optimizer, y_pred_cls, accuracy, global_step, cost = get_model(netconf, dataconf, "P")

        self.net_check = net_check
        self.model = model
        self.X = X
        self.Y = Y
        self.optimizer = optimizer
        self.y_pred_cls = y_pred_cls
        self.accuracy = accuracy
        self.global_step = global_step

        if net_check == "S":
            data = predict_run(filelist, netconf, dataconf, model, y_pred_cls, X)
        else:
            println("net_check=" + net_check)

        return data



