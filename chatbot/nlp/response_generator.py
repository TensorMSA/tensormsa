from chatbot.common.chat_share_data import ShareData

class ResponseGenerator(ShareData):

    def __init__(self,  response_story):
        self.response_story = response_story

    def select_response(self, share_data):
        try:
            response = ""
            response = self.response_story[0]['fields']['output_data']

            # if (self.story_board_id == '2'):
            #     response = self.story_slot_entity["이름"] + "의 전화번호는 XX-XXX-1234입니다."
            # elif (self.story_board_id == '3'):
            #     name = self.story_slot_entity["업무"]
            #     business = {"출하" : "김승우", "야드" : "김수상", "설비" : "박성찬", "매출" : "백지현", "공정" : "이상현", "원가" : "김영재"}
            #        response = self.story_slot_entity["업무"] + "업무 담당자는" + business[name] + "입니다"
            # elif (self.story_board_id == '4'):
            #     response = self.story_slot_entity["이름"] + "은 " + self.story_slot_entity["날짜"] + " 휴가입니다."
            #
            # elif (self.story_board_id == '7'):
            #     response = self.story_slot_entity["이름"] + " 등 X명이 참석자로 " + self.story_slot_entity["장소"] + "에서 회의 예약 되었습니다."
            # else :
            #     response = self.get_unknown_response()
            # print("■■■■■■■■■■ 챗봇 응답 메세지 결과 : " + response)
            self.set_output_data(response)
            return share_data

        except Exception as e:
            raise Exception(e)

    def get_unknown_response(self) :
        return "무슨 말씀인지 잘 모르겠어요"

    def tone_generator(self):
        return None
