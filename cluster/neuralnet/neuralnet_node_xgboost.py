import logging
import xgboost as xgb
import pandas as pd
import importlib.util
import json
from time import gmtime, strftime

from cluster.common.train_summary_accloss_info import TrainSummaryAccLossInfo
from cluster.common.train_summary_info import TrainSummaryInfo
from cluster.data.data_node_frame import DataNodeFrame
from master.workflow.netconf.workflow_netconf_xgboost import WorkFlowNetConfXgboost
from master.network.nn_common_manager import NNCommonManager
from cluster.neuralnet.neuralnet_node import NeuralNetNode
from common import utils

class NeuralNetNodeXgboost(NeuralNetNode):
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
        logging.info("NeuralNetNode Xgboost Run called") #nodeid 필요

        try:

            self._init_train_parm(conf_data)
            #self._init_value()
            train, test= self.get_input_data()

            spec = importlib.util.spec_from_file_location("data_preprocess", "/hoya_src_root/data_preprocess.py")
            foo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(foo)
            _label, _label_info, _label_values = foo.label_info()

            y_train = train[_label].ravel()
            x_train = train.drop([_label,"id"], axis=1)

            y_test = test[_label].ravel()
            x_test = test.drop([_label,"id"], axis=1)

            #x_train = train.values  # Creates an array of the train data
            #x_test = test.values  # Creats an array of the test data

            self.load_batch = self.get_eval_batch(self.node_id)  # Train이 Y인것 가져오기 Eval Flag가 Y인거 가져오기
            self.train_batch, self.batch = self.make_batch(self.node_id)

            logging.info("Xgboost Train get batch -> {0}".format(self.batch))
            logging.info("Xgboost Train get batch -> {0}".format(self.load_batch))
            if self.train_batch == None:
                self.model_train_path = ''.join([self.model_path + '/' + self.batch + '.bin'])
            else:
                self.model_train_path = ''.join([self.model_path + '/' + self.train_batch + '.bin'])

            xgb_params = self.get_xgboost_paramter()

            num_rounds = self.conf.get("epoch")
            dtrain = xgb.DMatrix(x_train, y_train)  # training data
            dvalid = xgb.DMatrix(x_test, y_test)  # validation data
            eval_result= {}
            gbm = xgb.train(xgb_params, dtrain, num_rounds,
                            [(dtrain, 'train'),(dvalid,"test")],
                            evals_result= eval_result
                            )  # stop if no improvement in 10 rounds

            gbm.save_model(self.model_train_path )
            predictions = gbm.predict(dvalid)
            train_prediction = gbm.predict(dvalid)

            #trainprediction_xgb = pd.DataFrame({'id': test,
            #                                    'predict': train_prediction})

            #trainprediction_xgb_merge = train_results_xgb.merge(trainprediction_xgb, how='left', on='id')
            # Todo Eval flag 보도록 고치고
            #    "nn_wf_ver_id": self.wf_ver, "nn_batch_ver_id": self.batch}
            config = {"nn_id": self.nn_id, "nn_wf_ver_id": self.wf_ver,
                      "nn_batch_ver_id": self.batch}
            acc_result = TrainSummaryAccLossInfo(config)
            acc_result.loss_info["loss"].extend(eval_result['test']['rmse'])
            acc_result.acc_info["acc"].extend(eval_result['test']['rmse'])
            self.save_accloss_info(acc_result)

            config = {"type": self.model_type, "labels": _label_values, "nn_id":self.nn_id, "nn_wf_ver_id":self.wf_ver}
            eval_result = TrainSummaryInfo(conf=config)
            eval_result.set_nn_batch_ver_id(self.batch)

            eval_result.set_result_info(y_test, train_prediction)

            input_data = TrainSummaryInfo.save_result_info(self, eval_result)
            input_data['accuracy'] = eval_result.get_accuracy()

            return input_data
        except Exception as e:
            logging.info("NeuralNetNodeXgboost Run Exception : {0}".format(e))
            raise Exception(e)

    def get_xgboost_paramter(self):
        xgb_params = {}
        xgb_params["eta"] = self.conf.get("learning_rates")
        xgb_params["colsample_bytree"] = self.conf.get("colsample_bytree")
        xgb_params["gamma"] = self.conf.get("gamma")
        xgb_params["max_depth"] = self.conf.get("max_depth")
        xgb_params["min_child_weight"] = self.conf.get("min_child_weight")
        xgb_params["n_estimator"] = self.conf.get("n_estimator")
        xgb_params["subsample"] = self.conf.get("subsample")
        xgb_params["eval_metric"] = ['logloss', "mae","map","rmse"]

        _drop_none_params = [_k for _k, _v in xgb_params.items() if (_v == None or _v == 'None')]

        for _x in _drop_none_params:
            del xgb_params[_x]

        if self.model_type == 'regression':
            _model_type = {"objective": "reg:linear"}
        else:
            _model_type = {"objective": "multi:softmax"}

        xgb_params.update(_model_type)
        return xgb_params


    def get_input_data(self):
        try:

            train_list = [ self.load_data_from_h5(file_path) for file_path in utils.get_filepaths(self.data_store_path)]
            df_train = pd.DataFrame()
            result_train = df_train.append(train_list)

            test_list = [self.load_data_from_h5(file_eval_path) for file_eval_path in utils.get_filepaths(self.data_store_eval_path)]
            df_test = pd.DataFrame()
            result_test = df_test.append(test_list)
        except Exception as e:
            logging.info("NeuralNetNodeXgboost get input Exception : {0}".format(e))
            raise Exception(e)

        return result_train, result_test


    def get_predict_data(self, filelist):
        try:

            #for key, requestSingleFile in parm.FILES.items():
            df_train = pd.DataFrame()
            df_list = []
            for key, requestSingleFile in filelist.items():

                data_node = DataNodeFrame()
                #train_data_set = data_node.load_csv_by_pandas(self.predict_path + "/" + filename)

                df = pd.read_csv(requestSingleFile.file)
                df_list.append(df)

                #df_train.append(df)
        except Exception as e:
            logging.info("NeuralNetNodeXgboost get input Exception : {0}".format(e))
            raise Exception(e)

        return df_train.append(df_list)

    def _init_train_parm(self, conf_data):
        # get initial value
        self.conf_data = conf_data
        self.cls_pool = conf_data["cls_pool"]
        self.nn_id = conf_data["nn_id"]
        self.wf_ver = conf_data["wf_ver"]
        self.node_id = conf_data["node_id"]
        graph = NNCommonManager().get_nn_node_name(conf_data["nn_id"])
        for net in graph:
            if net['fields']['graph_node'] == 'netconf_node':
                self.netconf_node = net['fields']['graph_node_name']
            if net['fields']['graph_node'] == 'netconf_feed':
                self.train_feed_name = self.nn_id + "_" + self.wf_ver + "_" + net['fields']['graph_node_name']
            if net['fields']['graph_node'] == 'eval_feed':
                self.eval_feed_name = self.nn_id + "_" + self.wf_ver + "_" + net['fields']['graph_node_name']
        self.feed_node = self.get_prev_node()

        #key = conf_data.
        wf_net_conf = WorkFlowNetConfXgboost(self.node_id )
        self.conf = wf_net_conf.conf
        self.data_store_path = utils.get_store_path(self.net_id, self.net_ver, "data_node")
        self.data_store_eval_path = utils.get_store_path(self.net_id, self.net_ver, 'evaldata')
        self.model_path =self.conf.get('model_path')
        self.model_type = self.conf.get('model_type')
        print("")




    def _init_value(self):
        '''
        Residual Network Init Value
        :return: 
        '''

        self.file_end = '.bin'
        self.train_return_data = {}
        self.data_store_path = utils.get_store_path(self.net_id, self.net_ver, "data_node")
        self.data_store_eval_path = utils.get_store_path(self.net_id, self.net_ver, 'evaldata')
        self.model_path =self.conf.get('model_path')
        self.model_type = self.conf.get('model_type')

    def eval(self, node_id, conf_data, data=None, result=None):
        """
            Tensorflow Wide and Deep Network Eval Method
        :param node_id:
        :param parm:
        :return: None
        """
        logging.info("xgboost eval_starting ------> {0}".format(node_id))
        try:
            logging.info("xgboost eval_ending ------> {0}".format(node_id))
        except Exception as oe:
            logging.info(oe)
            raise Exception(oe)
        return None

    def predict(self, node_id, filelist):

        """ Wdnn predict 
            batchlist info에서 active flag가 Y인 Model을 가져와서 예측을 함 

        Args:
          params: 
            * node_id
            * conf_data

        Returns:
            none

        Raises:INFO

        Example

        """
        try:
            logging.info("xgboost predict_start nnid : {0}".format(node_id))
            self.node_id = node_id
            netconf = WorkFlowNetConfXgboost().get_view_obj(self.node_id)

            # get unique key
            self.load_batch = self.get_active_batch(self.node_id)
            # 훈련시 배치를 잘 들고 오는
            last_chk_path = ''.join([netconf.get('model_path'), "/" , self.load_batch ,".bin"])
            #xgb_params = self.get_xgboost_paramter()

            gbm = xgb.Booster()  # init model
            gbm.load_model(last_chk_path)  # load data

            predict_csv_read = self.get_predict_data(filelist)

            #y_train = predict_csv_read[_label].ravel()


            spec = importlib.util.spec_from_file_location("data_preprocess", "/hoya_src_root/data_preprocess.py")
            foo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(foo)
            _pre_df_predict_csv_read = foo.data_preprocess_by_file(predict_csv_read)

            x_predict = _pre_df_predict_csv_read.drop(["id"], axis=1)


            d_predict = xgb.DMatrix(x_predict)  # validation data

            predictions = gbm.predict(d_predict)

            predict_csv_read['predict'] = predictions

            self.save_predict_file(node_id, predict_csv_read)
            return json.loads(predict_csv_read.to_json())



        except Exception as e:
            logging.error("xgboost predict error {0}".format(e))

            raise Exception(e)

    def save_predict_file(self, node_id, df):

        _predict_path = utils.get_source_predict_path(node_id.split('_')[0], node_id.split('_')[1], 'predict')

        predict_result_dir = utils.make_and_exist_directory(_predict_path + "/" + "result" + "/")
        predict_result_filename = predict_result_dir + str(node_id) +"_" + strftime("%Y-%m-%d-%H:%M:%S",
                                                                            gmtime()) + ".csv"
        df.to_csv(predict_result_filename)

