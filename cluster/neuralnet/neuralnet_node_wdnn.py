from cluster.neuralnet.neuralnet_node import NeuralNetNode
from master.workflow.netconf.workflow_netconf_wdnn import WorkFlowNetConfWdnn
from master.workflow.data.workflow_data_frame import WorkFlowDataFrame
import pandas as pd
import tensorflow as tf
import json
import os
from master.workflow.dataconf.workflow_dataconf_frame import WorkflowDataConfFrame
from cluster.common.neural_common_wdnn import NeuralCommonWdnn
from cluster.preprocess.pre_node_feed_fr2wdnn import PreNodeFeedFr2Wdnn
from common import utils
import  tensorflow as tf

class NeuralNetNodeWdnn(NeuralNetNode):
    """

    """

    def run(self, conf_data):
        print("NeuralNetNodeWdnn Run called")
        """
                Wide & Deep Network Training
                :param nnid : network id in tfmsacore_nninfo
                :return: acturacy
        """
        try:
            self._init_node_parm(conf_data['node_id'])

            self.cls_pool = conf_data['cls_pool'] # Data feeder
            # get prev node for load data
            #data_node_name = self._get_backward_node_with_type(conf_data['node_id'], 'preprocess')
            #train_data_set = self.cls_pool[data_node_name[0]]
            # prepare net conf
            #self._set_train_model()


            print("model_path : " + str(self.model_path))
            print("hidden_layers : " + str(self.hidden_layers))
            print("activation_function : " + str(self.activation_function))

            data_store_path = WorkFlowDataFrame(conf_data['nn_id']+"_"+conf_data['wf_ver']+"_"+ "data_node").step_store

            data_conf_info = WorkflowDataConfFrame(conf_data['nn_id']+"_"+conf_data['wf_ver']+"_"+ "dataconf_node").data_conf

            # make wide & deep model
            wdnn = NeuralCommonWdnn()
            wdnn_model = wdnn.wdnn_build('wdnn', conf_data['node_id'],self.hidden_layers,str(self.activation_function),data_conf_info, str(self.model_path))

            #feed

            # get prev node for load data
            data_node_name = self._get_backward_node_with_type(conf_data['node_id'], 'preprocess')
            train_data_set = self.cls_pool[data_node_name[0]]
            file_queue  = str(train_data_set.input_paths[0])
            #str(file_queue[0])
            #feed = PreNodeFeedFr2Wdnn()

            #read hdf5
            # try:
            #     #TODO file이 여러개면 어떻하지?
            #     #file_paths = list()
            #     #for file_path in utils.get_filepaths(data_store_path, "tfrecords"):
            #     #    file_paths.append(file_path)
            #
            #
            #     #df = self.read_hdf5(file_paths[0])
            #
            # except Exception as e:
            #     print("Error Message : {0}".format(e))
            #     raise Exception(e)

            #feature, label = wdnn.input_fn( df, conf_data['node_id'],data_conf_info)

            #multi Feeder modified
            wdnn_model.fit(input_fn=lambda: train_data_set.input_fn(tf.contrib.learn.ModeKeys.TRAIN, file_queue,128), steps=200)

            results = wdnn_model.evaluate(input_fn=lambda: train_data_set.input_fn(tf.contrib.learn.ModeKeys.TRAIN, file_queue,128), steps=1)
            for key in sorted(results):
                print("%s: %s" % (key, results[key]))

            #feature_map, target = train_data_set.input_fn(tf.contrib.learn.ModeKeys.TRAIN, file_queue, 128)
            print("end")
            #with tf.Session() as sess:
        except Exception as e:
            print ("Error Message : {0}".format(e))
            raise Exception(e)


        return None

    def read_hdf5_chunk(self,filename):

        # type4 partial read
        store = pd.HDFStore(filename)
        nrows = store.get_storer('table1').nrows
        chunksize = 100

        for i in range(nrows // chunksize + 1):
            chunk = store.select('table1',
                                 start=i * chunksize,
                                 stop=(i + 1) * chunksize)
        store.close()
        return chunk

    def read_hdf5(self,filename):

        store = pd.HDFStore(filename)
        #df = store.get_storer('table1')
        df = store.select('table1')
        store.close()
        return df

    def load_hdf5(data_path, dataframe):
        """
        Load_hdf5
        :param data_path:
        :return:data_path
        """
        store_filepath_name = data_path + "/" + "adult.h5"
        hdf = pd.HDFStore(store_filepath_name)
        hdf.put('table1', dataframe, format='table', data_columns=True)
        hdf.close()

    def _init_node_parm(self, node_id):
        return None

    def _set_progress_state(self):
        return None

    def predict(self, nn_id, conf_data, parm = {}):

        # model build
        #
        # self._init_node_parm(nn_id)

        # data_conf_info = WorkflowDataConfFrame(nn_id + "_" + ver + "_" + "dataconf_node").data_conf
        try:
            node_id = conf_data['node_id']
            netconf = conf_data['net_conf']
            dataconf = conf_data['data_conf']

            # make wide & deep model
            wdnn = NeuralCommonWdnn()
            # wdnn_model = wdnn.wdnn_predict_build('wdnn', nn_id, netconf['hidden_layers'], netconf['activation_function'], '', netconf['model_path'], False)

            wdnn_model = wdnn.wdnn_build('wdnn', nn_id, netconf['hidden_layers'],netconf['activation_function'],dataconf['data_conf'], netconf['model_path'], False)

            label_column = list(dataconf['data_conf']["label"].keys())[0]

            # data -> csv (pandas)
            df = pd.read_csv( tf.gfile.Open('/hoya_src_root/adultest.data'),
                             # names=COLUMNS,
                              skipinitialspace=True,
                              engine="python")

            # df['label'] = (df[label_column].apply(lambda x: "Y" in x)).astype(int)
            # df['label'] = (df['income_bracket'].apply(lambda x: '>50K' in x)).astype(int)


            # predict
            #    def input_fn(self, df, nnid, dataconf ):
            predict_results = wdnn_model.predict(input_fn=lambda: wdnn.input_fn( df, nn_id, dataconf['data_conf']))
            df['label'] = list(predict_results)

            return None
        except Exception as e:
            raise Exception(e)
        return None

    def eval(self, node_id, parm={}):
        """

        :param node_id:
        :param parm:
        :return:
        """
        pass
    def _init_node_parm(self, key):
        """
        Init parameter from workflow_data_frame
        :return:
        """
        wf_net_conf = WorkFlowNetConfWdnn(key)
        self.model_path = wf_net_conf.model_path
        self.hidden_layers = wf_net_conf.hidden_layers
        self.activation_function = wf_net_conf.activation_function
