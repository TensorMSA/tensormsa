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

        return None

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



