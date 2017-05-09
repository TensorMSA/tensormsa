from cluster.common.common_node import WorkFlowCommonNode
from master import models
from master import serializers

class NeuralNetNode(WorkFlowCommonNode):
    """

    """

    def run(self, conf_data):
        """
        call on train
        :param conf_data:
        :return:
        """
        pass

    def _init_node_parm(self, node_id):
        """
        call on init parms from db
        :param node_id:
        :return:
        """
        pass

    def _set_progress_state(self):
        """
        set node progress info and etc
        :return:
        """
        pass

    def predict(self, node_id, parm = {}):
        """

        :param node_id:
        :param parm:
        :return:
        """
        pass

    def eval(self, node_id, parm={}):
        """

        :param node_id:
        :param parm:
        :return:
        """
        pass

    def make_batch(self, node_id):
        """
        call this function for next version
        :param node_id:
        :return:
        """
        netnode = models.NN_WF_NODE_INFO.objects.get(nn_wf_node_id=node_id)
        nn_id = netnode.wf_state_id.nn_id
        nn_wf_ver_id = netnode.wf_state_id.nn_wf_ver_id.nn_wf_ver_id
        ver_id = models.NN_VER_WFLIST_INFO.objects.get(nn_id=nn_id, nn_wf_ver_id=nn_wf_ver_id).id
        train_batch_count = len(models.NN_VER_BATCHLIST_INFO.objects.filter(nn_wf_ver_id=ver_id, train_flag='Y'))
        if train_batch_count == 0 :
            train_batch = None
        elif train_batch_count == 1 :
            train_batch = models.NN_VER_BATCHLIST_INFO.objects.get(nn_wf_ver_id=ver_id, train_flag='Y').nn_batch_ver_id
        eval_batch_count = len(models.NN_VER_BATCHLIST_INFO.objects.filter(nn_wf_ver_id=ver_id, eval_flag='Y'))
        if eval_batch_count != 0 :
            eval_batch = models.NN_VER_BATCHLIST_INFO.objects.get(nn_wf_ver_id=ver_id, eval_flag='Y')
            setattr(eval_batch, 'eval_flag', 'N')
            eval_batch.save()
        input_data = {}
        input_data['nn_wf_ver_id'] = ver_id
        count = len(models.NN_VER_BATCHLIST_INFO.objects.filter(nn_wf_ver_id=ver_id))
        input_data['nn_batch_ver_id'] = nn_id + '_' + str(nn_wf_ver_id) + '_' + str(count + 1)
        if count == 0 :
            input_data['active_flag'] = 'Y'
        else :
            input_data['active_flag'] = 'N'
        serializer = serializers.NN_VER_BATCHLIST_INFO_Serializer(data=input_data)
        if serializer.is_valid():
            serializer.save()
        return train_batch, input_data['nn_batch_ver_id']

    def get_active_batch(self, node_id):
        """
        find batch version for predict
        :param node_id:
        :return:
        """
        netnode = models.NN_WF_NODE_INFO.objects.get(nn_wf_node_id=node_id)
        nn_id = netnode.wf_state_id.nn_id
        nn_wf_ver_id = netnode.wf_state_id.nn_wf_ver_id.nn_wf_ver_id
        ver_id = models.NN_VER_WFLIST_INFO.objects.get(nn_id=nn_id, nn_wf_ver_id=nn_wf_ver_id).id
        batch = models.NN_VER_BATCHLIST_INFO.objects.get(nn_wf_ver_id=ver_id, active_flag='Y').nn_batch_ver_id
        return batch

    def get_eval_batch(self, node_id):
        """
        find a batch version for eval, train
        :param node_id:
        :return:
        """
        netnode = models.NN_WF_NODE_INFO.objects.get(nn_wf_node_id=node_id)
        nn_id = netnode.wf_state_id.nn_id
        nn_wf_ver_id = netnode.wf_state_id.nn_wf_ver_id.nn_wf_ver_id
        ver_id = models.NN_VER_WFLIST_INFO.objects.get(nn_id=nn_id, nn_wf_ver_id=nn_wf_ver_id).id
        batch = models.NN_VER_BATCHLIST_INFO.objects.get(nn_wf_ver_id=ver_id, eval_flag='Y').nn_batch_ver_id
        return batch

    def check_batch_exist(self, node_id):
        """
        use if you want to check batch data exists or not
        check if batch version data exists
        :param node_id:
        :return:
        """
        netnode = models.NN_WF_NODE_INFO.objects.get(nn_wf_node_id=node_id)
        nn_id = netnode.wf_state_id.nn_id
        nn_wf_ver_id = netnode.wf_state_id.nn_wf_ver_id.nn_wf_ver_id
        ver_id = models.NN_VER_WFLIST_INFO.objects.get(nn_id=nn_id, nn_wf_ver_id=nn_wf_ver_id).id
        if(len(models.NN_VER_BATCHLIST_INFO.objects.filter(nn_wf_ver_id=ver_id)) > 0) :
            return True
        else :
            return False

    def get_before_make_batch(self, node_id, nn_batch_ver_id):
        """
        find a batch version for eval, train
        :param node_id:
        :return:
        """
        netnode = models.NN_WF_NODE_INFO.objects.get(nn_wf_node_id=node_id)
        nn_id = netnode.wf_state_id.nn_id
        nn_wf_ver_id = netnode.wf_state_id.nn_wf_ver_id.nn_wf_ver_id
        ver_id = models.NN_VER_WFLIST_INFO.objects.get(nn_id=nn_id, nn_wf_ver_id=nn_wf_ver_id).id
        _before_batch_ver_id = nn_batch_ver_id.split('_')[-1]
        for _i in range(int(_before_batch_ver_id)-1,0,-1): #find maximun version before current batch version
            before_batch_ver_id = '_'.join([nn_id,str(nn_wf_ver_id),str(_i)])
            if(models.NN_VER_BATCHLIST_INFO.objects.filter(nn_batch_ver_id=before_batch_ver_id).exists()):
                return models.NN_VER_BATCHLIST_INFO.objects.get(nn_batch_ver_id=before_batch_ver_id)
        return None