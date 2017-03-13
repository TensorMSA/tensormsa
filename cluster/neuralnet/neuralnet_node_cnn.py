from cluster.neuralnet.neuralnet_node import NeuralNetNode
from common.utils import *
from master.workflow.netconf.workflow_netconf_cnn import WorkFlowNetConfCNN
import tensorflow as tf
import time
import numpy as np
from datetime import timedelta
########################################################################
def get_training_data(self, dataconf):
    println(dataconf)
    train_data_set = None
    train_label_set = None
    println("Start Down OK....")
    from tensorflow.contrib.learn.python.learn.datasets.mnist import read_data_sets
    tf.set_random_seed(0)

    mnist = read_data_sets("data", one_hot=True, reshape=False, validation_size=0)

    train_data_set = mnist.test.images
    train_label_set = mnist.test.labels
    println("End Down OK....")

    return train_data_set, train_label_set
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
# Train
def random_batch(images_train, labels_train):
    # Number of images in the training-set.
    num_images = len(images_train)

    # Create a random index.
    idx = np.random.choice(num_images,
                           size=1000,
                           replace=False)

    # Use the random index to select random images and labels.
    x_batch = images_train[idx, :, :, :]
    y_batch = labels_train[idx, :]

    return x_batch, y_batch
########################################################################
def train(train_data_set, train_label_set, L1, X, Y, train_cnt, model_path):

    try:
        cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=L1, labels=Y))
        optimizer = tf.train.AdamOptimizer(0.001).minimize(cost)

        check_prediction = tf.equal(tf.argmax(L1, 1), tf.argmax(Y, 1))
        accuracy = tf.reduce_mean(tf.cast(check_prediction, tf.float32))

        # global_step = tf.Variable(initial_value=10, name='global_step', trainable=False)
        saver = tf.train.Saver()

        with tf.Session() as sess:
            try:
                println("Trying to restore last checkpoint SavePath : " + model_path)
                # Use TensorFlow to find the latest checkpoint - if any.
                last_chk_path = tf.train.latest_checkpoint(checkpoint_dir=model_path)
                println("Try and load the data in the checkpoint: : " + str(last_chk_path))
                # Try and load the data in the checkpoint.
                saver.restore(sess, save_path=last_chk_path)
                # If we get to this point, the checkpoint was successfully loaded.
                println("Restored checkpoint from:"+ last_chk_path)
            except:
                # If the above failed for some reason, simply
                # initialize all the variables for the TensorFlow graph.
                println("None to restore checkpoint. Initializing variables instead.")
                sess.run(tf.initialize_all_variables())

            ################################################################
            println("Train Optimize Call:"+ str(train_cnt))

            start_time = time.time()

            for i in range(train_cnt):
                x_batch, y_true_batch = random_batch(train_data_set, train_label_set)
                feed_dict_train = {X: x_batch,Y: y_true_batch}
                # i_global, _ = sess.run([global_step, optimizer],feed_dict=feed_dict_train)
                sess.run(optimizer, feed_dict=feed_dict_train)

                # Print status to screen every 100 iterations (and last).
                if (i % 1 == 0) or (i == train_cnt - 1):
                    # Calculate the accuracy on the training-batch.
                    batch_acc = sess.run(accuracy, feed_dict=feed_dict_train)

                    # Print status.
                    msg = "Global Step: {0:>6}, Training Batch Accuracy: {1:>6.1%}"
                    println(msg.format(i, batch_acc))

                # Save a checkpoint to disk every 1000 iterations (and last).
                if (i % 10 == 0) or (i == train_cnt - 1):
                    println("Save model_path="+model_path + "check")
                    saver.save(sess,
                               save_path=model_path,
                               global_step=i)

        println("Saved checkpoint.")
    except Exception as e:
        net_check = "Error[400] .............................................."
        println(net_check)
        println(e)
        L1 = e

    # Ending time.
    end_time = time.time()

    # Difference between start and end-times.
    time_dif = end_time - start_time

    # Print the time-usage.
    println("Time usage: " + str(timedelta(seconds=int(round(time_dif)))))
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
        model_path = get_model_path(netconf["key"]["nn_id"], netconf["key"]["wf_ver_id"], "cnnmodel")

        x_size = dataconf["preprocess"]["x_size"]
        y_size = dataconf["preprocess"]["y_size"]
        train_cnt = int(netconf["config"]["epoch"])

        num_classes = 10
        x_size = 28  # MNIST 이미지의 가로 크기
        y_size = 28  # MNIST 이미지의 세로 크기
        color = 1
        train_cnt = 12

        X = tf.placeholder(tf.float32, shape=[None, x_size, y_size, color], name='x')
        Y = tf.placeholder(tf.float32, shape=[None, num_classes], name='y')
        println("1......")
        ################################################################
        train_data_set, train_label_set = get_training_data(self, dataconf)
        netcheck, model = get_model(self, netconf, X, num_classes)
        if netcheck == "S":
            train(train_data_set, train_label_set, model, X, Y, train_cnt, model_path)
        else:
            println("net_check=" + netcheck)

        return None

    def _init_node_parm(self, node_id):
        return None

    def _set_progress_state(self):
        return None

