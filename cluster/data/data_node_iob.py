from cluster.data.data_node import DataNode
from master.workflow.data.workflow_data_iob import WorkFlowDataIob
from common import utils
import os,h5py
from time import gmtime, strftime
from cluster.service.service_predict_w2v import PredictNetW2V
from common.utils import *
from cluster.common.neural_common_bilismcrf import BiLstmCommon

class DataNodeIob(DataNode, BiLstmCommon):


    def run(self, conf_data):
        """
        run on train time
        data node collect data from source, preprocess data and sotre it on NAS
        :param conf_data:
        :return:
        """
        self._init_node_parm(conf_data['node_id'])
        if(self.data_src_type == 'local') :
            self.src_local_handler(conf_data)
        if (self.data_src_type == 'rdb'):
            raise Exception ("on development now")
        if (self.data_src_type == 's3'):
            raise Exception("on development now")
        if (self.data_src_type == 'hbase'):
            raise Exception("on development now")

    def src_local_handler(self, conf_data):
        """
        read data from local file system
        :param conf_data:
        :return:
        """
        try:
            # init value
            vocab_words = None
            vocab_tags = None
            vocab_chars = None

            # get word embedding model
            parm = {"type": "model", "val_1": {}, "val_2": []}
            embed_model = PredictNetW2V().run(self.word_embed_model, parm)

            # read files from srouce folder (handle one by one)
            fp_list = utils.get_filepaths(self.data_src_path, file_type='iob')
            if (len(fp_list) == 0):
                return None

            netconf_node = self.get_linked_next_node_with_grp('netconf')
            if (len(netconf_node) > 0 ) :
                store_path = get_model_path(netconf_node[0].get_net_id(),
                                            netconf_node[0].get_net_ver(),
                                            netconf_node[0].get_net_node_id())

                # create dict folder for ner if not exists
                netconf_path = ''.join([store_path, '/dict/'])
                if not os.path.exists(netconf_path):
                    os.makedirs(netconf_path)

                vocab_words = self.load_vocab(''.join([netconf_path, 'words.txt']))
                vocab_tags = self.load_vocab(''.join([netconf_path, 'tags.txt']))
            else :
                return None

            for file_path in fp_list :
                # Data Generators
                dev = self.CoNLLDataset(file_path)
                train = self.CoNLLDataset(file_path)

                # get distinct vocab and chars
                vocab_words, vocab_tags = self.get_vocabs([train, dev], vocab=vocab_words, tags=vocab_tags)
                vocab = vocab_words & set(embed_model.wv.index2word)
                vocab.add(self.UNK)
                vocab_chars = self.get_char_vocab(train, chars=vocab_chars)

            # write dict and vecotors for train
            self.write_char_embedding(vocab_chars, ''.join([netconf_path, 'char.vec']))
            self.write_vocab(vocab_chars, ''.join([netconf_path, 'chars.txt']))
            self.write_vocab(vocab, ''.join([netconf_path, 'words.txt']))
            self.write_vocab(vocab_tags, ''.join([netconf_path, 'tags.txt']))
            self.export_trimmed_glove_vectors(vocab, embed_model, ''.join([netconf_path, 'words.vec']))

        except Exception as e:
            raise Exception(e)
        finally :
            for file_path in fp_list:
                # move source file to store path
                str_buf = self._load_local_files(file_path)
                self._save_raw_file(str_buf)

    def _save_raw_file(self,buffer_list):
        file_name = ''.join([strftime("%Y-%m-%d-%H:%M:%S", gmtime()) , '.iob'])
        output_path = os.path.join(self.data_store_path, file_name)
        with open(output_path, 'w+') as f:
            for line in buffer_list:
                f.write("%s " % line)
            f.flush()
            f.close()

    def _load_local_files(self, file_path):
        """

        :return:
        """

        with open(file_path, 'r') as myfile:
            os.remove(file_path)
            return myfile.readlines()

    def _init_node_parm(self, key):
        """
        init parms by using master classes (handling params)
        :return:
        """
        try :
            wf_conf = WorkFlowDataIob(key)
            self.data_sql_stmt = wf_conf.get_sql_stmt()
            self.data_src_path = wf_conf.get_source_path()
            self.data_src_type = wf_conf.get_src_type()
            self.data_store_path = wf_conf.get_step_store()
            self.data_server_type = wf_conf.get_src_server()
            self.data_parse_type = wf_conf.get_parse_type()
            self.data_preprocess_type = wf_conf.get_step_preprocess()
            self.preprocess_type = self.data_preprocess_type
            self.word_embed_model = wf_conf.get_word_embed_model()
        except Exception as e :
            raise Exception ("error on initialzing data_iob node : {0}".format(e))

    def _set_progress_state(self):
        return None

    def load_data(self, node_id = "", parm = 'all'):
        """
        load train data
        :param node_id:
        :param parm:
        :return:
        """
        try:
            file_path = utils.get_filepaths(self.data_store_path, 'iob')
            return file_path
        except Exception as e:
            raise Exception(e)


