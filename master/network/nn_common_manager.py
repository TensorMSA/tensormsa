from django.core import serializers as serial
from master import models
from master import serializers
import json

class NNCommonManager :
    """
    1. desc : CRUD function for Network Info
    2. table
        NN_DEF_LIST_INFO
        NN_VER_WFLIST_INFO
        NN_VER_BATCHLIST_INFO
    """

    def get_nn_info(self, condition):
        """
        search nn_info
        :return:
        """
        try:
            query_set = models.NN_DEF_LIST_INFO.objects.filter(nn_id__contains=condition['nn_id'], \
                                                               biz_cate__contains=condition['biz_cate'], \
                                                               biz_sub_cate__contains=condition['biz_sub_cate'])
            query_set = serial.serialize("json", query_set)
            return json.loads(query_set)
        except Exception as e:
            raise Exception(e)

    def delete_nn_info(self, nn_id_list):
        """
        deleted selected nn_info
        :param nn_id_list: list of nn_ids
        :return:
        """
        try:
            if (isinstance(nn_id_list, (str))):
                models.NN_DEF_LIST_INFO.objects.filter(nn_id__contains=nn_id_list).delete()
            elif (isinstance(nn_id_list, (list))):
                for d_id in nn_id_list:
                    models.NN_DEF_LIST_INFO.objects.filter(nn_id__contains=d_id).delete()
            else:
                return 'delete request data type is wrong'
            return nn_id_list
        except Exception as e:
            return e


    def update_nn_info(self, nn_id, obj):
        """
        update nn_info
        :param nn_id:
        :param obj : json object
        :return:
        """
        return None

    def insert_nn_info(self, req):
        """
        insert nn_info
        :param nn_id:
        :param obj : json object
        :return:
        """
        try:
            serializer = serializers.NN_DEF_LIST_INFO_Serializer(data=req)
            if serializer.is_valid():
                serializer.save()
        except Exception as e:
            raise Exception(e)
        finally:
            return req["nn_id"]
