class ChatKnowledgeDataDict:

    def __init__(self, cb_id):
        pass

    def get_entity_keys(self, cb_id):
        entity_key_list = ['이름', '직급', '직책', '타입', '실', '근태코드', '그룹', '근무조', '부', '업무', '날짜','회의','시간시작','시간끝','장소']
        return entity_key_list

    def get_entity_types(self, cb_id):
        #TODO : need to get data from db or cache
        #['이름', '직급', '직책', '근태코드', '실', 'Grade', '그룹', '근무조', '부', '지역']
        temp_entitiy = {}
        temp_entitiy['이름'] = ['김승우', '김수상', '박성찬', '백지현', '이상현', '김영재', '이태영','신민호','주용회','김동희','박종규','차민주']
        temp_entitiy['업무'] = ['출하', '야드', '설비', '매출', '공정', '원가', '메일']
        temp_entitiy['날짜'] = ['어제', '오늘', '지금', '내일', '모래']
        temp_entitiy['타입'] = ['이미지', '안녕', '하이', '채홍', '영식','김채홍','김영식','정덕균','덕균','박미화','미화','박미','저장']
        #temp_entitiy['직책'] = ['팀장', '일반']
        temp_entitiy['직급'] = ['사원', '대리', '과장', '차장' , '부장', '팀장', '사업부장','상사','리더']
        temp_entitiy['근태코드'] = ['머', '연차', '반차', '근무', '어디', '근태']
        temp_entitiy['시간시작'] = ['부터','2시부터','3시부터','4시부터','5시부터','6시부터','7시부터','8시부터','9시부터','10시부터','11시부터','12시부터',
                    '1시에서','2시에서','3시에서','4시에서','5시에서','6시에서','7시에서','8시에서','9시에서','10시에서','11시에서','12시에서']

        temp_entitiy['시간끝'] = ['까지','2시까지','3시까지','4시까지','5시까지','6시까지','7시까지','8시까지'
                                 ,'9시까지','10시까지','11시까지','12시까지']
        temp_entitiy['회의'] = ['회의', '회의실']
        temp_entitiy['장소'] = ['센터', '판교', '포항', '광양']

        #temp_entitiy['그룹'] = ['']
        #temp_entitiy['근무조'] = ['']
        #temp_entitiy['업무'] = ['ERP','SCM','EP','MES']
        #temp_entitiy['지역'] = ['서울', '판교', '포항', '광양']
        return temp_entitiy

    def get_essential_entity(self, story_board_id):
        essential_entity = []
        if(story_board_id == '') :
            pass
        elif(story_board_id == '2') :
            essential_entity = ["이름"]
        elif(story_board_id == '3') :
            essential_entity = ["업무"]
        elif(story_board_id == '4') :
            essential_entity = ["이름","날짜"]
        elif(story_board_id == '6') :
            essential_entity = ["이름"]
        elif(story_board_id == '7') :#회의 등록
            essential_entity = ["이름","시간시작","시간끝","장소"]
        return essential_entity