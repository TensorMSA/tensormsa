import codecs
import pandas as pd
from konlpy.tag import Mecab

class DataAugmentation :
    """
    Data Augmentation Class for nlp
    mainly for create iob data with pattern and dict
    """

    def __init__(self):
        """
        init parms need to mange teses parms on db
        """
        self.use_mecab = True
        self.pattern_data_path = "/home/dev/Test.txt"
        self.augmented_out_path = "/home/dev/Test.iob"
        self.dict_path = "/home/dev/Test.csv"
        self.ner_dicts = {}

    def load_dict(self):
        """
        load dict list from csv file
        :return:
        """
        df_csv_read = pd.read_csv(self.dict_path,
                                  skipinitialspace=True,
                                  engine="python",
                                  encoding='utf-8-sig')

        for col in df_csv_read.keys() :
            self.ner_dicts[col] = []
            for val in df_csv_read[col] :
                if (val == val) :
                    self.ner_dicts[col].append(val)

    def _check_all_match(self, words) :
        """
        check all matcing dict keys
        in ohter word entity keys
        :param words: sentence str
        :return: list contain keys
        """
        match_keys = []
        for word in words :
            if(word in list(self.ner_dicts.keys())) :
                match_keys.append(word)
        return match_keys

    def _aug_sent(self, keys, pattern) :
        """
        function which actually augment sentences
        with given pattern and keys
        :param keys: entity keys
        :param pattern: sentence pattern
        :return: list of augmented sentence
        """
        return_aug_sent = []
        for key in keys :
            for word in self.ner_dicts[key] :
                line = []
                for slot in pattern :
                    for rep in ['\n', 'NaN'] :
                        slot = slot.replace(rep, '')
                    if(key in slot) :
                        line.append((word, key))
                    else :
                        line.append((slot, 'O'))
                return_aug_sent.append(line)

        for key in keys :
            for word in self.ner_dicts[key]:
                for i, line in enumerate(return_aug_sent) :
                    for j, slot in enumerate(line) :
                        if (slot[0] == key) :
                            return_aug_sent[i][j] = (word, key)

        return return_aug_sent

    def _iob_formatter(self, aug_data) :
        """
        save aug list as iob file format
        :param aug_data: augmented list of sentence
        :return: None
        """
        with open(self.augmented_out_path, "a")  as f :
            for line in aug_data :
                for word in line :
                    f.write(''.join([word[0], ' ', word[1]]))
                    f.write('\n')
                f.write('\n')

    def convert_data(self) :
        """
        augment data with entity list and pattern
        :return: None
        """
        with codecs.open( self.pattern_data_path, "r", "utf-8" ) as fileObj :
            document = fileObj.readlines()
            return_arr = []

            for i, line in enumerate(document) :
                words = []
                if(self.use_mecab) :
                    words = str(line).split(' ')
                else :
                    mecab = Mecab('/usr/local/lib/mecab/dic/mecab-ko-dic')
                    pos = mecab.pos(line)
                    for word, tag in pos:
                        words.append(word)
                print("===={0} line job start".format(i))
                match_keys = self._check_all_match(words)
                self._iob_formatter(self._aug_sent(match_keys, words))
                print("===={0} line job done".format(i))


# cls = DataAugmentation()
# cls.load_dict()
# cls.convert_data()

