from cluster.service import WorkFlowPredictTask


class PredictService :
    """
    1. definition
        -manage job list
        -manage cluster tarin server status
        -manage cluster job and result

    2. table
        CONF_SERV_CLUSTER_INFO
        COMMON_JOB_LIST_INFO
        NN_VER_BARCHLIST_INFO
    """

    def regist_predict_request(self):
        task = WorkFlowPredictTask()
        task.run()
        return None
