import numpy as np
from common.utils.common_util import isnan

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
        self.add_flag = True

    def off_edit_mode(self):
        """
        off add dict mode
        :param dict_list:
        :return:
        """
        self.add_flag = False

    def on_edit_mode(self):
        """
        on add dict mode
        :param dict_list:
        :return:
        """
        self.add_flag = True

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
        try :
            if (self.add_flag == False) :
                pass
            if item not in self.dict_list :
                if(self.bucket_size > len(self.dict_list)) :
                    if (isnan(item) == False) :
                        self.dict_list.append(item)
        except Exception as e:
           raise Exception("get voc error !")

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
            if(item == '#') :
                return self.bucket.copy()

            idx = self.get_idx(item)
            if(idx >= 0 and (self.bucket_size > idx)) :
                np.put(self.bucket, idx, 1)
                return self.bucket.copy()
            else :
                return None
        except Exception as e :
            raise Exception ("get vector error !")

    def get_vocab(self, vector, prob_idx = 0, min_prob = 0.2):
        """
        get posb max item
        :param item: posb vector
        :return:
        """
        try :
            sorted_list = sorted(vector, reverse = True)
            idx = np.where(vector==sorted_list[prob_idx])[0][0]

            if(vector[idx] > min_prob) :
                return self.dict_list[idx]
            else :
                return "-1"
        except Exception as e :
            return "-1"


