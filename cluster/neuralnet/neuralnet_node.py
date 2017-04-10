from cluster.common.common_node import WorkFlowCommonNode

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
