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
        netnode = models.NN_WF_NODE_INFO.objects.get(nn_wf_node_id=node_id)
        nn_id = netnode.wf_state_id.nn_id
        nn_wf_ver_id = netnode.wf_state_id.nn_wf_ver_id.nn_wf_ver_id
        ver_id = models.NN_VER_WFLIST_INFO.objects.get(nn_id=nn_id, nn_wf_ver_id=nn_wf_ver_id).id
        train_batch_count = len(models.NN_VER_BATCHLIST_INFO.objects.filter(nn_wf_ver_id=ver_id, train_flag='Y'))
        if train_batch_count == 0 :
            train_batch = None
        elif train_batch_count == 1 :
            train_batch = models.NN_VER_BATCHLIST_INFO.objects.get(nn_wf_ver_id=ver_id, train_flag='Y').nn_batch_ver_id
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
        netnode = models.NN_WF_NODE_INFO.objects.get(nn_wf_node_id=node_id)
        nn_id = netnode.wf_state_id.nn_id
        nn_wf_ver_id = netnode.wf_state_id.nn_wf_ver_id.nn_wf_ver_id
        ver_id = models.NN_VER_WFLIST_INFO.objects.get(nn_id=nn_id, nn_wf_ver_id=nn_wf_ver_id).id
        batch = models.NN_VER_BATCHLIST_INFO.objects.get(nn_wf_ver_id=ver_id, active_flag='Y').nn_batch_ver_id
        return batch

    def get_eval_batch(selfself, node_id):
        netnode = models.NN_WF_NODE_INFO.objects.get(nn_wf_node_id=node_id)
        nn_id = netnode.wf_state_id.nn_id
        nn_wf_ver_id = netnode.wf_state_id.nn_wf_ver_id.nn_wf_ver_id
        ver_id = models.NN_VER_WFLIST_INFO.objects.get(nn_id=nn_id, nn_wf_ver_id=nn_wf_ver_id).id
        batch = models.NN_VER_BATCHLIST_INFO.objects.get(nn_wf_ver_id=ver_id, eval_flag='Y').nn_batch_ver_id
        return batch