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
from cluster.preprocess.pre_node_feed_fr2wdnn import PreNodeFeedFr2Wdnn
from cluster.data.data_node_frame import DataNodeFrame
from common import utils
from time import gmtime, strftime
from cluster.common.train_summary_accloss_info import TrainSummaryAccLossInfo


class NeuralNetNodeWdnn(NeuralNetNode):
    """
    Tensorflow Wide and Deep Network Class
    :param self:
    :return:
    """

    def run(self, conf_data):
        """
        Wide and Deep Network Training 
        :param : conf_data
        :return: None
        """
        logging.info("NeuralNetNodeWdnn Run called")

        try:
            self._init_node_parm(conf_data['node_id'])

            if self.train == False: #Train Value 가 False면 훈련 안함
                 return None
            #Set Data Feeder
            self.cls_pool = conf_data['cls_pool'] # Data feeder

            # set batch
            self.load_batch = self.get_eval_batch(conf_data['node_id']) #Train이 Y인것 가져오기 Eval Flag가 Y인거 가져오기
            self.train_batch, self.batch = self.make_batch(conf_data['node_id'])
            #self.before_train_batch = self.get_before_make_batch(conf_data['node_id'], self.batch)  # before train batch

            #if self.before_train_batch != None:
            #    self.model_train_before_path = ''.join([self.model_path+'/'+str(self.before_train_batch.nn_batch_ver_id)])
            logging.info("Wdnn Train get batch -> {0}".format(self.batch))
            logging.info("Wdnn Train get batch -> {0}".format(self.load_batch))
            if self.train_batch == None :
                self.model_train_path = ''.join([self.model_path+'/'+self.batch])
            else :
                self.model_train_path = ''.join([self.model_path + '/' + self.train_batch])

            #Todo Eval flag 보도록 고치고
            #    "nn_wf_ver_id": self.wf_ver, "nn_batch_ver_id": self.batch}
            config = {"nn_id": conf_data['node_id'], "nn_wf_ver_id": self.net_ver,
                      "nn_batch_ver_id": self.batch}
            acc_result = TrainSummaryAccLossInfo(config)

            if self.load_batch  != self.batch:
                src = ''.join([self.model_path+'/'+self.load_batch])
                dst =  self.model_train_path
                utils.copy_all(src, dst)

            logging.info("model_path : {0} ".format(self.model_path))
            logging.info("hidden_layers : {0} ".format(self.hidden_layers))
            logging.info("activation_function : {0} ".format(self.activation_function))
            logging.info("batch_size : {0} ".format(self.batch_size))
            logging.info("epoch : {0} ".format(self.epoch))
            logging.info("model_type : {0} ".format(self.model_type))


            data_conf_info = self.data_conf

            # make wide & deep model
            wdnn = NeuralCommonWdnn()
            wdnn_model = wdnn.wdnn_build(self.model_type, conf_data['node_id'],self.hidden_layers,str(self.activation_function),data_conf_info, str(self.model_train_path),self.train, self.auto_demension)

            #feed
            # TODO file이 여러개면 어떻하지?
            # get prev node for load data
            data_node_name = self._get_backward_node_with_type(conf_data['node_id'], 'preprocess')
            train_data_set = self.cls_pool[data_node_name[0]] #get filename
            file_queue  = str(train_data_set.input_paths[0]) #get file_name

            #file을 돌면서 최대 Row를 전부 들고 옴 tfrecord 총 record갯수 가져오는 방법필요
            _batch_size = self.batch_size
            _num_tfrecords_files = 0

            #multi Feeder modified
            multi_read_flag = self.multi_read_flag

            #validation_monitor = _LossCheckerHook(acc_result)
            train_cnt = 5



            #customsMonitor = EarlyStoppingHook()
            if multi_read_flag == True:
                logging.info("Reading tfrecord")
                for index, fn in enumerate(train_data_set.input_paths):
                    _num_tfrecords_files += self.generator_len(
                        tf.python_io.tf_record_iterator(fn))  # get length of generators
                logging.info("total loop " + str(math.ceil(_num_tfrecords_files/_batch_size)) )

                for index in range(int(math.ceil(_num_tfrecords_files/_batch_size))):
                    for i in range(train_cnt):
                        logging.info("number of for loop " + str(index))
                        train_result = wdnn_model.fit(input_fn=lambda: train_data_set.input_fn(tf.contrib.learn.ModeKeys.TRAIN, file_queue,_batch_size), steps=self.epoch)
                        #train_result = wdnn_model.fit(
                        #    input_fn=lambda: train_data_set.input_fn(tf.contrib.learn.ModeKeys.TRAIN, file_queue,
                        #                                             _batch_size), steps=self.epoch)
                        eval_result = wdnn_model.evaluate(
                            input_fn=lambda: train_data_set.input_fn(tf.contrib.learn.ModeKeys.TRAIN, file_queue,
                                                                     _batch_size), steps=200)
                        acc = eval_result['accuracy']
                        loss = eval_result['loss']
                        acc_result.loss_info["loss"].append(str(eval_result['loss']))
                        acc_result.acc_info["acc"].append(str(eval_result['accuracy']))


            else:
                #Todo H5
                # train per files in folder h5용
                logging.info("Reading hdf5")
                while(train_data_set.has_next()) :

                    for i in range(0, train_data_set.data_size(), self.batch_size):
                        for i in range(train_cnt):
                            data_set = train_data_set[i:i + self.batch_size]
                            if i == 0:
                                eval_data_Set = data_set
                            train_result = wdnn_model.fit(
                                input_fn=lambda: train_data_set.input_fn2(tf.contrib.learn.ModeKeys.TRAIN, file_queue,
                                                                          data_set,data_conf_info), steps=self.epoch)
                            eval_result = wdnn_model.evaluate(
                                input_fn=lambda: train_data_set.input_fn2(tf.contrib.learn.ModeKeys.TRAIN, file_queue,
                                                                          data_set, data_conf_info), steps=200)
                            print("model fitting h5 " + str(data_set))

                            acc = eval_result['accuracy']
                            loss = eval_result['loss']
                            acc_result.loss_info["loss"].append(str(eval_result['loss']))
                            acc_result.acc_info["acc"].append(str(eval_result['accuracy']))
                            #train_result = wdnn_model.fit(
                            #    input_fn=lambda: train_data_set.input_fn2(tf.contrib.learn.ModeKeys.TRAIN, file_queue,
                            #                                              data_set, data_conf_info), steps=self.epoch)

                            logging.info("Traing Result -> {0}".format(train_result))

                    train_data_set.next()

                print("end")
                self.save_accloss_info(acc_result)
            return None
        except Exception as e:
            logging.info("[Wide and Deep Train Process] : {0}".format(e))
            raise Exception(e)

    def generator_len(self, it):
        """
                Help for Generator length promote util class(?)
                :param it : python generator
                :return: length of generatorDataNodeFrame
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
        store_filepath_name = data_path + "/" + "adult.noth5"
        hdf = pd.HDFStore(store_filepath_name)
        hdf.put('table1', dataframe, format='table', data_columns=True)
        hdf.close()

    def _set_progress_state(self):
        return None

    def predict2(self, nn_id, conf_data, parm = {}):

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
        #key = conf_data.
        wf_net_conf = WorkFlowNetConfWdnn(key)
        self.model_path = wf_net_conf.model_path
        self.hidden_layers = wf_net_conf.hidden_layers
        self.activation_function = wf_net_conf.activation_function
        self.batch_size = wf_net_conf.batch_size
        self.epoch = wf_net_conf.epoch
        self.model_type = wf_net_conf.model_type
        self.train = wf_net_conf.train
        self.auto_demension = wf_net_conf.auto_demension
        #Todo 어떻게 꺼내는지 승우씨한테 물어볼것
        _wf_data_conf = wf_data_conf(key.split('_')[0]+'_'+key.split('_')[1]+'_'+'dataconf_node')
        self.data_conf = _wf_data_conf.conf
        self.label = _wf_data_conf.label
        self.cell_feature = _wf_data_conf.cell_feature
        self.cross_cell = _wf_data_conf.cross_cell
        self.extend_cell_feature = _wf_data_conf.extend_cell_feature
        self.label_values = _wf_data_conf.label_values

        _wf_data_node = wf_data_node(key.split('_')[0] + '_' + key.split('_')[1] + '_' + 'data_node')
        self.multi_read_flag = _wf_data_node.multi_node_flag
        self.predict_path = _wf_data_node.predict_path


    def eval(self, node_id, conf_data, data=None, result=None):
        """
            Tensorflow Wide and Deep Network Eval Method
        :param node_id:
        :param parm:
        :return: None
        """
        logging.info("eval_starting ------> {0}".format(node_id))
        try:
            #self._init_node_parm(conf_data['node_id'])
            #conf_data['node_id']
            #self._init_node_parm(conf_data['node_id'])
            self._init_node_parm(conf_data.get('nn_id') + "_" + conf_data.get('wf_ver')+ "_" + "netconf_node")
            self.cls_pool_all = conf_data['cls_pool']  # Data feeder

            config = {"type": self.model_type, "labels": self.label_values, "nn_id":conf_data.get('nn_id'), "nn_wf_ver_id":conf_data.get('wf_ver')}
            train = TrainSummaryInfo(conf=config)
            print(config)
            self.batch_eval = self.get_eval_batch(node_id)
            #print(train)
            self.model_eval_path = ''.join([self.model_path + '/' + self.batch])


            for _k, _v in self.cls_pool_all.items():
                if 'test' in _k:
                    self.cls_pool = _v

                if 'evaldata' in _k:
                    self.multi_node_flag = _v.multi_node_flag

            #conf_data['cls_pool'].get('nn00001_1_pre_feed_fr2wdnn_test')
            logging.info("model_path : {0}".format(self.model_path))
            print("hidden_layers : {0}".format(self.hidden_layers))
            print("activation_function : {0}".format(self.activation_function))
            print("batch_size : {0}".format(self.batch_size))
            print("epoch : {0}".format(self.epoch))
            print("model_type : {0}".format(self.model_type))
            print("model_type : {0}".format(self.auto_demension))

            config_acc = {"nn_id": conf_data['node_id'], "nn_wf_ver_id": conf_data.get('wf_ver'),
                      "nn_batch_ver_id": self.batch}
            acc_result = TrainSummaryAccLossInfo(config_acc)

            data_conf_info = self.data_conf

            #validation_monitor = _LossCheckerHook(acc_result)

            # make wide & deep modelnot
            wdnn = NeuralCommonWdnn()
            wdnn_model = wdnn.wdnn_build(self.model_type, conf_data['node_id'], self.hidden_layers,
                                         str(self.activation_function), data_conf_info, str(self.model_eval_path),
                                         self.train, self.auto_demension)

            #, self.train, self.auto_demension

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

                        eval_result = wdnn_model.evaluate(
                           input_fn=lambda: train_data_set.input_fn2(tf.contrib.learn.ModeKeys.TRAIN, file_queue,
                                                                     data_set, data_conf_info), steps=200)
                        print("model fitting h5 " + str(data_set))

                        acc = eval_result['accuracy']
                        loss = eval_result['loss']
                        acc_result.loss_info["loss"].append(str(eval_result['loss']))
                        acc_result.acc_info["acc"].append(str(eval_result['accuracy']))

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
                        predict_y = list(data_set['predict_label'])


                        ori_list.extend(data_set[self.label].values.tolist())
                        pre_list.extend(list(data_set['predict_label']))

                        # model fitting
                        logging.info("wdnn eval ori list  : {0}".format(len(ori_list)) )
                        logging.info("wdnn eval pre list  : {0}".format(len(pre_list)) )

                    train_data_set.next()

                #TODO : 앞으로 옮기자
                train.set_nn_batch_ver_id(self.batch_eval)
                if self.model_type == "regression":
                    results['ori'] = ori_list
                    results['pre'] = pre_list
                    train.set_result_info(ori_list, pre_list)

                if (self.model_type == "category" or self.model_type == "deep"):
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
        except Exception as oe:
            logging.info(oe)
            raise Exception(e)
        return train
        # with tf.Session() as sess:

    def predict(self, node_id,ver, parm, data=None, result=None):

        """ Wdnn predict 
            batchlist info에서 active flag가 Y인 Model을 가져와서 예측을 함 

        Args:
          params: 
            * node_id
            * conf_data

        Returns:
            none

        Raises:

        Example

        """
        try:
            logging.info("wdnn predict_start nnid : {0}".format(node_id))
            if ver == 'active':
                self.batch, wf_ver = self.get_active_batch2(node_id)
                #self.model_predict_path = ''.join([self.model_path + '/' + self.batch])
            else:
                wf_ver = ver
                _nn_ver_id= node_id + "_" + wf_ver + "_" + "netconf_node"
                self.batch = self.get_active_batch(_nn_ver_id)  # Train이 Y인것 가져오기 Eval Flag가 Y인거 가져오기

            _node_id = node_id + "_" + wf_ver+ "_" + "netconf_node"
            _data_conf_id = node_id + "_" + wf_ver + "_dataconf_node"
            self._init_node_parm(_node_id)

            config = {"type": self.model_type, "labels": self.label_values, "nn_id":node_id, "nn_wf_ver_id":ver}
            #train = TrainSummaryInfo(conf=config)
            self.model_predict_path = ''.join([self.model_path + '/' + self.batch])
            self.multi_node_flag = False
            self.predict_path = ''.join(['/hoya_src_root/'+node_id+'/common/predict'])

            conf_data = {}
            conf_data['node_id'] = _node_id

            logging.info("model_path : " + str(self.model_path))
            logging.info("hidden_layers : " + str(self.hidden_layers))
            logging.info("activation_function : " + str(self.activation_function))
            logging.info("batch_size : " + str(self.batch_size))
            logging.info("epoch : " + str(self.epoch))
            logging.info("model_type : " + str(self.model_type))

            data_conf_info = self.data_conf
            # make wide & deep model
            wdnn = NeuralCommonWdnn()
            wdnn_model = wdnn.wdnn_build(self.model_type, node_id, self.hidden_layers,
                                         str(self.activation_function), data_conf_info, str(self.model_predict_path),dememsion_auto_flag = self.auto_demension)
            # feed
            le = LabelEncoder()
            le.fit(self.label_values)

            file_cnt = len(parm.FILES.keys())
            dir = 'predict'
            filelist = list()
            if file_cnt > 0:
                for key, requestSingleFile in parm.FILES.items():
                    filelist.append(str(requestSingleFile._name))

            _batch_size = self.batch_size
            _num_tfrecords_files = 0

            # multi Feeder modified
            multi_read_flag = self.multi_read_flag

            results = dict()
            ori_list = list()
            pre_list = list()
            #self.batch_size = 5
            for filename in filelist:
                print("h5")
                #feeder = PreNodeFeedFr2Wdnn().set_for_predict(_data_conf_id)
                feeder = PreNodeFeedFr2Wdnn()

                feeder.set_for_predict(_data_conf_id)
                data_node = DataNodeFrame()
                train_data_set = data_node.load_csv_by_pandas(self.predict_path + "/" + filename)

                result_df = pd.DataFrame()

                for i in range(0, len(train_data_set.index), self.batch_size):

                    data_set = train_data_set[i:i + self.batch_size]

                    predict_value = wdnn_model.predict(
                        input_fn=lambda: feeder.input_fn2(tf.contrib.learn.ModeKeys.TRAIN, filename,
                                                                  data_set, data_conf_info))

                    data_set_count = len(data_set.index)
                    predict_val_list = [_pv for _pv in predict_value]
                    predict_val_count = len(predict_val_list)

                    if (data_set_count != predict_val_count):
                        logging.error("wdnn eval error check : dataframe count({0}) predict count({1})".format(data_set_count, predict_val_count))
                        raise ValueError(
                            'eval data validation check error : dataframe and predict count is different(neuralnet_node_wdnn.eval)')

                    data_set['predict_label'] = list(le.inverse_transform(predict_val_list)) #list(predict_value)

                    #_predict = list(predict_value)
                    predict_y = list(data_set['predict_label'])
                    #pd.concat(result_df, data_set)
                    result_df = result_df.append(data_set)
                    ori_list.extend(data_set[self.label].values.tolist())
                    pre_list.extend(list(data_set['predict_label']))

                    logging.info("wdnn eval ori list  : {0}".format(len(ori_list)))
                    logging.info("wdnn eval ori list  : {0}".format(len(pre_list)))
                #train_data_set.next()

            predict_result_dir = utils.make_and_exist_directory(self.predict_path + "/" + "result" + "/")
            predict_result_filename = predict_result_dir + "result_" + strftime("%Y-%m-%d-%H:%M:%S",
                                                                                gmtime()) + ".csv"
            result_df.to_csv(predict_result_filename)

            logging.info("eval end")
            return json.loads(result_df.to_json())
        except Exception as e:
            logging.error("Wdnn predict error {0}".format(e))

            raise Exception(e)

    # with tf.Session() as sess:


class _LossCheckerHook(tf.train.SessionRunHook):

    def __init__(self, conf = None):

        if (conf):

            self.acc_result = conf
    def begin(self):
        self.loss_collection = tf.get_collection(tf.GraphKeys.LOSSES)

    def after_run(self, run_context, run_values):
        losses = run_context.session.graph.get_collection("losses")
        acc1 = run_context.session.graph.get_tensor_by_name('binary_logistic_head/metrics/accuracy/total:0')
        acc2 = run_context.session.graph.get_tensor_by_name('binary_logistic_head/metrics/accuracy/count:0')
        acc3 = run_context.session.graph.get_tensor_by_name('binary_logistic_head/metrics/accuracy_1/total:0')
        acc4 = run_context.session.graph.get_tensor_by_name('binary_logistic_head/metrics/accuracy_1/count:0')

        #acc = run_context.session.graph.get_collection("summaries")
        sess_loss = run_context.session.run(losses)[0]
        sess_acc1 = run_context.session.run(acc1)
        sess_acc2 = run_context.session.run(acc2)
        sess_acc3 = run_context.session.run(acc3)
        sess_acc4 = run_context.session.run(acc4)

        self.acc_result.loss_info["loss"].append(str(sess_loss))
        logging.info("logging done")