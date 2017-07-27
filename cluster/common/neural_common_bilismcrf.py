import numpy as np
import os,h5py
from hanja import hangul

class BiLstmCommon :
    """
    common functions for bilstm crf
    """
    UNK = "$UNK$"
    NUM = "$NUM$"
    NONE = "O"

    def write_char_embedding(self, vocab, trimmed_filename):
        """
        Writes a vocab to a file

        Args:
            vocab: iterable that yields word
            filename: path to vocab file
        Returns:
            write a word per line
        """
        try:
            print("Writing vocab...")
            embeddings = np.zeros([len(vocab), 160])
            if (type(vocab) == type(set())):
                vocab = list(vocab)
            for i, word in enumerate(vocab):
                word = word.lower()
                embeddings[vocab.index(word)] = np.array(self.get_onehot_vector(word))[0]
            np.savetxt(trimmed_filename, embeddings)
            print("- done. {} tokens".format(len(vocab)))
        except Exception as e:
            print("error on write_char_embedding : {0}".format(e))


    def write_vocab(self, vocab, filename):
        """
        Writes a vocab to a file

        Args:
            vocab: iterable that yields word
            filename: path to vocab file
        Returns:
            write a word per line
        """
        print("Writing vocab...")
        with open(filename, "w+") as f:
            for i, word in enumerate(vocab):
                if i != len(vocab) - 1:
                    f.write("{}\n".format(word))
                else:
                    f.write(word)
        print("- done. {} tokens".format(len(vocab)))


    def get_vocabs(self, datasets, vocab=None, tags=None):
        """
        Args:
            datasets: a list of dataset objects
        Return:
            a set of all the words in the dataset
        """
        try:
            print("Building vocab...")
            if (vocab == None or tags == None):
                vocab_words = set()
                vocab_tags = set()
            else:
                vocab_words = set(vocab)
                vocab_tags = set(tags)

            for dataset in datasets:
                for words, tags in dataset:
                    vocab_words.update(words)
                    vocab_tags.update(tags)
            print("- done. {} tokens".format(len(vocab_words)))
            return vocab_words, vocab_tags
        except Exception as e:
            print("error on get_vacabs {0}".format(e))


    def load_vocab(self, filename):
        """
        Args:
            filename: file with a word per line
        Returns:
            d: dict[word] = index
        """
        d = dict()

        if (os.path.exists(filename) == False):
            return d

        with open(filename) as f:
            for idx, word in enumerate(f):
                word = word.strip()
                d[word] = idx

        return d


    def export_trimmed_glove_vectors(self, vocab, model, trimmed_filename):
        """
        Saves glove vectors in numpy array

        Args:
            vocab: dictionary vocab[word] = index
            glove_filename: a path to a glove file
            trimmed_filename: a path where to store a matrix in npy
            dim: (int) dimension of embeddings
            UNK = "$UNK$"
            NUM = "$NUM$"
            NONE = "O"
        """
        try:
            embeddings = np.zeros([len(vocab), model.vector_size])
            for word in vocab:
                if (word != self.UNK):
                    embeddings[list(vocab).index(word)] = model[word]
            np.savetxt(trimmed_filename, embeddings)
        except Exception as e:
            print("error on export_trimmed_glove_vectors : {0}".format(e))


    def get_trimmed_glove_vectors(self, filename):
        """
        Args:
            filename: path to the npz file
        Returns:
            matrix of embeddings (np array)
        """
        with open(filename) as f:
            return np.loadtxt(f)


    def get_char_vocab(self, dataset, chars=None):
        """
        Args:
            dataset: a iterator yielding tuples (sentence, tags)
        Returns:
            a set of all the characters in the dataset
        """
        if (chars == None):
            vocab_char = set()
        else:
            vocab_char = set(chars)

        for words, _ in dataset:
            for word in words:
                word = word.lower()
                vocab_char.update(word)

        return vocab_char


    def get_processing_word(self, vocab_words=None, vocab_chars=None,
                            lowercase=False, chars=False):
        """
        Args:
            vocab: dict[word] = idx
        Returns:
            f("cat") = ([12, 4, 32], 12345)
                     = (list of char ids, word id)
        """

        def f(word):
            # 1. preprocess word
            if (lowercase):
                word = word.lower()

            # 0. get chars of words
            if vocab_chars is not None and chars == True:
                char_ids = []
                for char in word:
                    # ignore chars out of vocabulary
                    if char in vocab_chars:
                        char_ids += [vocab_chars[char]]

            # 2. get id of word
            if vocab_words is not None:
                if word in vocab_words:
                    word = vocab_words[word]
                else:
                    word = vocab_words[self.UNK]

            # 3. return tuple char ids, word id
            if vocab_chars is not None and chars == True:
                return char_ids, word
            else:
                return word

        return f


    def minibatches(self, data, minibatch_size):
        """
        Args:
            data: generator of (sentence, tags) tuples
            minibatch_size: (int)
        Returns:
            list of tuples
        """
        x_batch, y_batch = [], []
        for (x, y) in data:
            if len(x_batch) == minibatch_size:
                yield x_batch, y_batch
                x_batch, y_batch = [], []

            if type(x[0]) == tuple:
                x = zip(*x)
            x_batch += [x]
            y_batch += [y]

        if len(x_batch) != 0:
            yield x_batch, y_batch


    def _pad_sequences(self, sequences, pad_tok, max_length):
        """
        Args:
            sequences: a generator of list or tuple
            pad_tok: the char to pad with
        Returns:
            a list of list where each sublist has same length
        """
        sequence_padded, sequence_length = [], []

        for seq in sequences:
            seq = list(seq)
            seq_ = seq[:max_length] + [pad_tok] * max(max_length - len(seq), 0)
            sequence_padded += [seq_]
            sequence_length += [min(len(seq), max_length)]

        return sequence_padded, sequence_length


    def get_chunks(self, seq, tags):
        """
        Args:
            seq: [4, 4, 0, 0, ...] sequence of labels
            tags: dict["O"] = 4
        Returns:
            list of (chunk_type, chunk_start, chunk_end)

        Example:
            seq = [4, 5, 0, 3]
            tags = {"B-PER": 4, "I-PER": 5, "B-LOC": 3}
            result = [("PER", 0, 2), ("LOC", 3, 4)]
        """
        try:
            default = tags[self.NONE]
            idx_to_tag = {idx: tag for tag, idx in iter(tags.items())}
            chunks = []
            chunk_type, chunk_start = None, None
            for i, tok in enumerate(seq):
                # End of a chunk 1
                if tok == default and chunk_type is not None:
                    # Add a chunk.
                    chunk = (chunk_type, chunk_start, i)
                    chunks.append(chunk)
                    chunk_type, chunk_start = None, None

                # End of a chunk + start of a chunk!
                elif tok != default:
                    tok_chunk_type = self.get_chunk_type(tok, idx_to_tag)
                    if chunk_type is None:
                        chunk_type, chunk_start = tok_chunk_type, i
                    # elif tok_chunk_type != chunk_type or tok[0] == "B":
                    elif tok_chunk_type != chunk_type:
                        chunk = (chunk_type, chunk_start, i)
                        chunks.append(chunk)
                        chunk_type, chunk_start = tok_chunk_type, i
                else:
                    pass
            # end condition
            if chunk_type is not None:
                chunk = (chunk_type, chunk_start, len(seq))
                chunks.append(chunk)
            return chunks
        except Exception as e:
            raise Exception(e)


    def pad_sequences(self, sequences, pad_tok, nlevels=1):
        """
        Args:
            sequences: a generator of list or tuple
            pad_tok: the char to pad with
        Returns:
            a list of list where each sublist has same length
        """
        if nlevels == 1:
            max_length = max(map(lambda x: len(x), sequences))
            sequence_padded, sequence_length = self._pad_sequences(sequences,
                                                                   pad_tok, max_length)

        elif nlevels == 2:
            max_length_word = max([max(map(lambda x: len(x), seq)) for seq in sequences])
            sequence_padded, sequence_length = [], []
            for seq in sequences:
                # all words are same length now
                sp, sl = self._pad_sequences(seq, pad_tok, max_length_word)
                sequence_padded += [sp]
                sequence_length += [sl]

            max_length_sentence = max(map(lambda x: len(x), sequences))
            sequence_padded, _ = self._pad_sequences(sequence_padded, [pad_tok] * max_length_word,
                                                     max_length_sentence)
            sequence_length, _ = self._pad_sequences(sequence_length, 0, max_length_sentence)

        return sequence_padded, sequence_length


    def get_chunk_type(self, tok, idx_to_tag):
        tag_name = idx_to_tag[tok]
        return tag_name.split('-')[-1]


    class CoNLLDataset(object):
        """
        Class that iterates over CoNLL Dataset
        """

        def __init__(self, filename, processing_word=None, processing_tag=None,
                     max_iter=None, all_line=True):
            """
            Args:
                filename: path to the file
                processing_words: (optional) function thsat takes a word as input
                processing_tags: (optional) function that takes a tag as input
                max_iter: (optional) max number of sentences to yield
            """
            self.filename = filename
            self.processing_word = processing_word
            self.processing_tag = processing_tag
            self.max_iter = max_iter
            self.length = None
            self.all_line = all_line

        def __iter__(self):
            try:
                niter = 0
                with open(self.filename) as f:
                    words, tags = [], []
                    for line in f:
                        line = line.strip()
                        if (len(line) == 0 or line.startswith("-DOCSTART-")):
                            if len(words) != 0:
                                niter += 1
                                if self.max_iter is not None and niter > self.max_iter:
                                    break
                                yield words, tags
                                words, tags = [], []
                        else:
                            if len(line.split(' ')) != 2 :
                                continue
                            if len(line.split(' ')) > 2 :
                                temp = line.split(' ')
                                line = ' '.join([temp[len(temp)-2],temp[len(temp)-1]])
                            word, tag = line.split(' ')
                            if self.processing_word is not None:
                                word = self.processing_word(word)
                            if self.processing_tag is not None:
                                tag = self.processing_tag(tag)
                            words += [word]
                            tags += [tag]

            except Exception as e:
                raise Exception(e)

        def __len__(self):
            """
            Iterates once over the corpus to set and store length
            """
            if self.length is None:
                self.length = 0
                for _ in self:
                    self.length += 1

            return self.length