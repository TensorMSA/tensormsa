from cluster.preprocess.pre_node_feed import PreNodeFeed
import os,h5py

class PreNodeFeedText2Seq(PreNodeFeed):
    """

    """
    def __getitem__(self, key):
        """

        :param key:
        :return:
        """
        encode = self._convert_data_format(self.input_paths[0][self.pointer], key)
        decode = self._convert_data_format(self.input_paths[1][self.pointer], key)
        return encode, decode

    def _convert_data_format(self, file_path, index):
        """
        just pass hdf5 file chunk
        :param file_path:
        :param index:
        :return:
        """
        try:
            h5file = h5py.File(file_path, mode='r')
            rawfile = h5file['rawdata']
            return rawfile[index.start : index.stop]
        except Exception as e:
            raise Exception(e)
        finally:
            h5file.close()
