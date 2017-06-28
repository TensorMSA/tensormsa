from master.workflow.dataconf.workflow_dataconf import WorkFlowDataConf
from common import utils
from master import models

class WorkflowDataConfFrame(WorkFlowDataConf):
    """
    Data Columns의 속성을 정의 해주는 Class
    # properties
        data_conf
    """
    def __init__(self, key = None):
        """
        init key variable
        :param key:
        :return:
        """
        if (key is not None):
            self.key = key
            self.conf = self.get_step_source(key)

    @property
    def cell_feature(self):
        """
        getter for object type
        """
        return self.conf['cell_feature']
    @property
    def extend_cell_feature(self):
        """
        getter for object type
        """
        return self.conf['extend_cell_feature']
    @property
    def Transformations(self):
        """
        getter for object type
        """
        return self.conf['Transformations']
    @property
    def cross_cell(self):
        """
        getter for object type
        """
        return self.conf['cross_cell']
    @property
    def label_values(self):
        """
        getter for object type
        """
        return self.conf['label_values'] if ('label_values' in self.conf) else list()
    @property
    def label(self):
        """
        getter for object type
        """
        return self.conf['label']

    @property
    def label_type(self):
        """
        getter for object type
        """
        return self.conf['label_type']
    @property
    def cell_feature_unique(self):
        """
        getter for object type
        """
        return self.conf['cell_feature_unique']


    #data_conf
    def get_view_obj(self):
        """
        get column type info for view
        :return:
        """
        self._get_default_type()
        self._get_modified_type()

        return None

    def set_view_obj(self, obj):
        """
        set column type info on db json filed
        :param obj:
        :return:
        """
        return None

    def _get_default_type(self):
        """

        :return:
        """
        return None

    def _get_modified_type(self):
        """

        :return:
        """
        return None

    def _set_default_type(self):
        """

        :return:
        """
        return None

    def _set_modified_type(self):
        """

        :return:
        """
        return None

    def put_step_source(self, nnid, ver, node, input_data):
        """
        putter for source step
        :param obj: config data from view
        :return:boolean
        """
# "label":
# "Transformations":
# "cross_cell"
# "cell_feature":
# "extend_cell_feature":
# "label_values":

        try:
            obj = models.NN_WF_NODE_INFO.objects.get(nn_wf_node_id=str(nnid) + "_" + str(ver) + "_" + str(node))
            config_data = getattr(obj, 'node_config_data')
            #ternary operator if else statement
            config_data['label'] = input_data.get('label') if 'label' in input_data else config_data['label']
            config_data['Transformations'] = input_data.get('Transformations') if 'Transformations' in input_data else config_data['Transformations']
            config_data['cross_cell'] = input_data.get('cross_cell') if 'cross_cell' in input_data else config_data['cross_cell']
            config_data['cell_feature'] = input_data.get('cell_feature') if 'cell_feature' in input_data else config_data['cell_feature']
            config_data['extend_cell_feature'] = input_data.get('extend_cell_feature') if 'extend_cell_feature' in input_data else config_data['extend_cell_feature']
            config_data['label_values'] = input_data.get('label_values') if 'label_values' in input_data else config_data['label_values']
            config_data['label_type'] = input_data.get('label_type') if 'label_type' in input_data else config_data['label_type']
            config_data['cell_feature_unique'] = input_data.get('cell_feature_unique') if 'cell_feature_unique' in input_data else self.config_data_nvl(config_data, 'cell_feature_unique')
            setattr(obj, 'node_config_data', config_data)
            obj.save()
            return config_data
        except Exception as e:
            raise Exception(e)

    def get_data_conf(self, nnid, ver, node):
        """
        putter for source step
        :param obj: config data from view
        :return:boolean
        """
        # "label":
        # "Transformations":
        # "cross_cell"
        # "cell_feature":
        # "extend_cell_feature":
        # "label_values":

        try:
            obj = models.NN_WF_NODE_INFO.objects.get(nn_wf_node_id=str(nnid) + "_" + str(ver) + "_" + str(node))
            config_data = getattr(obj, 'node_config_data')
            return config_data
        except Exception as e:
            raise Exception(e)

    def config_data_nvl(self, config_data, attribute_name):

        if attribute_name in config_data:
            _value = config_data[attribute_name]
        else:
            _value = list()
        return _value

