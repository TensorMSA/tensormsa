from cluster.common.common_node import WorkFlowCommonNode
from django.db import connection
from common.utils import *

class PredictNet(WorkFlowCommonNode):
    """

    """

    def run(self, nn_id, parm={}):
        pass

    def _valid_check(self):
        pass

    def _find_netconf_node_id(self, nn_id):
        """
        return node id of netconf
        :param nn_id:
        :param version:
        :return:
        """

        # make query string (use raw query only when cate is too complicated)
        query_list = []
        query_list.append("SELECT NI.NN_WF_NODE_ID  ")
        query_list.append("FROM MASTER_NN_VER_WFLIST_INFO WV JOIN MASTER_NN_WF_STATE_INFO WS   ")
        query_list.append("     ON WV.NN_WF_VER_ID =  WS.NN_WF_VER_ID_ID    ")
        query_list.append("     AND WV.ACTIVE_FLAG = 'Y'    ")
        query_list.append("     AND WV.NN_ID_ID = %s    ")
        query_list.append("     JOIN MASTER_NN_WF_NODE_INFO NI    ")
        query_list.append("     ON WS.WF_STATE_ID = NI.WF_STATE_ID_ID    ")
        query_list.append("     JOIN MASTER_WF_TASK_SUBMENU_RULE SR  ")
        query_list.append("     ON SR.WF_TASK_SUBMENU_ID = NI.WF_TASK_SUBMENU_ID_ID    ")
        query_list.append("     AND SR.WF_TASK_MENU_ID_ID = 'netconf'")

        # parm_list : set parm value as list
        parm_list = []
        parm_list.append(nn_id)

        with connection.cursor() as cursor:
            cursor.execute(''.join(query_list), parm_list)
            row = dictfetchall(cursor)
        if(len(row) > 0):
            return row[0]['nn_wf_node_id']
        else :
            raise Exception ("No Active version Exist for predict service !")