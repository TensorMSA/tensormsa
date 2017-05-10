class TrainSummaryInfo:
    def __init__(self, conf = None, type=None):
        """
        set type of result form is necessary
        :param type:
        """
        self.nn_id = ''
        self.nn_wf_ver_id = ''
        self.nn_batch_ver_id = ''

        if(type) :
            self.type = type

        if(conf) :
            self.type = conf.get('type')
            self.set_result_data_format(conf)
            self.nn_id = conf.get('nn_id')
            self.nn_wf_ver_id = conf.get('nn_wf_ver_id')
            self.nn_batch_ver_id = conf.get('nn_batch_ver_id')

    def set_result_data_format(self, config):
        """
        set config parms and result form is necessary before use
        :param config:
        :return:
        """
        if self.type == 'regression':
            self.result_info = {"labels":[], "predicts":[]}
        elif self.type == 'category':
            predicts = [[0 for col in range(len(config["labels"]))] for row in range(len(config["labels"]))]
            for i in range(0, len(config["labels"]) - 1, 1):
                for j in range(0, len(config["labels"]) - 1, 1):
                    predicts[i][j] = 0
            self.result_info = {"labels": config["labels"], "predicts": predicts}
            self.labels = config["labels"]
        elif self.type == 'w2v':
            self.result_info = {"word":[], "x":[], "y":[]}
        elif self.type == 'seq2seq':
            self.result_info = {"question":[], "answer":[], "predict":[], "accuracy":[]}

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

    def get_result_info(self):
        return self.result_info

    def set_result_info(self, label, predict, input=None, acc=None, coord_x=None, coord_y=None):
        if self.type == 'regression':
            labels = self.result_info["labels"]
            labels.extend(label)
            self.result_info["labels"] = labels
            predicts = self.result_info["predicts"]
            predicts.extend(predict)
            self.result_info["predicts"] = predicts
        elif self.type == 'category':
            i = self.labels.index(label)
            j = self.labels.index(predict)
            predicts = self.result_info["predicts"]
            predicts[i][j] = predicts[i][j] + 1
            self.result_info["predicts"] = predicts
        elif self.type == 'w2v':
            raise Exception ("Eval for W2V is on development now")
        elif self.type == 'seq2seq':
            self.result_info['question'].append(input)
            self.result_info['answer'].append(label)
            self.result_info['predict'].append(predict)
            self.result_info['accuracy'].append(acc)