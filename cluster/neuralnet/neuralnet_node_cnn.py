from cluster.neuralnet.neuralnet_node import NeuralNetNode
from common.utils import *
from master.workflow.netconf.workflow_netconf_cnn import WorkFlowNetConfCNN
import tensorflow as tf
import time
import numpy as np
from datetime import timedelta

def get_training_data(self, dataconf):
    println(dataconf)
    train_data_set = None
    train_label_set = None
    println("Start Down OK....")

    println("End Down OK....")

    return train_data_set, train_label_set

def get_model(self, netconf, dataconf):
    # println(netconf)
    x_size = dataconf["preprocess"]["x_size"]
    y_size = dataconf["preprocess"]["y_size"]
    num_classes = 8

    X = tf.placeholder(tf.float32, shape=[None, x_size, y_size, 3], name='x')
    Y = tf.placeholder(tf.float32, shape=[None, num_classes], name='y')
    ################################################################
    L1 = X
    stopper = 1
    net_check = "S"

    while True:
        try:
            layer = netconf["layer"+str(stopper)]
        except Exception as e:
            if stopper == 1:
                net_check = "Error[100] .............................................."
                L1 = "layer is None."
                return net_check, L1
            break
        println(layer)
        # println("num_outputs=" + str(layer["node_in_out"][1]))
        # println("cnnfilter=" + str(layer["cnnfilter"]))
        # println("active=" + str(layer["active"]))
        # println("maxpoolmatrix=" + str(layer["maxpoolmatrix"]))

        try:
            if str(layer["active"]) == 'relu':
                activitaion = tf.nn.relu
            elif str(layer["active"]) == 'softmax':
                activitaion = tf.nn.softmax('float32')
            else:
                activitaion = tf.nn.relu

            L1 = tf.contrib.layers.conv2d(inputs = L1
                                          , num_outputs = int(layer["node_out"])
                                          , kernel_size = [int((layer["cnnfilter"][0])), int((layer["cnnfilter"][1]))]
                                          , activation_fn = activitaion
                                          , weights_initializer=tf.contrib.layers.xavier_initializer_conv2d()
                                          , padding=str((layer["padding"])) )

            L1 = tf.contrib.layers.max_pool2d(inputs=L1
                                              , kernel_size = [int((layer["maxpoolmatrix"][0])), int((layer["maxpoolmatrix"][1]))]
                                              , stride = [int((layer["maxpoolstride"][0])), int((layer["maxpoolstride"][1]))]
                                              , padding=str((layer["padding"])) )

            if str(layer["droprate"]) is not "":
                droprate = float((layer["droprate"]))
            else:
                droprate = 0.0

            if droprate > 0.0:
                # println("droprate="+str(droprate))
                L1 = tf.nn.dropout(L1, droprate)
        except Exception as e:
            net_check = "Error[200] .............................................."
            L1 = e
            return net_check, L1

        stopper += 1
        if (stopper >= 1000):
            break
    try:
        fclayer = netconf["out"]
        println(fclayer)
        println(L1)

        # 1. softmax
        reout = int(L1.shape[1])*int(L1.shape[2])*int(L1.shape[3])
        L1 = tf.reshape(L1, [-1, reout])
        W1 = tf.Variable(tf.truncated_normal([reout, fclayer["node_out"]], stddev=0.1))
        L1 = tf.nn.relu(tf.matmul(L1, W1))
        W5 = tf.Variable(tf.truncated_normal([fclayer["node_out"], num_classes], stddev=0.1))
        L1 = tf.matmul(L1, W5)
        Yresult = tf.nn.softmax(L1)
        cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=L1, labels=Y))


        # # # 2. tf.contrib.layers.fully_connected
        # L1 = tf.contrib.layers.flatten(L1)
        # L1 = tf.contrib.layers.fully_connected(L1, fclayer["node_out"],
        #                                        normalizer_fn=tf.contrib.layers.batch_norm)
        # L1 = tf.contrib.layers.fully_connected(L1, num_classes)
        # cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=L1, labels=Y))
        # println(cost)
        # println(Yresult)

        # Define loss and optimizer
        train_op = tf.train.AdamOptimizer(1e-4).minimize(cost)
        correct_prediction = tf.equal(tf.argmax(Yresult, 1), tf.argmax(Y, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

        println("soft end")

    except Exception as e:
        net_check = "Error[300] .............................................."
        L1 = e

    return net_check, L1, X, Y, train_op, accuracy

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

def train(train_data_set, train_label_set, model, accuracy, netconf, X, Y):
    println("train start .....")
    _train_cnt = 5
    model_path = get_model_path(netconf["key"]["nn_id"], netconf["key"]["wf_ver_id"], "cnnmodel")
    global_step = tf.Variable(initial_value=10, name='global_step', trainable=False)
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
            println("Restored checkpoint from:", last_chk_path)
        except:
            # If the above failed for some reason, simply
            # initialize all the variables for the TensorFlow graph.
            println("None to restore checkpoint. Initializing variables instead.")
            sess.run(tf.initialize_all_variables())

        ################################################################
        println("Train Optimize Call:", _train_cnt)

        start_time = time.time()

        for i in range(_train_cnt):
            # Get a batch of training examples.
            # x_batch now holds a batch of images and
            # y_true_batch are the true labels for those images.
            x_batch, y_true_batch = random_batch(train_data_set, train_label_set)

            # Put the batch into a dict with the proper names
            # for placeholder variables in the TensorFlow graph.
            feed_dict_train = {X: x_batch,
                               Y: y_true_batch}

            # Run the optimizer using this batch of training data.
            # TensorFlow assigns the variables in feed_dict_train
            # to the placeholder variables and then runs the optimizer.
            # We also want to retrieve the global_step counter.
            i_global, _ = sess.run([global_step, model],
                                      feed_dict=feed_dict_train)

            # Print status to screen every 100 iterations (and last).
            if (i_global % 100 == 0) or (i == _train_cnt - 1):
                # Calculate the accuracy on the training-batch.
                batch_acc = sess.run(accuracy,
                                        feed_dict=feed_dict_train)

                # Print status.
                msg = "Global Step: {0:>6}, Training Batch Accuracy: {1:>6.1%}"
                println(msg.format(i_global, batch_acc))

            # Save a checkpoint to disk every 1000 iterations (and last).
            if (i_global % 1000 == 0) or (i == _train_cnt - 1):
                # Save all variables of the TensorFlow graph to a
                # checkpoint. Append the global_step counter
                # to the filename so we save the last several checkpoints.
                saver.save(sess,
                           save_path=model_path + "check",
                           global_step=global_step)

                println("Saved checkpoint.")

        # Ending time.
        end_time = time.time()

        # Difference between start and end-times.
        time_dif = end_time - start_time

        # Print the time-usage.
        println("Time usage: " + str(timedelta(seconds=int(round(time_dif)))))

class NeuralNetNodeCnn(NeuralNetNode):
    """

    """
    def load_training_data(self):
        train_data_set = None
        train_label_set = None
        return train_data_set, train_label_set

    def run(self, conf_data):
        println("run NeuralNetNodeCnn")
        println(conf_data)
        ################################################################
        # search nn_node_info
        dataconf = WorkFlowNetConfCNN().get_view_obj(str(conf_data["node_list"][0]))
        netconf = WorkFlowNetConfCNN().get_view_obj(str(conf_data["node_list"][1]))

        train_data_set, train_label_set = get_training_data(self, dataconf)
        netcheck, model, X, Y, train_op, accuracy = get_model(self, netconf, dataconf)
        train(train_data_set, train_label_set, model, accuracy, netconf, X, Y)
        println("net_check=" + netcheck)
        println(model)






        # optimizer = tf.train.AdamOptimizer(0.001).minimize(cost)

        return None

    def _init_node_parm(self, node_id):
        return None

    def _set_progress_state(self):
        return None

