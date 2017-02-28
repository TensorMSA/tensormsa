from __future__ import absolute_import, unicode_literals
import importlib
from celery import shared_task

@shared_task
def single_run(nn_id, wf_ver, node_id) :
    print ("[Train Task] Start Celery Job ")
    result = WorkFlowSingleTask()._run_single_node(nn_id, wf_ver, node_id)
    return result


class WorkFlowSingleTask():

    def _run_single_node(self, nn_id, wf_ver, node_id):
        """
        run given single node directly and return result
        :param obj: nn_id, ver, node and etc
        :return:
        """

        return object