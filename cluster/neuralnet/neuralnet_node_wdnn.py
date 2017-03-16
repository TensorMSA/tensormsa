from cluster.neuralnet.neuralnet_node import NeuralNetNode
from master.workflow.netconf.workflow_netconf_wdnn import WorkFlowNetConfWdnn
from master.workflow.data.workflow_data_frame import WorkFlowDataFrame
import pandas as pd
import os


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
            print("model_path : " + str(self.model_path))
            print("hidden_layers : " + str(self.hidden_layers))
            print("activation_function : " + str(self.activation_function))

            data_store_path = WorkFlowDataFrame(conf_data['nn_id']+"_"+conf_data['wf_ver']+"_"+ "data_node").step_store

            filename = data_store_path + "/" + "adult.h5"

            for root, dirs, files in os.walk(data_store_path):
                for file in files:
                    print(file)


            print(filename)


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
    def read_hdf5(self,filename):

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
