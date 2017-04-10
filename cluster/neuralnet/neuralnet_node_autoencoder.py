from cluster.neuralnet.neuralnet_node import NeuralNetNode
from master.workflow.netconf.workflow_netconf_autoencoder import WorkFlowNetConfAutoEncoder
import tensorflow as tf
import numpy as np
from PIL import Image

class NeuralNetNodeAutoEncoder(NeuralNetNode):
    """

    """

    def run(self, conf_data):
        try:

            learning_rate = 0.01
            training_epoch = 20
            batch_size = 100

            n_hidden = 256
            n_input = 30000 #460 * 321

            #im = Image.open(value)
            #image = np.array(DataNodeImage()._resize_file_image(im, preprocess))

            # init parms
            self._init_node_parm(conf_data['node_id'])
            self.cls_pool = conf_data['cls_pool']

            data_node_name = self._get_backward_node_with_type(conf_data['node_id'], 'preprocess')
            train_data_set = self.cls_pool[data_node_name[0]]

            X = tf.placeholder(tf.float32, shape=[None, 30000], name='x')

            #X = tf.placeholder(tf.float32, [None, n_input])
            W_encode = tf.Variable(tf.random_normal([n_input, n_hidden]))
            b_encode = tf.Variable(tf.random_normal([n_hidden]))

            W_decode = tf.Variable(tf.random_normal([n_hidden, n_input]))
            b_decode = tf.Variable(tf.random_normal([n_input]))

            encoder = tf.nn.sigmoid(
                tf.add(tf.matmul(X, W_encode), b_encode))

            decoder = tf.nn.sigmoid(
                tf.add(tf.matmul(encoder, W_decode), b_decode))

            Y = X

            cost = tf.reduce_mean(tf.pow(Y - decoder, 2))
            optimizer = tf.train.RMSPropOptimizer(learning_rate).minimize(cost)

            init = tf.global_variables_initializer()
            sess = tf.Session()
            sess.run(init)

            # total_batch = int(data_set.train.num_examples / batch_size)
            total_batch = 1


            while (train_data_set.has_next()):
                for i in range(0, train_data_set.data_size(), batch_size):
                    data_set = train_data_set[i:i + batch_size]
                    img_data_batch = data_set[0]
                    x_batch = np.zeros((len(img_data_batch), len(img_data_batch[0])))
                    r = 0
                    for j in img_data_batch:
                        j = j.tolist()
                        x_batch[r] = j
                        r += 1
                    _, cost_val = sess.run([optimizer, cost], feed_dict={X: x_batch})
                train_data_set.next()



            #x_batch = np.reshape(x_batch, 30000)

            for epoch in range(training_epoch):
                total_cost = 0
                for i in range(total_batch):
                    # data_set = input_data[i:i + batch_size]
                    #x_batch, y_batch = get_batch_data(data_set, dataconf, num_classes, "T")

                    #batch_xs = np.array(data_set)
                    # batch_xs, batch_ys = data_set.train.next_batch(batch_size)

                    _, cost_val = sess.run([optimizer, cost], feed_dict={X: x_batch})
                    total_cost += cost_val
                print('Epoch:', '%04d' % (epoch + 1), 'Avg. cost =', '{:.6f}'.format(total_cost / total_batch))
            return None

        except Exception as e:
            raise Exception(e)

    def _init_node_parm(self, node_id):
        wf_conf = WorkFlowNetConfAutoEncoder(node_id)

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