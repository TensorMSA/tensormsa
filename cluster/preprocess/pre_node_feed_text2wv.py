from cluster.preprocess.pre_node_feed import PreNodeFeed
import os,h5py

class PreNodeFeedText2Wv(PreNodeFeed):
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
