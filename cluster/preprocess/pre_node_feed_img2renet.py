from cluster.preprocess.pre_node_feed import PreNodeFeed
import h5py


class PreNodeFeedImg2Renet(PreNodeFeed):
    """

    """

    def _convert_data_format(self, file_path, index):
        try:
            rawdata = file_path['image_features']
            targets = file_path['targets']
            return rawdata[index.start: index.stop], targets[index.start: index.stop]
        except Exception as e:
            raise Exception(e)