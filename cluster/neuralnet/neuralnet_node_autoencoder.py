from cluster.neuralnet.neuralnet_node import NeuralNetNode
from master.workflow.netconf.workflow_netconf_autoencoder import WorkFlowNetConfAutoEncoder
import tensorflow as tf
import numpy as np
from common.utils import *

class NeuralNetNodeAutoEncoder(NeuralNetNode):
    """

    """

    def run(self, conf_data):
        try:
            # init parms
            self._init_node_parm(conf_data['node_id'])
            self.cls_pool = conf_data['cls_pool']

            data_node_name = self._get_backward_node_with_type(conf_data['node_id'], 'preprocess')
            train_data_set = self.cls_pool[data_node_name[0]]

            X = tf.placeholder(tf.float32, shape=[None, self.n_input], name='x')

            W_encode = tf.Variable(tf.random_normal([self.n_input, self.n_hidden]))
            b_encode = tf.Variable(tf.random_normal([self.n_hidden]))

            W_decode = tf.Variable(tf.random_normal([self.n_hidden, self.n_input]))
            b_decode = tf.Variable(tf.random_normal([self.n_input]))

            encoder = tf.nn.sigmoid(
                tf.add(tf.matmul(X, W_encode), b_encode))

            decoder = tf.nn.sigmoid(
                tf.add(tf.matmul(encoder, W_decode), b_decode))

            Y = X

            cost = tf.reduce_mean(tf.pow(Y - decoder, 2))
            optimizer = tf.train.RMSPropOptimizer(self.learning_rate).minimize(cost)

            init = tf.global_variables_initializer()
            sess = tf.Session()
            sess.run(init)
            saver = tf.train.Saver(tf.all_variables())
            if (len(get_filepaths(self.md_store_path)) > 0):
                saver.restore(sess, ''.join([self.md_store_path, '/']))

            while (train_data_set.has_next()):
                for i in range(0, train_data_set.data_size(), self.batch_size):
                    data_set = train_data_set[i:i + self.batch_size]
                    img_data_batch = data_set[0]
                    x_batch = np.zeros((len(img_data_batch), len(img_data_batch[0])))
                    r = 0
                    for j in img_data_batch:
                        j = j.tolist()
                        x_batch[r] = j
                        r += 1
                    for epoch in range(self.iter_size):
                        total_cost = 0
                        _, cost_val = sess.run([optimizer, cost], feed_dict={X: x_batch})
                        total_cost += cost_val
                        print('Epoch:', '%04d' % (epoch + 1), 'Avg. cost =', '{:.6f}'.format(total_cost / train_data_set.data_size()))
                train_data_set.next()

            # save model and close session
            saver.save(sess, ''.join([self.md_store_path, '/']))
            # close session
            sess.close()
            return None
        except Exception as e:
            raise Exception(e)

    def _init_node_parm(self, node_id):
        try:
            wf_conf = WorkFlowNetConfAutoEncoder(node_id)
            self.md_store_path = wf_conf.get_model_store_path()
            self.iter_size = wf_conf.get_iter_size()
            self.batch_size = wf_conf.get_batch_size()
            self.learning_rate = wf_conf.get_learn_rate()
            self.n_hidden = wf_conf.get_n_hidden()
            self.n_input = wf_conf.get_n_input()

        except Exception as e :
            raise Exception (e)

    def predict(self, node_id, parm = {"input_data" : {}}):
        """

        :param node_id:
        :param parm:
        :return:
        """
        # set init params
        self._init_node_parm(node_id)

        # prepare net conf
        # create session
        sess = tf.Session()
        sess.run(tf.initialize_all_variables())
        saver = tf.train.Saver(tf.all_variables())
        if (len(get_filepaths(self.md_store_path)) > 0):
            saver.restore(sess, ''.join([self.md_store_path, '/']))
        else:
            raise Exception("error : no pretrained model exist")
        decoder =""
        result = sess.run(decoder, feed_dict={X: parm})
        sess.close()
        return result

    def _set_progress_state(self):
        return None

    def eval(self, node_id, parm={}):
        """

        :param node_id:
        :param parm:
        :return:
        """
        pass