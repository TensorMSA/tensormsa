from cluster.preprocess.pre_node_feed import PreNodeFeed


class PreNodeFeedFr2Cnn(PreNodeFeed):
    """

    """

    def run(self, conf_data):
        """
        override init class
        """
        super(PreNodeFeedFr2Cnn, self).run(conf_data)
        self._init_node_parm(conf_data['node_id'])

    def _convert_data_format(self, obj, index):
        pass

