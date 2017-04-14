from chatbot.renponse.response_generator import ResponseGenerator

class ResponseSelection:

    def select_response(self, intend):
        response = ""
        if (intend == ' 1'):
            response = "이미지로 사람을 검색하려면 학습된 이미지 데이터가 있어야합니다"
        elif (intend == ' 2'):
            response = "MES 운영팀에 P1 남자 직급은 없습니다"
        elif (intend == ' 3'):
            response = "KCH사업부장님 입니다"
        elif (intend == ' 4'):
            response = "AI과제팀에 문의해주세요"
        elif (intend == ' 5'):
            response = "EP 팀장님 전화번호는 XXX-XXXX입니다"
        elif (intend == ' 6'):
            response = "SJJ Manager에게 물어보세요"
        elif (intend == ' 7'):
            response = "LSH(P2) Manager에게 물어보세요"
        elif (intend == ' 8'):
            response = "KYJ(P3) Manager에게 물어보세요"
        elif (intend == ' 9'):
            response = "LAB P1직급은 XXX입니다"
        elif (intend == ' 10'):
            response = "Smart사업실장님에 대해 궁금한가"
        elif (intend == ' 11'):
            response = "정보기획실장에 대해 무엇이 궁금한가요"
        elif (intend == ' -1'):
            response = self.get_unknown_response()
        print ("Selected Response : {0}".format(response))
        return response

    def get_unknown_response(self):
        answer = "이해가 잘 안되요 자세히 알려주세요"
        return answer

    def get_frequent_response(self):
        return None

    def get_default_response(self):
        answer = ""
        return answer
