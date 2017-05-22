from master.result.result_manager import ResultManager
from django.core import serializers as serial
from django.db.models import Max
from master import models
from master import serializers
from django.db import connection
from common.utils import dictfetchall
import json


class ResultManagerDefault(ResultManager) :
    """
    1. definition

    2. table

    """
    def get_view_obj(self,nnid, wf_id):
        """
        get view data for net config
        :return:
        """

        try:
            #query_set = models.TRAIN_SUMMARY_RESULT_INFO.objects.select_related(models.NN_VER_BATCHLIST_INFO).filter(nn_id=nnid, nn_wf_ver_id =wf_id)
            query_set = models.TRAIN_SUMMARY_RESULT_INFO.objects.select_related('nn_batch_ver_id').filter(nn_id=nnid, nn_wf_ver_id = wf_id, nn_batch_ver_id__eval_flag='Y')
            query_set = serial.serialize("json", query_set)
            return json.loads(query_set)
        except Exception as e:
            raise Exception(e)

    def set_view_obj(self,nnid, wf_id):
        """
        set net config data edited on view
        :param obj:
        :return:
        """
        pass