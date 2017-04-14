from konlpy.tag import Mecab

#sentence Analyzer
class AnalyzeSentence:


    def get_entity_value(self, sentence):

        mecab = Mecab('/usr/local/lib/mecab/dic/mecab-ko-dic')
        pos_sentence = mecab.pos(sentence)
        print("◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆ 자연언어 Tagging 결과 출력 {0}".format(pos_sentence))

        entity_sentence = mecab.nouns(sentence)
        print("◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆ 자연언어 Entity 결과 출력 {0}".format(entity_sentence))

        return entity_sentence

    def _mecab_parse(self, sentence):

        mecab = Mecab('/usr/local/lib/mecab/dic/mecab-ko-dic')

        #pos_sentence = mecab.pos(sentence)
        #print('Tagged : {}'.pos_sentence)
        # pos_sentence = []
        # for data in sentence:
        #     pos_sentence = pos_sentence + mecab.pos(data)
        return mecab

    def sentence_to_vector(sentence):
        sentence_temp=sentence
        return None

