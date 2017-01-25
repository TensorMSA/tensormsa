from cluster.service import WorkFlowTrainTask

class RunManager :
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
    def get_view_obj(self):
        """
        get view data for net config
        :return:
        """
        pass

    def set_view_obj(self, obj):
        """
        set net config data edited on view
        :param obj:
        :return:
        """
        pass

    def regist_train_request(self):
        task = WorkFlowTrainTask()
        task.delay()

        return None

    def _find_proper_train_server(self):

        return None

    def _check_train_server_capa(self):

        return None

    def _get_next_job(self):

        return None

    def _check_cur_running_job(self):

        return None

    def _get_max_allow_job(self):

        return None

    def _exec_next_job(self):

        return None

    def set_job_init(self, nn_id, wf_ver):

        return None

    def set_job_start(self, nn_id, wf_ver):

        return None

    def set_job_finish(self, nn_id, wf_ver):
        return None

    def set_job_error(self, nn_id, wf_ver):
        return None
