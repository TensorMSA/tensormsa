from cluster.neuralnet.neuralnet_node import NeuralNetNode
from common.utils import *
from master.workflow.netconf.workflow_netconf_cnn import WorkFlowNetConfCNN
import tensorflow as tf
import time
import numpy as np
from datetime import timedelta
from cluster.data.data_node_image import DataNodeImage
import os
########################################################################
# nm_classes = label cnt or max label cnt
def one_hot_encoded(num_classes):
    one = np.zeros((num_classes, num_classes))

    for i in range(num_classes):
        for j in range(num_classes):
            if i == j:
                one[i][j] = 1
    return one
########################################################################
def model_file_delete(model_path, save_name):
    existcnt = 10
    filelist = os.listdir(model_path)
    print(filelist)
    flist = []
    for i in filelist:
        i = i.replace(save_name + "-", "")
        dotidx = i.find(".")
        if dotidx > -1:
            i = i[:dotidx]
            try:
                flist.append(int(i))
            except:
                None
    flist.sort()

    j = len(flist) - 1
    for i in range(len(flist)):
        if i > existcnt * 3:
            fname = save_name + "-" + str(flist[j])

            for file in filelist:
                print(fname, file)
                fidx = file.find(fname)
                if fidx > -1:
                    if os.path.isfile(model_path + "/" + file):
                        os.remove(model_path + "/" + file)
        j -= 1
########################################################################
def get_model(self, netconf, X, num_classes):
    net_check = "S"
    stopper = 1
    L1 = X
    try:
        while True:
            try:
                layer = netconf["layer" + str(stopper)]
            except Exception as e:
                if stopper == 1:
                    net_check = "Error[100] .............................................."
                    L1 = "layer is None."
                    return net_check, L1
                break
            println(layer)

            try:
                if str(layer["active"]) == 'relu':
                    activitaion = tf.nn.relu
                elif str(layer["active"]) == 'softmax':
                    activitaion = tf.nn.softmax('float32')
                else:
                    activitaion = tf.nn.relu

                L1 = tf.contrib.layers.conv2d(inputs=L1
                                              , num_outputs=int(layer["node_out"])
                                              , kernel_size=[int((layer["cnnfilter"][0])), int((layer["cnnfilter"][1]))]
                                              , activation_fn=activitaion
                                              , weights_initializer=tf.contrib.layers.xavier_initializer_conv2d()
                                              , padding=str((layer["padding"])))

                L1 = tf.contrib.layers.max_pool2d(inputs=L1
                                                  , kernel_size=[int((layer["maxpoolmatrix"][0])),
                                                                 int((layer["maxpoolmatrix"][1]))]
                                                  , stride=[int((layer["maxpoolstride"][0])),
                                                            int((layer["maxpoolstride"][1]))]
                                                  , padding=str((layer["padding"])))

                if str(layer["droprate"]) is not "":
                    droprate = float((layer["droprate"]))
                else:
                    droprate = 0.0

                if droprate > 0.0:
                    L1 = tf.nn.dropout(L1, droprate)
            except Exception as e:
                net_check = "Error[200] .............................................."
                L1 = e
                return net_check, L1

            stopper += 1
            if (stopper >= 1000):
                break

        fclayer = netconf["out"]

        # 1. softmax
        reout = int(L1.shape[1])*int(L1.shape[2])*int(L1.shape[3])
        L1 = tf.reshape(L1, [-1, reout])
        W1 = tf.Variable(tf.truncated_normal([reout, fclayer["node_out"]], stddev=0.1))
        L1 = tf.nn.relu(tf.matmul(L1, W1))
        W5 = tf.Variable(tf.truncated_normal([fclayer["node_out"], num_classes], stddev=0.1))
        L1 = tf.matmul(L1, W5)

        #     # # 2. tf.contrib.layers.fully_connected
        #     L1 = tf.contrib.layers.flatten(L1)
        #     L1 = tf.contrib.layers.fully_connected(L1, fclayer["node_out"],
        #                                            normalizer_fn=tf.contrib.layers.batch_norm)
        #     L1 = tf.contrib.layers.fully_connected(L1, num_classes)

        println(L1)

    except Exception as e:
        net_check = "Error[300] .............................................."
        println(net_check)
        println(e)
        L1 = e

    return net_check, L1
########################################################################
def train(input_data, L1, X, Y, netconf, dataconf):
    x_size = dataconf["preprocess"]["x_size"]
    y_size = dataconf["preprocess"]["y_size"]
    channel = dataconf["preprocess"]["channel"]
    labelsDict = dataconf["labels"]

    num_classes = netconf["config"]["num_classes"]
    batchsize = netconf["config"]["batch_size"]
    learnrate = netconf["config"]["learnrate"]

    start_time = time.time()
    global_step = tf.Variable(initial_value=10, name='global_step', trainable=False)

    try:
        cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=L1, labels=Y))
        # optimizer = tf.train.AdamOptimizer(learnrate).minimize(cost)
        optimizer = tf.train.AdamOptimizer(learning_rate=learnrate).minimize(cost, global_step=global_step)

        check_prediction = tf.equal(tf.argmax(L1, 1), tf.argmax(Y, 1))
        accuracy = tf.reduce_mean(tf.cast(check_prediction, tf.float32))
        ################################################################ Label
        # println("Label Dict //////////////////////////////////////////////////")
        labelsDictHot = one_hot_encoded(num_classes)
        # println(labelsDict)
        # println(labelsDictHot)
        ################################################################ Image Label
        for data in input_data:
            # println("File //////////////////////////////////////////////////////")
            # println(data)
            labels_data = data['targets']
            img_data = data['image_features']

            for i in range(0, img_data.len(), batchsize):
                label_data_batch = labels_data[i:i + batchsize]
                img_data_batch = img_data[i:i + batchsize]

                y_batch = np.zeros((len(label_data_batch), num_classes))
                r = 0
                for j in label_data_batch:
                    j = j.decode('UTF-8')
                    k = labelsDict.index(j)
                    y_batch[r] = labelsDictHot[k]
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
                train_run(x_batch, y_batch, netconf, dataconf, X, Y, optimizer, accuracy, global_step)

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
########################################################################
def train_run(x_batch, y_batch, netconf, dataconf, X, Y, optimizer, accuracy, global_step):
    save_name = "model"
    train_cnt = netconf["config"]["traincnt"]
    # println(netconf["key"]["nn_id"])
    # println(netconf["key"]["wf_ver_id"])
    model_path = get_model_path(netconf["key"]["nn_id"], netconf["key"]["wf_ver_id"], "cnnmodel")
    # println(model_path)
    saver = tf.train.Saver()
    with tf.Session() as sess:
        try:
            last_chk_path = tf.train.latest_checkpoint(checkpoint_dir=model_path)
            saver.restore(sess, save_path=last_chk_path)
            println("Restored checkpoint from:" + last_chk_path)
        except:
            println("None to restore checkpoint. Initializing variables instead.")
            sess.run(tf.initialize_all_variables())

        for i in range(train_cnt):
            feed_dict_train = {X: x_batch, Y: y_batch}
            # sess.run(optimizer, feed_dict=feed_dict_train)
            i_global, _ = sess.run([global_step, optimizer],
                                      feed_dict=feed_dict_train)

            # Print status to screen every 10 iterations (and last).
            if (i_global % 10 == 0) or (i == train_cnt - 1):
                # Calculate the accuracy on the training-batch.
                batch_acc = sess.run(accuracy, feed_dict=feed_dict_train)

                # Print status.
                msg = "Global Step: {0:>6}, Training Batch Accuracy: {1:>6.1%}"
                println(msg.format(i_global, batch_acc))

            # Save a checkpoint to disk every 100 iterations (and last).
            if (i_global % 100 == 0) or (i == train_cnt - 1):
                println("Save model_path=" + model_path)
                saver.save(sess,
                           save_path=model_path+"/"+save_name,
                           global_step=global_step)

    model_file_delete(model_path, save_name)
    println("Saved checkpoint.")
########################################################################
class NeuralNetNodeCnn(NeuralNetNode):
    """
    """
    def run(self, conf_data):
        println("run NeuralNetNodeCnn")
        println(conf_data)
        ################################################################
        # search nn_node_info
        dataconf = WorkFlowNetConfCNN().get_view_obj(str(conf_data["node_list"][0]))
        netconf = WorkFlowNetConfCNN().get_view_obj(str(conf_data["node_list"][1]))

        x_size  = dataconf["preprocess"]["x_size"]
        y_size  = dataconf["preprocess"]["y_size"]
        channel = dataconf["preprocess"]["channel"]
        num_classes = netconf["config"]["num_classes"]

        ################################################################
        X = tf.placeholder(tf.float32, shape=[None, x_size, y_size, channel], name='x')
        Y = tf.placeholder(tf.float32, shape=[None, num_classes], name='y')
        ################################################################
        node_id = str(conf_data["node_list"][0])
        input_data = DataNodeImage().load_train_data(node_id)

        netcheck, model = get_model(self, netconf, X, num_classes)
        if netcheck == "S":
            train(input_data, model, X, Y, netconf, dataconf)
        else:
            println("net_check=" + netcheck)

        println("train end......")
        return None

    def _init_node_parm(self, node_id):
        return None

    def _set_progress_state(self):
        return None

