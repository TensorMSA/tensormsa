import codecs, os
import pandas as pd
from konlpy.tag import Mecab
from numba import *
import numpy as np

class DataAugmentation :
    """
    Data Augmentation Class for nlp
    mainly for create iob data with pattern and dict
    test = DataAugmentation()
    test.load_dict()
    test.convert_data()
    """

    def __init__(self, conf):
        """
        init parms need to mange teses parms on db
        """
        self.aug_file_cnt = 0
        self.use_mecab = conf.get("use_mecab")
        self.max_file_size = conf.get("max_file_size")  #10M
        self.pattern_data_path = conf.get("pattern_data_path")
        self.augmented_out_path = conf.get("augmented_out_path")
        self.dict_path = conf.get("dict_path")
        self.out_format_type = conf.get("out_format_type")
        self.ner_dicts = {}
        self.gpu_use = True

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
            for val in list(set(df_csv_read[col])) :
                if (val == val and val != None) :
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
            word = word.replace('\n', '')
            if(word in list(self.ner_dicts.keys())) :
                match_keys.append(word)
        return match_keys

    #@autojit
    def _aug_sent(self, keys, pattern, return_aug_sent=[]) :
        """
        function which actually augment sentences
        with given pattern and keys
        :param keys: entity keys
        :param pattern: sentence pattern
        :return: list of augmented sentence
        """
        try :
            if (len(keys) > 0):
                key = keys[0]
                del keys[0]
            else :
                return return_aug_sent

            if (len(return_aug_sent) == 0):
                for word in self.ner_dicts[key] :
                    line = []
                    for slot in pattern:
                        for rep in ['\n', 'NaN'] :
                            slot = slot.replace(rep, '')
                        if(key in slot) :
                            for wd in self.mecab.morphs(word):
                                line.append((wd, key))
                        else :
                            line.append((slot, 'O'))
                    return_aug_sent.append(line)
            else :
                del_idx = []
                for i, line in enumerate(return_aug_sent):
                    for j, slot in enumerate(line):
                        if (slot[0] == key):
                            for word in self.ner_dicts[key]:
                                line = return_aug_sent[i].copy()
                                for z, slot in enumerate(line):
                                    if(slot[0] == key) :
                                        buffer = ""
                                        for wd in self.mecab.morphs(word) :
                                            buffer = ' '.join([buffer,wd])
                                            line[z] = (buffer, key)
                                return_aug_sent.append(line)
                            del_idx.append(i)

                for _ in del_idx:
                    del return_aug_sent[0]
            return self._aug_sent(keys, pattern, return_aug_sent)
        except Exception as e :
            print("error on nlp data augmentation :{0}".format(e))

    def _iob_formatter(self, aug_data) :
        """
        save aug list as iob file format
        :param aug_data: augmented list of sentence
        :return: None
        """
        path = ''.join([self.augmented_out_path, 'Test' , str(self.aug_file_cnt) , '.iob'])
        if(os.path.exists(path) == False or os.path.getsize(path) < self.max_file_size) :
            with open(path, "a")  as f :
                for line in aug_data :
                    for word in line :
                        related_words =  word[0].split(' ')
                        for tocken in related_words :
                            f.write(''.join([tocken, ' ', word[1]]))
                            f.write('\n')
                    f.write('\n')
        else :
            self.aug_file_cnt = self.aug_file_cnt + 1
            path = ''.join([self.augmented_out_path, 'Test', str(self.aug_file_cnt), '.iob'])
            with open(path, "w")  as f :
                for line in aug_data :
                    for word in line :
                        related_words =  word[0].split(' ')
                        for tocken in related_words :
                            f.write(''.join([tocken, ' ', word[1]]))
                            f.write('\n')
                    f.write('\n')

    def _plain_formatter(self, aug_data) :
        """
        save aug list as iob file format
        :param aug_data: augmented list of sentence
        :return: None
        """
        path = ''.join([self.augmented_out_path, 'Test', str(self.aug_file_cnt), '.out'])
        if (os.path.exists(path) == False or os.path.getsize(path) < self.max_file_size):
            with open(path, "a")  as f :
                for line in aug_data :
                    for word in line :
                        f.write(''.join([word[0], ' ']))
                    f.write('\n')
        else :
            self.aug_file_cnt = self.aug_file_cnt + 1
            path = ''.join([self.augmented_out_path, 'Test', str(self.aug_file_cnt), '.out'])
            with open(path, "w")  as f :
                for line in aug_data :
                    for word in line :
                        f.write(''.join([word[0], ' ']))
                    f.write('\n')

    def _intent_formatter(self, aug_data, key) :
        """
        save aug list as iob file format
        :param aug_data: augmented list of sentence
        :return: None
        """
        path = ''.join([self.augmented_out_path, 'Test', str(self.aug_file_cnt), '.csv'])

        if (os.path.exists(path) == False) :
            with open(path, "w")  as f :
                f.write('encode,decode\n')

        if (os.path.exists(path) == False or os.path.getsize(path) < self.max_file_size):
            with open(path, "a")  as f :
                for line in aug_data :
                    for word in line :
                        f.write(''.join([word[0], ' ']))
                    f.write(',')
                    f.write(str(key))
                    f.write('\n')
        else :
            self.aug_file_cnt = self.aug_file_cnt + 1
            path = ''.join([self.augmented_out_path, 'Test', str(self.aug_file_cnt), '.csv'])
            with open(path, "w")  as f :
                for line in aug_data :
                    for word in line :
                        f.write(''.join([word[0], ' ']))
                    f.write(',')
                    f.write(str(key))
                    f.write('\n')

    def convert_data(self) :
        """
        augment data with entity list and pattern
        :return: None
        """
        if (self.out_format_type == 'intent'):
            self._conv_type_b()
        else :
            self._conv_type_a()

    def _conv_type_b(self):
        """
        
        :return: 
        """
        df_csv_read = pd.read_csv(self.pattern_data_path,
                                  skipinitialspace=True,
                                  engine="python",
                                  encoding='utf-8-sig')

        i = 0
        for key, line in zip(df_csv_read['decode'].values, df_csv_read['encode'].values) :
            words = []
            if (self.use_mecab):
                self.mecab = Mecab('/usr/local/lib/mecab/dic/mecab-ko-dic')
                pos = self.mecab.pos(line)
                for word, tag in pos:
                    words.append(word)
            else:
                words = str(line).split(' ')
            print("===={0} line job start".format(i))
            match_keys = self._check_all_match(words)
            aug_data = self._aug_sent(match_keys, words, [])
            self._intent_formatter(aug_data, key)
            print("===={0} line job done".format(i))
            i = i + 1

    def _conv_type_a(self):
        """
        
        :return: 
        """
        with codecs.open( self.pattern_data_path, "r", "utf-8" ) as fileObj :
            document = fileObj.readlines()
            return_arr = []

            for i, line in enumerate(document) :
                words = []
                if(self.use_mecab) :
                    self.mecab = Mecab('/usr/local/lib/mecab/dic/mecab-ko-dic')
                    pos = self.mecab.pos(line)
                    for word, tag in pos:
                        words.append(word)
                else :
                    words = str(line).split(' ')

                print("===={0} line job start".format(i))
                match_keys = self._check_all_match(words)
                if(self.out_format_type == 'plain') :
                    aug_data = self._aug_sent(match_keys, words, [])
                    self._plain_formatter(aug_data)
                elif(self.out_format_type == 'iob') :
                    aug_data = self._aug_sent(match_keys, words, [])
                    self._iob_formatter(aug_data)
                else :
                    raise Exception (' '.join(['not', 'plain', 'or iob']))
                print("===={0} line job done".format(i))