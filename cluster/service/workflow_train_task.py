from __future__ import absolute_import, unicode_literals
from celery import Task


class WorkFlowTrainTask(Task):

    def run(self, source, *args, **kwargs):
        self.source = source

    def _exec_train(self):
        return None

    def _exec_node(self):
        return None

    def _stop_task(self):
        return None

    def _get_arranged_node_list(self):
        return None

    def _get_next_exec_node(self):
        return None

    def _run_next_node(self):
        return None

    def _check_node_job_state(self):
        return None

    def _report_server_state(self):
        return None

    def _report_job_state(self):
        return None










