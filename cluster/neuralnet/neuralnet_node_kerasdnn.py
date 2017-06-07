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
import math
from master.workflow.dataconf.workflow_dataconf_frame import WorkflowDataConfFrame as wf_data_conf
from master.workflow.data.workflow_data_frame import WorkFlowDataFrame as wf_data_node
from cluster.common.train_summary_info import TrainSummaryInfo
#from tensorflow.python.platform import tf_logging as logging
import logging
import random
import shutil, errno
from sklearn.preprocessing import LabelEncoder
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Activation, Dense, BatchNormalization
import keras
#from keras. import
from sklearn.preprocessing import MinMaxScaler
from keras.callbacks import ReduceLROnPlateau, CSVLogger, EarlyStopping
import numpy as np

class History(keras.callbacks.Callback):
    def on_train_begin(self, logs={}):
        self.losses = []
        self.acc = []

    def on_batch_end(self, batch, logs={}):
        self.losses.append(str(logs.get('loss')))
        self.acc.append(str(logs.get('acc')))

class NeuralNetNodeKerasdnn(NeuralNetNode):
    """

    """

    def run(self, conf_data):
        logging.info("NeuralNetNodeWdnn Run called")
        #return None
        #return None
        """
                Wide & Deep Network Training
                :param nnid : network id in tfmsacore_nninfo
                :return: acturacy
        """
        try:
            self._init_node_parm(conf_data['node_id'])
            self.cls_pool = conf_data['cls_pool'] # Data feeder
            self.train_batch, self.batch = self.make_batch(conf_data['node_id']) #makebatch
            self.before_train_batch = self.get_before_make_batch(conf_data['node_id'], self.batch)  #before train batch

            if self.before_train_batch != None:
                self.model_train_before_path = ''.join([self.model_path+'/'+str(self.before_train_batch.nn_batch_ver_id)])

            if self.train_batch == None :
                self.model_train_path = ''.join([self.model_path+'/'+self.batch])
            else :
                self.model_train_path = ''.join([self.model_path + '/' + self.train_batch])

            #model file copy
            if self.before_train_batch != None:
                src = self.model_train_before_path
                dst =  self.model_train_path
                utils.copy_all(src, dst)

            logging.info("model_path : {0} ".format(self.model_path))
            logging.info("hidden_layers : {0} ".format(self.hidden_layers))
            logging.info("activation_function : {0} ".format(self.activation_function))
            logging.info("batch_size : {0} ".format(self.batch_size))
            logging.info("epoch : {0} ".format(self.epoch))
            logging.info("model_type : {0} ".format(self.model_type))

            data_conf_info = self.data_conf

            #feed
            # TODO file이 여러개면 어떻하지?
            # get prev node for load data
            data_node_name = self._get_backward_node_with_type(conf_data['node_id'], 'preprocess')
            train_data_set = self.cls_pool[data_node_name[0]] #get filename
            file_queue  = str(train_data_set.input_paths[0]) #get file_name

            #TODO 아 eval이 안되서 데이터가 안불러
            _batch_size = self.batch_size
            _num_tfrecords_files = 0
            #_batch_size = 2

            data_set = train_data_set[0 : train_data_set.data_size() ]

            input_dims = len(data_set.columns)-1 # label 갯수 제거
            # model = Sequential()
            # model.add(Dense(100, input_dim=input_dims, activation='relu'))
            # #model.add(Dense(50))
            # model.add(Dense(50, activation='sigmoid'))
            # #model.add(Dense(50, activation='sigmoid'))
            # model.compile(optimizer='rmsprop',
            #               loss='binary_crossentropy',
            #               metrics=['accuracy'])
            model = Sequential()
            model.add(Dense(10, input_dim=input_dims,init='uniform'))
            model.add(BatchNormalization())
            model.add(Activation('sigmoid'))
            #model.add(Dense(10, init='uniform'))
            #model.add(BatchNormalization())
            #model.add(Activation('sigmoid'))
            model.add(Dense(1, init='uniform'))
            model.add(BatchNormalization())
            model.add(Activation('sigmoid'))
            lr_reducer = ReduceLROnPlateau(monitor='val_loss', factor=np.sqrt(0.1), cooldown=0, patience=5, min_lr=0.5e-6)
            early_stopper = EarlyStopping(monitor='val_acc', min_delta=0.001, patience=10)
            csv_logger = CSVLogger('resnet18_cifar10.csv')
            history = History()

            # Compile model
            model.compile(loss='binary_crossentropy', optimizer='sgd')

            self.batch_size = 4



            #multi Feeder modified
            multi_read_flag = self.multi_read_flag
            if multi_read_flag == False:
                #Todo H5
                # train per files in folder h5용
                while(train_data_set.has_next()) :
                    logging.info("start keras dnn")
                    #파일이 하나 돌때마다
                    #for 배치사이즈와 파일의 총갯수를 가져다가 돌린다. -> 마지막에 뭐가 있을지 구분한다.
                    #파일에 iter를 넣으면 배치만큼 가져오는 fn이 있음 그걸 __itemd에 넣고
                    # Input 펑션에서 multi를 vk판단해서 col와 ca를 구분한다.(이걸 배치마다 할 필요가 있나?)
                    # -> 그러면서 피팅
                    #for x in range(0, self.iter_size):
                    for i in range(0, train_data_set.data_size(), self.batch_size):
                        #Last batch size preprocessing
                        if (i+self.batch_size > train_data_set.data_size()):
                            i= i - (train_data_set.data_size()%self.batch_size) + 1
                        data_set = train_data_set[i:i + self.batch_size]
                        #data_set = train_data_set[0:train_data_set.data_size()]

                        logging.info(i)
                        X_train, targets, = train_data_set.input_fn3( file_queue,data_set,data_conf_info)
                        #loss, accuracy =
                        model.fit(X_train, targets
                                  , epochs=10
                                  , validation_data=(X_train, targets)
                                  , batch_size=self.batch_size
                                  , callbacks = [lr_reducer, csv_logger, history]
                                  )


                        #logging.info("keras training info loss : {0} ,  accuracy{1}".format(loss, accuracy))
                    # #Select Next file
                    train_data_set.next()
                #os.makedirs(self.md_store_path + '/' + self.batch, exist_ok=True)
               # keras.models.save_model(model, ''.join([self.md_store_path + '/' + self.batch, '/model.bin']))

            print("end")
        except Exception as e:
            logging.error("Error Message : {0}".format(e))
            raise Exception(e)

        return None

    def generator_len(self, it):
        """
                Help for Generator length promote util class(?)
                :param it : python generator
                :return: length of generator
        """
        return len(list(it))

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

    def _init_node_parm(self, key):
        """
        Init parameter from workflow_data_frame
        :return:
        """
        wf_net_conf = WorkFlowNetConfWdnn(key)
        self.wf_state_id = wf_net_conf.get_state_id(key).pk
        netconfig = wf_net_conf.get_view_obj(key)
        self.model_path = wf_net_conf.model_path
        self.hidden_layers = wf_net_conf.hidden_layers
        self.activation_function = wf_net_conf.activation_function
        self.batch_size = wf_net_conf.batch_size
        self.epoch = wf_net_conf.epoch
        self.model_type = wf_net_conf.model_type
        #Todo 어떻게 꺼내는지 승우씨한테 물어볼것
        _wf_data_conf = wf_data_conf(key.split('_')[0]+'_'+key.split('_')[1]+'_'+'dataconf_node')
        self.data_conf = _wf_data_conf.conf
        self.label = _wf_data_conf.label
        self.cell_feature = _wf_data_conf.cell_feature
        self.cross_cell = _wf_data_conf.cross_cell
        self.extend_cell_feature = _wf_data_conf.extend_cell_feature
        self.label_values = _wf_data_conf.label_values

        if 'test' in self.get_prev_node()[0].node_name:
            _wf_data_node = wf_data_node(key.split('_')[0] + '_' + key.split('_')[1] + '_' + 'data_node')
            self.multi_read_flag = _wf_data_node.multi_node_flag
        else:
            _wf_data_node = wf_data_node(key.split('_')[0] + '_' + key.split('_')[1] + '_' + 'data_node')
            self.multi_read_flag = _wf_data_node.multi_node_flag

        #_wf_data_node = wf_data_node(key.split('_')[0] + '_' + key.split('_')[1] + '_' + 'data_node')
        #self.multi_read_flag = _wf_data_node.multi_node_flag


    def eval(self, node_id, conf_data, data=None, result=None):
        """

        :param node_id:
        :param parm:
        :return:
        """
        logging.info("eval_data")

        self._init_node_parm(node_id.split('_')[0] + "_" + node_id.split('_')[1]+ "_" + "netconf_node")
        self.cls_pool_all = conf_data['cls_pool']  # Data feeder

        config = {"type": self.model_type, "labels": self.label_values, "nn_id":conf_data.get('nn_id'), "nn_wf_ver_id":conf_data.get('wf_ver')}
        train = TrainSummaryInfo(conf=config)
        print(config)
        self.batch = self.get_eval_batch(node_id)
        #print(train)
        self.model_eval_path = ''.join([self.model_path + '/' + self.batch])


        for _k, _v in self.cls_pool_all.items():
            if 'test' in _k:
                self.cls_pool = _v

            if 'evaldata' in _k:
                self.multi_node_flag = _v.multi_node_flag

        #conf_data['cls_pool'].get('nn00001_1_pre_feed_fr2wdnn_test')
        print("model_path : " + str(self.model_path))
        print("hidden_layers : " + str(self.hidden_layers))
        print("activation_function : " + str(self.activation_function))
        print("batch_size : " + str(self.batch_size))
        print("epoch : " + str(self.epoch))
        print("model_type : " + str(self.model_type))

        # data_store_path = WorkFlowDataFrame(conf_data['nn_id']+"_"+conf_data['wf_ver']+"_"+ "data_node").step_store
        data_conf_info = self.data_conf

        # make wide & deep model
        wdnn = NeuralCommonWdnn()
        wdnn_model = wdnn.wdnn_build(self.model_type, conf_data['node_id'], self.hidden_layers,
                                     str(self.activation_function), data_conf_info, str(self.model_eval_path))

        # feed
        # TODO file이 여러개면 어떻하지?
        # get prev node for load data
        #data_node_name = self._get_backward_node_with_type(conf_data['node_id'], 'preprocess')
        #train_data_set = self.cls_pool[data_node_name[0]]  # get filename
        train_data_set = self.cls_pool  # get filename
        file_queue = str(train_data_set.input_paths[0])  # get file_name

        # file을 돌면서 최대 Row를 전부 들고 옴 tfrecord 총 record갯수 가져오는 방법필요

        _batch_size = self.batch_size
        _num_tfrecords_files = 0

        # multi Feeder modified
        multi_read_flag = self.multi_read_flag

        # Todo H5
        # train per files in folder h5용
        # if multi_file flag = no이면 기본이 h5임
        try:
            results = dict()
            ori_list = list()
            pre_list = list()

            while (train_data_set.has_next()):
                print("h5")
                # 파일이 하나 돌때마다
                # for 배치사이즈와 파일의 총갯수를 가져다가 돌린다. -> 마지막에 뭐가 있을지 구분한다.
                # 파일에 iter를 넣으면 배치만큼 가져오는 fn이 있음 그걸 __itemd에 넣고
                # Input 펑션에서 multi를 vk판단해서 col와 ca를 구분한다.(이걸 배치마다 할 필요가 있나?)
                # -> 그러면서 피팅
                #
                # # Iteration is to improve for Model Accuracy

                # Per Line in file
                # eval should be one line predict
                #self.batch_size = 2

                for i in range(0, train_data_set.data_size(), self.batch_size):

                    data_set = train_data_set[i:i + self.batch_size]
                    #if i == 0:
                    #eval_data_Set = data_set
                    # input_fn2(self, mode, data_file, df, nnid, dataconf):
                    predict_value = wdnn_model.predict(
                        input_fn=lambda: train_data_set.input_fn2(tf.contrib.learn.ModeKeys.TRAIN, file_queue,
                                                                  data_set, data_conf_info))

                    data_set_count = len(data_set.index)
                    predict_val_list = [_pv for _pv in predict_value]
                    predict_val_count = len(predict_val_list)

                    if (data_set_count != predict_val_count):
                        logging.error("wdnn eval error check : dataframe count({0}) predict count({1})".format(data_set_count, predict_val_count))
                        raise ValueError(
                            'eval data validation check error : dataframe and predict count is different(neuralnet_node_wdnn.eval)')

                    data_set['predict_label'] = predict_val_list #list(predict_value)
                    #_predict = list(predict_value)
                    predict_y = list(data_set['predict_label'])


                    ori_list.extend(data_set[self.label].values.tolist())
                    pre_list.extend(list(data_set['predict_label']))

                    # model fitting
                    print(len(ori_list))
                    print(len(pre_list))
                    #logging.error("wdnn eval ori list  : {0}".format(ori_list) )
                    logging.info("wdnn eval ori list  : {0}".format(len(ori_list)) )
                    #logging.info("wdnn eval ori list  : {0}".format('info'))
                    #logging.debug("wdnn eval ori list  : {0}".format('debug'))
                    #logging.critical("wdnn eval ori list  : {0}".format('critical'))
                    #print("model fitting h5 " + str(data_set))
                # #Select Next file
                train_data_set.next()

            #TODO : 앞으로 옮기자
            train.set_nn_batch_ver_id(self.batch)
            if self.model_type == "regression":
                results['ori'] = ori_list
                results['pre'] = pre_list
                train.set_result_info(ori_list, pre_list)

            if self.model_type == "category":
                # tfrecord는 여기서 Label을 변경한다. 나중에 꺼낼때 답이 없음 Tensor 객체로 추출되기 때문에 그러나 H5는 feeder에서 변환해주자
                le = LabelEncoder()
                le.fit(self.label_values)

                for _i, _ori in enumerate(ori_list):
                    #return_value = self.labels[np.argmax(model.predict(X_train))]
                    train.set_result_info(str(_ori), str(le.inverse_transform(pre_list[_i])))
            #return self.batch
        except Exception as e:
            print("eval error")
            print(e)
            raise Exception(e)

        logging.info("eval end")
        return train





