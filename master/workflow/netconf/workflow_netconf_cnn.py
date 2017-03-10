from master.workflow.netconf.workflow_netconf import WorkFlowNetConf
from common.utils import *
from master import models
from django.core import serializers as serial
import json

class WorkFlowNetConfCNN(WorkFlowNetConf):
    """

    """


    def validation_check(self, json_data):
        return True