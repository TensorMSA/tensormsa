from cluster.preprocess.pre_node_feed import PreNodeFeed
import os,h5py

class PreNodeFeedText2Seq(PreNodeFeed):
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
            encode = h5py.File(file_path[0], mode='r')['rawdata']
            decode = h5py.File(file_path[1], mode='r')['rawdata']
            return encode[index.start : index.stop], decode[index.start : index.stop]
        except Exception as e:
            raise Exception(e)
        finally:
            encode.close()
            decode.close()
