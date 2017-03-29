from cluster.preprocess.pre_node_feed import PreNodeFeed
import os,h5py

class PreNodeFeedText2Dv(PreNodeFeed):
    """

    """
    def _convert_data_format(self, file_path, index):
        """
        just pass hdf5 file chunk
        :param file_path:
        :param index:
        :return:
        """
        try:
            h5file = h5py.File(file_path, mode='r')
            raw_data = h5file['rawdata']
            return raw_data[index.start : index.stop]
        except Exception as e:
            raise Exception(e)
        finally:
            h5file.close()

    def data_size(self):
        try:
            h5file = h5py.File(self.input_paths[self.pointer], mode='r')
            return h5file['rawdata'].len()
        except Exception as e:
            raise Exception(e)
        finally:
            h5file.close()