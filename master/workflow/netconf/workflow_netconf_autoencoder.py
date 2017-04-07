from master.workflow.netconf.workflow_netconf import WorkFlowNetConf

class WorkFlowNetConfAutoEncoder(WorkFlowNetConf):
    """

    """
    def validation_check(self, json_data):
        error_msg = ""
        if ('display_step' not in json_data):
            error_msg = ''.join([error_msg, 'display_step (str) not defined'])
        if ('learning_rate' not in json_data):
            error_msg = ''.join([error_msg, 'learning_rate (int) not defined'])
        if ('batch_size' not in json_data):
            error_msg = ''.join([error_msg, 'batch_size (int) not defined'])
        if ('batch_size' not in json_data):
            error_msg = ''.join([error_msg, 'batch_size (int) not defined'])
        if ('training_epochs' not in json_data):
            error_msg = ''.join([error_msg, 'training_epochs (int) not defined'])
        if (error_msg == ""):
            return True
        else:
            raise Exception (error_msg)