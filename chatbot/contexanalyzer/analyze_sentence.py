from konlpy.tag import Mecab
import json
#sentence Analyzer
class AnalyzeSentence:

    """
    TODO:swkim
    """
    def get_entity_value(self, sentence):

        mecab = Mecab('/usr/local/lib/mecab/dic/mecab-ko-dic')
        pos_sentence = mecab.pos(sentence)
        print("◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆ 자연언어 Tagging 결과 출력 {0}".format(pos_sentence))

        nouns_entity = mecab.nouns(sentence)
        print("◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆ 자연언어 Entity 결과 출력 {0}".format(nouns_entity))
        analyzed_entity = self.get_entity_analyze(nouns_entity)
        return analyzed_entity

    def get_entity_analyze(self, entity):
        try :
            grade = ['사원', '대리', '과장', '차장', '부장', '팀장']
            department = ['포스코IT사업부','정보기획']
            attendance = ['근태']
            telephone = ['전화번호', '전화', '번호']
            entity_list = []
            for noun in entity :
                if(noun in grade) :
                    entity_list.append("grade : " + noun)
                elif(noun in department) :
                    entity_list.append("department" + noun)
                elif(noun in attendance) :
                    entity_list.append("attendance" + noun)
                elif(noun in telephone) :
                    entity_list.append("telephone" + noun)
                else :
                    entity_list.append("unknown" + noun)

            return entity_list

        except Exception as e:
            raise Exception(e)


    def set_entity_value () :
        analyzed_entity = ""
        return analyzed_entity


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

