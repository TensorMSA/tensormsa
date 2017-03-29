from cluster.preprocess.pre_node_feed import PreNodeFeed
import h5py


class PreNodeFeedImg2Renet(PreNodeFeed):
    """

    """

    def _convert_data_format(self, file_path, index):
        try:
            h5file = h5py.File(file_path, mode='r')
            rawdata = h5file['image_features']
            targets = h5file['targets']
            return rawdata[index.start: index.stop], targets[index.start: index.stop]
        except Exception as e:
            raise Exception(e)
        finally:
            h5file.close()

    def data_size(self):
        try:
            h5file = h5py.File(self.input_paths[self.pointer], mode='r')
            rawdata = h5file['image_features']
            return rawdata.len()
        except Exception as e:
            raise Exception(e)
        finally:
            h5file.close()