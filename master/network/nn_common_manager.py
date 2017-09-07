from django.core import serializers as serial
from django.db.models import Max
from master import models
from master import serializers
from django.db import connection
from common.utils import dictfetchall
import json

class NNCommonManager :
    """
    1. desc : CRUD function for Network Info
    2. table
        NN_DEF_LIST_INFO
        NN_VER_WFLIST_INFO
        NN_VER_BATCHLIST_INFOs
    """
    def get_nn_id_max(self):
        try:
            query_set = models.NN_DEF_LIST_ID_INFO.objects.filter().aggregate(Max('id'))
            return_value = query_set['id__max']
            if query_set['id__max'] == None:
                return_value = 0
            return return_value

        except Exception as e:
            raise Exception(e)

    def get_nn_id_info(self, nn_id):
        """
        update nn_info
        :param nn_id:
        :param obj : json object
        :return:
        """
        try:
            query_set = models.NN_DEF_LIST_INFO.objects.filter(nn_id=nn_id)
            query_set = serial.serialize("json", query_set)
            return json.loads(query_set)
        except Exception as e:
            raise Exception(e)

    def get_nn_info(self, condition):
        """
        search nn_info
        :return:
        """
        try:
            # make query string (use raw query only when cate is too complicated)
            query_list = []
            query_list.append("SELECT * ")
            query_list.append("FROM  master_NN_DEF_LIST_INFO NL LEFT OUTER JOIN master_NN_VER_WFLIST_INFO WF ")
            query_list.append("      ON NL.nn_id = WF.nn_id_id AND WF.active_flag = 'Y' ")
            query_list.append("      LEFT OUTER JOIN master_NN_VER_BATCHLIST_INFO BT ")
            query_list.append("      ON wf.nn_id_id||'_'||wf.nn_wf_ver_id = substr(bt.nn_batch_ver_id,1,length(wf.nn_id_id||'_'||wf.nn_wf_ver_id)) ")
            if condition['nn_id'] == '%':
                query_list.append("      AND BT.eval_flag = 'Y' ")
            else:
                query_list.append("      AND BT.active_flag = 'Y' ")
            query_list.append("WHERE NL.nn_id like %s ")
            query_list.append("  AND NL.biz_cate like %s ")
            query_list.append("  AND NL.biz_sub_cate like %s ")
            query_list.append("  AND NL.use_flag = 'Y' ")

            # parm_list : set parm value as list
            parm_list = []
            parm_list.append("%" + ('' if condition.get("nn_id") is None else condition.get("nn_id")))
            parm_list.append("%" + ('' if condition.get("biz_cate") is None else condition.get("biz_cate")))
            parm_list.append("%" + ('' if condition.get("biz_sub_cate") is None else condition.get("biz_sub_cate")))

            with connection.cursor() as cursor:
                cursor.execute(''.join(query_list), parm_list)
                row = dictfetchall(cursor)
            return row
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


    def update_nn_info(self, input_data):
        """
        update nn_info
        :param nn_id:
        :param obj : json object
        :return:
        """
        try:
            obj = models.NN_DEF_LIST_INFO.objects.get(nn_id=str(input_data['nn_id']))
            for key in input_data.keys():
                if (input_data[key] != None):
                    setattr(obj, key, input_data[key])
            obj.save()
            return str(input_data['nn_id'])
        except Exception as e:
            raise Exception(e)


    def insert_nn_info(self, req, reqs):
        """
        insert nn_info
        :param req: json object
        :return:
        """
        try:
            serializer1 = serializers.NN_DEF_LIST_INFO_Serializer(data=req)
            if serializer1.is_valid():
                serializer1.save()
        except Exception as e:
            raise Exception(e)

        try:
            serializer2 = serializers.NN_DEF_LIST_ID_INFO_Serializer(data=reqs)
            if serializer2.is_valid():
                serializer2.save()
        except Exception as e:
            raise Exception(e)
        finally:
            return req["nn_id"]


    def insert_nn_wf_info(self, req):
        """
        insert nn_info version data
        :param req:
        :return:
        """
        try:
            serializer = serializers.NN_VER_WFLIST_INFO_Serializer(data=req)
            if serializer.is_valid():
                serializer.save()
        except Exception as e:
            raise Exception(e)
        finally:
            return req["nn_wf_ver_id"]

    def update_nn_wf_info(self, nn_id, up_data):
        """
        update nn_info
        :param nn_id:
        :param obj : json object
        :return:
        """
        try:
            # set all other version info active tag to false
            if(up_data['active_flag'] == 'Y'):
                query_list = models.NN_VER_WFLIST_INFO.objects.filter(nn_id=nn_id)
                for query_item in query_list:
                    query_item.active_flag = 'N'
                    query_item.save()

            # update user request
            obj = models.NN_VER_WFLIST_INFO.objects.get(nn_id=nn_id,
                                                        nn_wf_ver_id=str(up_data['nn_wf_ver_id']))
            for key in up_data.keys():
                if (up_data[key] != None):
                    setattr(obj, key, up_data[key])
            obj.save()
            return str(up_data['nn_wf_ver_id'])
        except Exception as e:
            raise Exception(e)

    def get_nn_wf_info(self, nn_id):
        """
        search nn_wf_info
        :return:
        """

        try:
            # make query string (use raw query only when cate is too complicated)
            query_list = []
            query_list.append(" select nn_wf.nn_id_id nn_id ")
            query_list.append("	     ,nn_wf.nn_wf_ver_id ")
            query_list.append("      ,nn_wf.wf_active_flag active_flag ")
            query_list.append("      ,nn_wf.nn_batch_ver_id train_batch_ver_id ")
            query_list.append("      ,nn_wf.train_acc_info ")
            query_list.append("      ,nn_wf.train_loss_info ")
            query_list.append("      ,nn_wf.nn_wf_ver_desc ")
            query_list.append("      ,btp.nn_batch_ver_id pred_batch_ver_id ")
            query_list.append("      ,smp.acc_info pred_acc_info ")
            query_list.append("      ,smp.loss_info pred_loss_info ")
            query_list.append("      ,smrt.result_info t_result_info ")
            query_list.append("      ,smrp.result_info p_result_info ")
            query_list.append(" from( ")
            query_list.append("      SELECT wf.nn_id_id ")
            query_list.append("      	    ,wf.nn_wf_ver_id ")
            query_list.append("      	    ,wf.nn_id_id||'_'||wf.nn_wf_ver_id as status_id ")
            query_list.append("      	    ,wf.active_flag wf_active_flag ")
            query_list.append("      	    ,wf.nn_wf_ver_desc ")
            query_list.append("      	    ,btt.nn_batch_ver_id ")
            query_list.append("      	    ,btt.active_flag bt_active_flag ")
            query_list.append("      	    ,smt.acc_info train_acc_info ")
            query_list.append("      	    ,smt.loss_info train_loss_info ")
            query_list.append("      	FROM	master_NN_DEF_LIST_INFO nl ")
            query_list.append("      			LEFT OUTER JOIN master_NN_VER_WFLIST_INFO wf ON nl.nn_id = wf.nn_id_id ")
            query_list.append("      				LEFT OUTER JOIN master_NN_VER_BATCHLIST_INFO btt ")
            query_list.append("      					ON wf.nn_id_id||'_'||wf.nn_wf_ver_id = substr(btt.nn_batch_ver_id,1,length(wf.nn_id_id||'_'||wf.nn_wf_ver_id)) ")
            query_list.append("      					and btt.eval_flag = 'Y' ")
            query_list.append("      					LEFT OUTER JOIN master_train_summary_accloss_info smt ")
            query_list.append("      						ON btt.nn_batch_ver_id = smt.nn_batch_ver_id_id	) nn_wf ")
            query_list.append("      		LEFT OUTER JOIN master_NN_VER_BATCHLIST_INFO btp ")
            query_list.append("      			ON nn_wf.status_id = substr(btp.nn_batch_ver_id,1,length(nn_wf.status_id)) ")
            query_list.append("      			and btp.active_flag = 'Y' ")
            query_list.append("      			LEFT OUTER JOIN master_train_summary_accloss_info smp ")
            query_list.append("      				ON btp.nn_batch_ver_id = smp.nn_batch_ver_id_id ")
            query_list.append("      		LEFT OUTER JOIN master_train_summary_result_info smrt ")
            query_list.append("      		    ON nn_wf.nn_batch_ver_id = smrt.nn_batch_ver_id_id ")
            query_list.append("      		LEFT OUTER JOIN master_train_summary_result_info smrp ")
            query_list.append("      		    ON btp.nn_batch_ver_id = smrp.nn_batch_ver_id_id ")

            query_list.append("WHERE nn_id_id like %s ")
            query_list.append("  order by nn_wf.nn_id_id, nn_wf.nn_wf_ver_id ")

            # parm_list : set parm value as list
            parm_list = []
            parm_list.append(nn_id)

            with connection.cursor() as cursor:
                cursor.execute(''.join(query_list), parm_list)
                row = dictfetchall(cursor)
            return row
        except Exception as e:
            raise Exception(e)

    def get_nn_max_ver(self, nn_id):
        try:
            query_set = models.NN_VER_WFLIST_INFO.objects.filter(nn_id=nn_id).aggregate(Max('nn_wf_ver_id'))
            return_value = query_set['nn_wf_ver_id__max']
            if query_set['nn_wf_ver_id__max'] == None:
                return_value = 0
            return return_value

        except Exception as e:
            raise Exception(e)

    def get_nn_batch_info(self, nn_id, ver):
        """
        search nn_batch_info
        :return:
        """
        try:
            # make query string (use raw query only when cate is too complicated)
            query_list = []
            query_list.append(" select wf.nn_id_id ")
            query_list.append("		    ,wf.nn_wf_ver_id ")
            query_list.append("	        ,bt.nn_batch_ver_id ")
            query_list.append("      	,bt.active_flag ")
            query_list.append("      	,bt.eval_flag ")
            query_list.append("      	,sm.acc_info ")
            query_list.append("      	,sm.loss_info ")
            query_list.append("      	,smr.result_info ")
            query_list.append(" from master_NN_VER_WFLIST_INFO wf ")
            query_list.append(" 	,master_NN_VER_BATCHLIST_INFO bt ")
            query_list.append(" 		LEFT OUTER JOIN master_train_summary_accloss_info sm ")
            query_list.append(" 			ON bt.nn_batch_ver_id = sm.nn_batch_ver_id_id ")
            query_list.append(" 		LEFT OUTER JOIN master_train_summary_result_info smr ")
            query_list.append(" 			ON bt.nn_batch_ver_id = smr.nn_batch_ver_id_id ")
            query_list.append(" where wf.nn_id_id||'_'||wf.nn_wf_ver_id = substr(bt.nn_batch_ver_id,1,length(wf.nn_id_id||'_'||wf.nn_wf_ver_id)) ")


            query_list.append(" and wf.nn_id_id = %s ")
            query_list.append(" and wf.nn_wf_ver_id = %s ")

            # parm_list : set parm value as list
            parm_list = []
            parm_list.append(nn_id)
            parm_list.append(ver)

            with connection.cursor() as cursor:
                cursor.execute(''.join(query_list), parm_list)
                row = dictfetchall(cursor)
            return row
        except Exception as e:
            raise Exception(e)

    def update_nn_batch_info(self, nn_id, ver, up_data):
        """
        update nn_info
        :param nn_id:
        :param obj : json object
        :return:
        """
        try:
            # update user request
            obj = models.NN_VER_BATCHLIST_INFO.objects.get(nn_batch_ver_id=str(up_data['nn_batch_ver_id']))
            for key in up_data.keys():
                if (up_data[key] != None):
                    setattr(obj, key, up_data[key])
            obj.save()
            return str(up_data['nn_batch_ver_id'])
        except Exception as e:
            raise Exception(e)

    def get_nn_node_info(self, nn_id, ver, desc):
        """
        update nn_info
        :param nn_id:
        :param obj : json object
        :return:
        """
        try:
            state_id = nn_id+"_"+ver
            if(desc != None and desc == "all"):
                query_set = models.NN_WF_NODE_INFO.objects.filter(wf_state_id=state_id)
            else:
                query_set = models.NN_WF_NODE_INFO.objects.filter(wf_state_id=state_id, nn_wf_node_desc=desc )
            query_set = serial.serialize("json", query_set)
            return json.loads(query_set)
        except Exception as e:
            raise Exception(e)

