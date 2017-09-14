from common.utils import *
from master import models

class AutoMlCommon:
    """
    Auto ML related conf get/set common methos
    """
    def __init__(self, key = None):
        """
        init key variable
        :param key:
        :return:
        """
        if (key is not None):
            self.key = key
            self.parm_info = self.get_parm_obj(key)
            self.conf_info = self.get_conf_obj(key)
            self.stat_info = self.get_stat_obj(key)
            self.net_type = self.get_net_type(key)


    def get_conf_obj(self, nn_id):
        """
        get view data for automl_parms
        :return:
        """
        try:
            obj = models.NN_DEF_LIST_INFO.objects.get(nn_id=nn_id)
            return getattr(obj, "automl_parms")
        except Exception as e:
            raise Exception(e)

    def update_conf_obj(self, nn_id, input_data):
        """
        update json filed with given data
        :param obj:
        :return:
        """
        try:
            obj = models.NN_DEF_LIST_INFO.objects.get(nn_id=nn_id)
            data_set = getattr(obj, "automl_parms")
            data_set.update(input_data)
            setattr(obj, "automl_parms", data_set)
            obj.save()
            return input_data
        except Exception as e:
            raise Exception(e)

    def get_stat_obj(self, nn_id):
        """
        get view data for net config
        :return:
        """
        try:
            obj = models.NN_DEF_LIST_INFO.objects.get(nn_id=nn_id)
            return getattr(obj, "automl_stat")
        except Exception as e:
            raise Exception(e)

    def update_stat_obj(self, nn_id, input_data):
        """
        set net config data edited on view
        :param obj:
        :return:
        """
        try:
            obj = models.NN_DEF_LIST_INFO.objects.get(nn_id=nn_id)
            data_set = getattr(obj, "automl_stat")
            data_set['bygen'] = data_set['bygen'] + (input_data['bygen'])
            data_set['best'] = input_data['best']
            setattr(obj, "automl_stat", data_set)
            obj.save()
            return data_set
        except Exception as e:
            raise Exception(e)

    def reset_stat_obj(self, nn_id):
        """
        set net config data edited on view
        :param obj:
        :return:
        """
        try:
            obj = models.NN_DEF_LIST_INFO.objects.get(nn_id=nn_id)
            data_set = {}
            data_set['bygen'] = []
            data_set['best'] = []
            setattr(obj, "automl_stat", data_set)
            obj.save()
            return data_set
        except Exception as e:
            raise Exception(e)

    def get_parm_obj(self, nn_id):
        """
        get view data for automl_parms
        :return:
        """
        try:
            obj = models.NN_DEF_LIST_INFO.objects.get(nn_id=nn_id)
            return getattr(obj, "automl_runtime")
        except Exception as e:
            raise Exception(e)

    def update_parm_obj(self, nn_id, input_data):
        """
        update json filed with given data
        :param obj:
        :return:
        """
        try:
            obj = models.NN_DEF_LIST_INFO.objects.get(nn_id=nn_id)
            data_set = getattr(obj, "automl_runtime")
            data_set.update(input_data)
            setattr(obj, "automl_runtime", data_set)
            obj.save()
            return input_data
        except Exception as e:
            raise Exception(e)

    def get_net_type(self, nn_id):
        """
        get net type on data base
        :return:
        """
        try:
            obj = models.NN_DEF_LIST_INFO.objects.get(nn_id=nn_id)
            return getattr(obj, "dir")
        except Exception as e:
            raise Exception(e)

    def update_net_type(self, nn_id, input_data):
        """
        update net type with given data
        :param obj:
        :return:
        """
        try:
            obj = models.NN_DEF_LIST_INFO.objects.get(nn_id=nn_id)
            data_set = getattr(obj, "dir")
            data_set.update(input_data)
            setattr(obj, "dir", data_set)
            obj.save()
            return input_data
        except Exception as e:
            raise Exception(e)