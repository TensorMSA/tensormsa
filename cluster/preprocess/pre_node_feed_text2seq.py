from cluster.preprocess.pre_node_feed import PreNodeFeed
import os,h5py

class PreNodeFeedText2Seq(PreNodeFeed):
    """

    """

    def run(self, conf_data):
        """

        :param conf_data:
        :return:
        """
        super(PreNodeFeedText2Seq, self).run(conf_data)
        self.file_list_size = max([len(self.input_paths[0]), len(self.input_paths[1])])
        self._init_node_parm(conf_data['node_id'])

    def has_next(self):
        """
        check if hdf5 file pointer has next
        :return:
        """

        if(self.file_list_size > self.pointer) :
            return True
        else :
            return False

    def next(self):
        """
        move pointer +1
        :return:
        """
        if(self.has_next()) :
            self.pointer = self.pointer + 1

    def len(self):
        """

        :return:
        """
        return self.file_list_size

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

    def data_size(self):
        try:
            h5file = h5py.File(self.input_paths[self.pointer], mode='r')
            return h5file['rawdata'].len()
        except Exception as e:
            raise Exception(e)
        finally:
            h5file.close()