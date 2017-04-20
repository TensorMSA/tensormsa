import numpy as np

class OneHotEncoder :
    """
    OneHot Encoder for batch train
    """
    def __init__(self, bucket_size, data_type=np.float):
        """
        initilize
        """
        self.bucket_size = bucket_size
        self.data_type = data_type
        self.pad = 0.
        self.bucket = np.zeros((self.bucket_size), dtype=data_type)
        self.dict_list = ['@','#','UNKNOWN']

    def restore(self, dict_list):
        """
        load dict_list from
        :param dict_list:
        :return:
        """
        for item in dict_list :
            self._set_item(item)

    def dics(self):
        """
        get dictionary list
        :return:
        """
        return self.dict_list

    def _set_item(self, item):
        """
        set item on bucket
        :param item:
        :return:
        """
        if item not in self.dict_list :
            if(self.bucket_size > len(self.dict_list)) :
                self.dict_list.append(item)

    def get_idx(self, item):
        """
        set item on bucket
        :param item:
        :return:
        """
        self._set_item(item)
        if item in self.dict_list :
            return self.dict_list.index(item)
        else :
            return self.get_idx("UNKNOWN")

    def get_vector(self, item):
        """
        get vector matrix of item
        :param item:
        :return:
        """
        try :
            self.bucket.fill(self.pad)
            idx = self.get_idx(item)
            if(idx >= 0 and (self.bucket_size > idx)) :
                np.put(self.bucket, idx, 1)
                return self.bucket.copy()
            else :
                return None
        except Exception as e :
            raise Exception ("get vector error !")

    def get_vocab(self, vector, prob_idx = 0, min_prob = 0.6):
        """
        get posb max item
        :param item: posb vector
        :return:
        """
        sorted_list = sorted(vector, reverse=True)
        idx = np.where(vector==sorted_list[prob_idx])[0][0]

        if(vector[idx] > min_prob) :
            return self.dict_list[idx]
        else :
            return "-1"


