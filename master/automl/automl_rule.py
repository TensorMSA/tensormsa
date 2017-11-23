from common.utils import *
from master import models
from master import serializers
from django.core import serializers as serial
import json

class AutoMlRule:
    """
    Auto ML related conf get/set common methos
    """
    def __init__(self, key = None):
        """
        init key variable
        :param key:
        :return:
        """
        if (key is not None):
            self.key = key
            self.conf = self.get_train_obj(key)

    def get_graph_type_list(self, graph_id):
        """
        get view data for net config
        :return:
        """
        try:
            graph_id = str(graph_id)
            query_set = models.AUTO_ML_RULE.objects.all()
            query_set = serial.serialize("json", query_set)
            query_set = json.loads(query_set)
            ids = []
            for row in query_set :
                grow = row["fields"]["graph_flow_group_id"]
                active = row["fields"]["active_flag"]
                if grow.find(graph_id) > -1 and active == "Y":
                    ids.append(row)

            # obj = models.NN_DEF_LIST_INFO.objects.get(nn_id=str(input_data['nn_id']))

            return ids
        except Exception as e:
            raise Exception(e)

    def get_graph_info(self, graph_flow_id, type = None):
        """
        get view data for net config
        :return:
        """
        try:
            query_set = models.AUTO_ML_RULE.objects.filter(graph_flow_id=graph_flow_id)
            query_set = serial.serialize("json", query_set)
            query_set = json.loads(query_set)
            ids = []
            for row in query_set :
                ids.append(row)
            return ids
        except Exception as e:
            raise Exception(e)


    def set_graph_type_list(self, graph_flow_id, req):
        """
        insert nn_info
        :param req: json object
        :return:
        """
        try:
            exists = models.AUTO_ML_RULE.objects.filter(graph_flow_id=graph_flow_id).count()
            if(exists > 0) :
                self.update_graph_type_list(graph_flow_id, req)
            else :
                obj = models.AUTO_ML_RULE.objects.create(graph_flow_id=graph_flow_id,
                                                         graph_flow_data={},
                                                         graph_flow_data_single={})
                setattr(obj, "graph_flow_data", req['auto'])
                setattr(obj, "graph_flow_data_single", req['single'])
                obj.save()
        except Exception as e:
            raise Exception(e)
        finally:
            return True

    def update_graph_type_list(self, graph_flow_id, input_data):
        """
        set net config data edited on view
        :param obj:
        :return:
        """
        try:
            exists = models.AUTO_ML_RULE.objects.filter(graph_flow_id=graph_flow_id).count()
            if (exists > 0):
                obj = models.AUTO_ML_RULE.objects.get(graph_flow_id=graph_flow_id)
                setattr(obj, "graph_flow_data", input_data['auto'])
                setattr(obj, "graph_flow_data_single", input_data['single'])
                obj.save()
            else:
                for i in input_data:
                    exists = models.AUTO_ML_RULE.objects.filter(graph_flow_id=i).count()
                    if (exists > 0):
                        obj = models.AUTO_ML_RULE.objects.get(graph_flow_id=i)
                        setattr(obj, graph_flow_id, input_data[i])
                        obj.save()

            return input_data
        except Exception as e:
            raise Exception(e)
        return None

