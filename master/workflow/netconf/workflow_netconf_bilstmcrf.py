from master.workflow.netconf.workflow_netconf import WorkFlowNetConf
from master import models

class WorkFlowNetConfBiLstmCrf(WorkFlowNetConf):
    """

    """
    def __init__(self, key = None):
        """
        init key variable
        :param key:
        :return:
        """
        if key is not None :
            self.key = key
            self.conf = self.get_view_obj(key)

        self._set_key_parms([])
        self._set_prhb_parms([])

    @property
    def get_model_store_path(self):
        """
        getter for preprocess
        """
        return self.conf.get('model_path')

    @property
    def crf(self):
        """
        if sentence max lenghth is one you cannot usr crf layer
        """
        return_val = self.conf.get('crf')
        return True if return_val == None else return_val

    @property
    def chars(self):
        """
        if char embedding, training is 3.5x slower
        """
        return_val = self.conf.get('chars')
        return True if return_val == None else return_val

    @property
    def dim(self):
        """
        dimension size of word vector (must be equal to word embedding models vecotr size)
        """
        return_val = self.conf.get('dim')
        return 300 if return_val == None else return_val

    @property
    def dim_char(self):
        """
        if you use default vector it's ok to use default value
        """
        return_val = self.conf.get('dim_char')
        return 160 if return_val == None else return_val

    @property
    def max_iter(self):
        """
        set maximum iteration size (None : no limit)
        """
        return_val = self.conf.get('max_iter')
        return None if return_val == None else return_val

    @property
    def lowercase(self):
        """
        lowercase preprocess only needed for english
        """
        return_val = self.conf.get('lowercase')
        return False if return_val == None else return_val

    @property
    def train_embeddings(self):
        """
        choose to chagne word embedding vector or not (recommend False)
        """
        return_val = self.conf.get('train_embeddings')
        return False if return_val == None else return_val

    @property
    def nepochs(self):
        """
        iteration time of train
        """
        return_val = self.conf.get('nepochs')
        return 5 if return_val == None else return_val

    @property
    def p_dropout(self):
        """
        drop rate on train process
        """
        return_val = self.conf.get('p_dropout')
        return 0.5 if return_val == None else return_val

    @property
    def batch_size(self):
        """
        batch size on train
        """
        return_val = self.conf.get('batch_size')
        return 50 if return_val == None else return_val

    @property
    def p_lr(self):
        """
        learning rate
        """
        return_val = self.conf.get('p_lr')
        return 0.001 if return_val == None else return_val

    @property
    def lr_decay(self):
        """
        hyper parms on learning rate which chage learning rate on the middle of traing
        """
        return_val = self.conf.get('lr_decay')
        return 0.9 if return_val == None else return_val

    @property
    def nepoch_no_imprv(self):
        """
        early stop cehck rule (if there is no improvement on given amount of time, train will be stopeed)
        """
        return_val = self.conf.get('nepoch_no_imprv')
        return 3 if return_val == None else return_val

    @property
    def hidden_size(self):
        """
        rnn cell size for word
        """
        return_val = self.conf.get('hidden_size')
        return 300 if return_val == None else return_val

    @property
    def char_hidden_size(self):
        """
        rnn cell size for char
        """
        return_val = self.conf.get('char_hidden_size')
        return 100 if return_val == None else return_val