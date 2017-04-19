from chatbot.common.chat_share_data import ShareData

class ResponseGenerator(ShareData):
    """

    """
    def select_response(self, share_data):
        try:
            self.__dict__ = share_data.__dict__
            response = ""
            if (self.story_board_id == '1'):
                self.set_output_data("이미지 검색 결과 출력")
            elif (self.story_board_id == '2'):
                response = self.story_set_entity["이름"] + "의 전화번호는 031-723-1234입니다."
            elif (self.story_board_id == '3'):
                name = self.story_set_entity["업무"]
                business = {"출하" : "김승우", "야드" : "김수상", "설비" : "박성찬", "매출" : "백지현", "공정" : "이상현", "원가" : "김영재"}
                response = self.story_set_entity["업무"] + "업무 담당자는" + business[name] + "입니다"
            elif (self.story_board_id == '4'):
                response = self.story_set_entity["이름"] + "은 " + self.story_set_entity["날짜"] + " 휴가입니다."
            elif (self.story_board_id == '5'):
                response = "AI과제 맴버는 김승우, 김수상, 백지현, 박성찬, 김영재, 이태영, 황민호, 이상현입니다."
            else :
                response = self.get_unknown_response()
            print("■■■■■■■■■■ 챗봇 응답 메세지 결과 : " + response)
            self.set_output_data(response)
            share_data = self._initailize_story(share_data)
            share_data.__dict__ =  self.__dict__

            return share_data

        except Exception as e:
            raise Exception(e)

    def _initailize_story(self, share_data):

        if(share_data != None) :
            share_data.set_story_id("")
            share_data.set_intent_id("")
            share_data.set_request_data("")
            share_data.initialize_story_entity()
            share_data.set_request_type("")
        return share_data

    def get_unknown_response(self) :
        return "무슨 말씀인지 잘 모르겠어요"

    def tone_generator(self):
        return None

    def grammar_generator(self):
        return None

    def final_generator(self):
        response = 'Hi I am Bot'
        return response