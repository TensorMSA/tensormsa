from cluster.neuralnet.neuralnet_node import NeuralNetNode
from master.workflow.netconf.workflow_netconf_wdnn import WorkFlowNetConfWdnn
from master.workflow.data.workflow_data_frame import WorkFlowDataFrame
import pandas as pd
import os
from master.workflow.dataconf.workflow_dataconf_frame import WorkflowDataConfFrame
from cluster.common.neural_common_wdnn import NeuralCommonWdnn
from common import utils

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


            #read hdf5
            try:
                #TODO file이 여러개면 어떻하지?
                file_paths = list()
                # for file_path in utils.get_filepaths(data_store_path, "tfrecords"):
                #     file_paths.append(file_path)
                for file_path in utils.get_filepaths(data_store_path, "h5"):
                    file_paths.append(file_path)

                df = self.read_hdf5(file_paths[0])

            except Exception as e:
                print("Error Message : {0}".format(e))
                raise Exception(e)

            #feature, label = wdnn.input_fn( df, conf_data['node_id'],data_conf_info)

            wdnn_model.fit(input_fn=lambda: wdnn.input_fn( df, conf_data['node_id'],data_conf_info), steps=200)

            results = wdnn_model.evaluate(input_fn=lambda: wdnn.input_fn( df, conf_data['node_id'],data_conf_info), steps=1)
            for key in sorted(results):
                print("%s: %s" % (key, results[key]))

            #m.fit(input_fn=lambda: input_fn(df_train), steps=train_steps)



            #for root, dirs, files in os.walk(data_store_path):
            #    for file in files:
            #        print(file)

            # make wide & deep model
            #wdnn_model = WdnnCommonManager.wdnn_build(self, nnid = nnid)


            #print(filename)


            #self.model_path = wf_net_conf.model_path
            #self.hidden_layers = wf_net_conf.hidden_layers
            #self.activation_function = wf_net_conf.activation_function
            #activation_function

            # #make wide & deep model
            # wdnn_model = WdnnCommonManager.wdnn_build(self, nnid = nnid)
            #
            # #get json from postgres by nnid
            # json_string = WdnnCommonManager.get_all_info_json_by_nnid(self, nnid=nnid)
            # database = json_string["dir"]
            # table_name = json_string["table"]
            #
            # #Make NetworkConfiguration Json Objct
            # json_string = netconf.load_ori_format(nnid)
            # json_ob = json.loads(json_string)
            #
            # #get label column from hbase nn config json
            # t_label = json_ob["label"]
            # label_column = list(t_label.keys())[0]
            #
            # #get train hyper param
            # #job_parm = JobStateLoader().get_selected_job_info(nnid)
            # batch_size = int(job_parm.batchsize)
            # model_lint_cnt = int(job_parm.epoch)
            #
            #
            # df, pnt = data.DataMaster().query_data(database, table_name, "a", use_df=True,limit_cnt=batch_size,with_label=label_column, start_pnt = start_pnt)
            # df_eval = df.copy()
            #
            #
            #
            # ##MAKE MONITOR
            #
            # customsMonitor = Monitors.MonitorCommon(p_nn_id = nnid, p_max_steps=model_lint_cnt, p_every_n_steps=1000)
            #
            #
            # wdnn_model.fit(input_fn=lambda: WdnnCommonManager.input_fn(self, df, nnid), steps=model_lint_cnt, monitors=[customsMonitor])
            #
            # if(len(df_eval) < 10):
            #
            #     results = wdnn_model.evaluate(input_fn=lambda: WdnnCommonManager.input_fn(self, df_eval, nnid), steps=1)
            #     for key in sorted(results):
            #         tfmsa_logger("%s: %s" % (key, results[key]))
            #     return nnid
            # else:
            #     JobStateLoader().inc_job_data_pointer(nnid)
            #     self.run_wdd_train(nnid = nnid , start_pnt = pnt)
            #
            # return nnid
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

    def predict(self, node_id, parm = {}):
        pass

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
