class ChatKnowledgeDataDict:

    def __init__(self, cb_id):
        pass

    def get_entity_keys(self, cb_id):
        entity_key_list = ['이름', '직급', '직책', '타입', '실', '근태코드', '그룹', '근무조', '부', '업무', '날짜']
        return entity_key_list

    def get_entity_types(self, cb_id):
        #TODO : need to get data from db or cache
        #['이름', '직급', '직책', '근태코드', '실', 'Grade', '그룹', '근무조', '부', '지역']
        temp_entitiy = {}
        temp_entitiy['이름'] = ['김승우', '김수상', '박성찬', '백지현', '이상현', '김영재', '이태영']
        temp_entitiy['업무'] = ['출하', '야드', '설비', '매출', '공정', '원가', '메일']
        temp_entitiy['날짜'] = ['어제', '오늘', '지금', '내일', '모래']
        temp_entitiy['타입'] = ['이미지', '안녕', '하이', '채홍', '영식','김채홍','김영식']
        #temp_entitiy['직책'] = ['팀장', '일반']
        temp_entitiy['직급'] = ['사원', '대리', '과장', '차장' , '부장', '팀장', '사업부장','상사']
        temp_entitiy['근태코드'] = ['머', '연차', '반차', '근무', '어디', '근태']
        #temp_entitiy['Grade'] = ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9']
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
        return essential_entity