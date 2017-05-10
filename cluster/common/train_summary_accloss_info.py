class TrainSummaryAccLossInfo:
    def __init__(self, conf = None):
        """
        set type of result form is necessary
        :param type:
        """
        self.nn_id = ''
        self.nn_wf_ver_id = ''
        self.nn_batch_ver_id = ''
        self.acc_info = {"acc":[]}
        self.loss_info = {"loss":[]}
        if(conf) :
            self.nn_id = conf.get('nn_id')
            self.nn_wf_ver_id = conf.get('nn_wf_ver_id')
            self.nn_batch_ver_id = conf.get('nn_batch_ver_id')

    def get_nn_id(self):
        return self.nn_id

    def set_nn_id(self, nn_id):
        self.nn_id = nn_id

    def get_nn_wf_ver_id(self):
        return self.nn_wf_ver_id

    def set_nn_wf_ver_id(self, nn_wf_ver_id):
        self.nn_wf_ver_id = nn_wf_ver_id

    def get_nn_batch_ver_id(self):
        return self.nn_batch_ver_id

    def set_nn_batch_ver_id(self, nn_batch_ver_id):
        self.nn_batch_ver_id = nn_batch_ver_id

    def get_acc_info(self):
        return self.acc_info

    def set_acc_info(self, acc):
        self.acc_info["acc"].append(str(acc))

    def get_loss_info(self):
        return self.loss_info

    def set_loss_info(self, loss):
        self.loss_inf["loss"].append(str(loss))