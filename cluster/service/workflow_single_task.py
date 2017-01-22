from __future__ import absolute_import, unicode_literals
from celery import Task
import importlib


class WorkFlowSingleTask(Task):

    def run(self, source, *args, **kwargs):
        self.source = source

        self._run_single_node(source.nn_id , source.wf_ver)


    def _run_single_node(self, obj):
        """
        run given single node directly and return result
        :param obj: nn_id, ver, node and etc
        :return:
        """

        return object