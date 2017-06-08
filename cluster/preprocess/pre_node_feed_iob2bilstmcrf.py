from cluster.preprocess.pre_node_feed import PreNodeFeed


class PreNodeFeedIob2BiLstmCrf(PreNodeFeed):
    """

    """

    def run(self, conf_data):
        """
        override init class
        """
        super(PreNodeFeedIob2BiLstmCrf, self).run(conf_data)
        self._init_node_parm(conf_data['node_id'])

    def _convert_data_format(self, obj, index):
        pass

    def get_file_name(self):
        """
        get file name of current file pointer
        :return:
        """
        return self.input_paths[self.pointer]

