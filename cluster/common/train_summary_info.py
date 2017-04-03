class TrainSummaryInfo:
    def __init__(self,config):
        self.nn_id = ''
        self.nn_wf_ver_id = ''
        self.nn_batch_ver_id = ''
        if config["type"] == 'regression':
            self.result_info = {"labels":[], "predicts":[]}
        elif config["type"] == 'category':
            predicts = [[0 for col in range(len(config["labels"]))] for row in range(len(config["labels"]))]
            for i in range(0, len(config["labels"]) - 1, 1):
                for j in range(0, len(config["labels"]) - 1, 1):
                    predicts[i][j] = 0
            self.result_info = {"labels": config["labels"], "predicts": predicts}
        self.acc_info = []
        self.loss_info = []
        self.type = config["type"]
        self.labels = config["labels"]

    def get_nn_id(self):
        return self.nn_id

    def set_nn_id(self, nn_id):
        self.nn_id = nn_id

    def get_nn_wf_ver_id(self):
        return self.nn_batch_ver_id

    def set_nn_wf_ver_id(self, nn_wf_ver_id):
        self.nn_wf_ver_id = nn_wf_ver_id

    def get_nn_batch_ver_id(self):
        return self.nn_batch_ver_id

    def set_nn_batch_ver_id(self, nn_batch_ver_id):
        self.nn_batch_ver_id = nn_batch_ver_id

    def get_result_info(self):
        return self.result_info

    def set_result_info(self, label, predict):
        if self.type == 'regression':
            labels = self.result_info["labels"]
            labels.append(label)
            self.result_info["labels"] = labels
            predicts = self.result_info["predicts"]
            predicts.append(predict)
            self.result_info["predicts"] = predicts
        elif self.type == 'category':
            i = self.labels.index(label)
            j = self.labels.index(predict)
            predicts = self.result_info["predicts"]
            predicts[i][j] = predicts[i][j] + 1
            self.result_info["predicts"] = predicts

    def get_acc_info(self):
        return self.acc_info

    def set_acc_info(self, acc_info):
        self.acc_info.append(acc_info)

    def get_loss_info(self):
        return self.loss_info

    def set_loss_info(self, loss_info):
        self.loss_info.append(loss_info)