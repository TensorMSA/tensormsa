from django.core import serializers as serial
from master import models
from master import serializers
from django.db import connection
from common.utils import dictfetchall
import json

class WorkFlowStateMenu :

    """
    2. Table
    WF_TASK_MENU_RULE
    WF_TASK_SUBMENU_RULE

    """

    def get_serizied_menu_info(self):

        return None

    def get_menu_info(self):
        """
                get menu
                :return:
                """
        try:
            query_list = []
            query_list.append(" select wf_task_menu_id,wf_task_menu_name,wf_task_menu_desc ")
            query_list.append(" from master_wf_task_menu_rule menu ")

            # parm_list : set parm value as list
            parm_list = []
            with connection.cursor() as cursor:
                cursor.execute(''.join(query_list), parm_list)
                row = dictfetchall(cursor)
            return row
        except Exception as e:
            raise Exception(e)

    def get_submenu_info(self):

        return None

    def _serialize_menu_info(self):

        return None

    def get_submenu_id_with_name(self, name):

        return None

    def put_menu_info(self, input_data):
        """

        :param input_data:
        :return:
        """
        try:
            serializer = serializers.WF_TASK_MENU_RULE_Serializer(data=input_data)
            if serializer.is_valid():
                serializer.save()
        except Exception as e:
            raise Exception(e)
        finally:
            return input_data["wf_task_menu_id"]


    def put_submenu_info(self, input_data):
        """

        :param menu:
        :param input_data:
        :return:
        """
        try:
            serializer = serializers.WF_TASK_SUBMENU_RULE_Serializer(data=input_data)
            print(serializer.is_valid())
            if serializer.is_valid():
                serializer.save()
        except Exception as e:
            raise Exception(e)
        finally:
            return input_data["wf_task_submenu_id"]

    def put_graph_info(self, input_data):
        """

        :param menu:
        :param input_data:
        :return:
        """
        try:
            exists = models.GRAPH_FLOW_INFO.objects.filter(graph_flow_info_id=input_data["graph_flow_info_id"]
                                                         , graph_seq=input_data["graph_seq"]).count()
            if (exists > 0):
                obj = models.GRAPH_FLOW_INFO.objects.get(graph_flow_info_id=input_data["graph_flow_info_id"]
                                                         , graph_seq=input_data["graph_seq"])
                for key in input_data.keys():
                    if (input_data[key] != None):
                        setattr(obj, key, input_data[key])
                obj.save()
            else:
                serializer = serializers.GRAPH_FLOW_INFO_Serializer(data=input_data)
                print(serializer.is_valid())
                if serializer.is_valid():
                    serializer.save()
        except Exception as e:
            raise Exception(e)
        finally:
            return input_data["graph_node_name"]

    def get_graph_info(self, graphid):
        try:
            query_set = models.GRAPH_FLOW_INFO.objects.filter(graph_flow_info_id=graphid )
            query_set = serial.serialize("json", query_set)
            return json.loads(query_set)
        except Exception as e:
            raise Exception(e)

