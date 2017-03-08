from cluster.neuralnet.neuralnet_node import NeuralNetNode
from common.utils import *
from master.workflow.netconf.workflow_netconf_cnn import WorkFlowNetConfCNN
import tensorflow as tf

def get_training_data(self, dataconf):
    println(dataconf)
    train_data_set = None
    train_label_set = None
    println("Start Down OK....")

    println("End Down OK....")

    return train_data_set, train_label_set

def get_network_data(self, netconf, dataconf):
    println(netconf)

    x_size = dataconf["preprocess"]["x_size"]
    y_size = dataconf["preprocess"]["y_size"]
    num_classes = 2

    X = tf.placeholder(tf.float32, shape=[None, x_size, y_size, 3], name='x')
    Y = tf.placeholder(tf.float32, shape=[None, num_classes], name='y')

    L1 = X
    stopper = 1
    net_check = "S"
    println("net_check="+net_check)
    while True:
        try:
            layer = netconf["layer"+str(stopper)]
        except Exception as e:
            if stopper == 1:
                net_check = "Error[100] : layer is None."
                return net_check
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

            L2 = tf.contrib.layers.conv2d(inputs = L1
                                          , num_outputs = int(layer["node_in_out"][1])
                                          , kernel_size = [int((layer["cnnfilter"][0])), int((layer["cnnfilter"][1]))]
                                          , activation_fn = activitaion)

            L3 = tf.contrib.layers.max_pool2d(inputs=L2
                                              , kernel_size = [int((layer["maxpoolmatrix"][0])), int((layer["maxpoolmatrix"][1]))]
                                              , stride = [int((layer["maxpoolstride"][0])), int((layer["maxpoolstride"][1]))] )

            if str(layer["droprate"]) is not "":
                droprate = float((layer["droprate"]))
            else:
                droprate = 0.0

            if droprate > 0.0:
                # println("droprate="+str(droprate))
                try:
                    L3 = tf.nn.dropout(L3, droprate)
                except Exception as e:
                    println(e)
            L1 = L3
        except Exception as e:
            net_check = 'Error[200] : '+str(e)
            println(net_check)
            return net_check

        stopper += 1
        if (stopper >= 1000):
            break

    L4 = tf.contrib.layers.flatten(L1)
    L5 = tf.contrib.layers.fully_connected(L4
                                           , 256
                                           , normalizer_fn=tf.contrib.layers.batch_norm)

    model = tf.contrib.layers.fully_connected(L5, num_classes)
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(model, Y))
    optimizer = tf.train.AdamOptimizer(0.001).minimize(cost)
    return net_check


class NeuralNetNodeCnn(NeuralNetNode):
    """

    """
    def load_training_data(self):
        train_data_set = None
        train_label_set = None
        return train_data_set, train_label_set

    def run(self, conf_data):
        println("run NeuralNetNodeCnn")
        node_id = conf_data
        ################################################################
        # search nn_node_info
        dataconf = WorkFlowNetConfCNN().get_view_obj(str(node_id).replace("netconf_node", "data_node"))
        netconf = WorkFlowNetConfCNN().get_view_obj(node_id)
        ################################################################
        train_data_set, train_label_set = get_training_data(self, dataconf)
        netcheck = get_network_data(self, netconf, dataconf)
        println("net_check=" + netcheck)
        return None

    def _init_node_parm(self):
        return None

    def _set_progress_state(self):
        return None

