from cluster.preprocess.pre_node_feed import PreNodeFeed
import os,h5py
import numpy as np

class PreNodeFeedText2FastText(PreNodeFeed):
    """

    """
    def run(self, conf_data):
        """
        override init class
        """
        super(PreNodeFeedText2FastText, self).run(conf_data)
        self._init_node_parm(conf_data['node_id'])


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
            data_set = raw_data[index.start: index.stop]
            filtered_data = [data_set[np.logical_not(data_set == '#')].tolist()]
            return filtered_data
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