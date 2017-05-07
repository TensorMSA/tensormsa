from chatbot import models
from django.core import serializers as serial

class ChatKnowledgeDataDict:

    def __init__(self, cb_id):
        pass

    def get_entity_keys(self, cb_id):
        entity_key_list = ['이름', '직급', '직책', '타입', '실', '근태코드', '그룹', '근무조', '부', '업무', '날짜','회의','시간시작','시간끝','장소']
        # query_set = models.CB_ENTITY_LIST_INFO.objects.filter(cb_id=cb_id,entity_type = 'key')
        # query_set = serial.serialize("json", query_set)
        # return json.loads(query_set) # list type
        return entity_key_list

    def get_entity_types(self, cb_id):
        #TODO : need to get data from db or cache
        #['이름', '직급', '직책', '근태코드', '실', 'Grade', '그룹', '근무조', '부', '지역']
        temp_entitiy = {}
        temp_entitiy['이름'] = ['김승우', '김수상', '박성찬', '백지현']
        temp_entitiy['업무'] = ['출하', '야드', '설비', '매출', '원가', '메일']
        temp_entitiy['날짜'] = ['어제', '오늘', '지금', '내일', '모래']
        temp_entitiy['타입'] = ['이미지', '안녕', '하이','저장','시작']
        #temp_entitiy['직책'] = ['팀장', '일반']
        temp_entitiy['직급'] = ['사원', '대리', '과장', '차장' , '부장', '팀장', '사업부장','상사','리더']
        temp_entitiy['근태코드'] = ['머', '연차', '반차', '근무', '어디', '근태']
        temp_entitiy['시간시작'] = ['부터','에서']
        temp_entitiy['시간끝'] = ['까지']
        temp_entitiy['회의'] = ['회의', '회의실']
        temp_entitiy['장소'] = ['센터', '판교', '포항', '광양']
        # query_set = models.CB_ENTITY_LIST_INFO.objects.filter(cb_id=cb_id)
        # query_set = serial.serialize("json", query_set)
        # return json.loads(query_set)
        return temp_entitiy

    def get_essential_entity(self, story_id):

        # query_set = models.CB_ENTITY_LIST_INFO.objects.filter(story_id = story_id,entity_type = 'essential')
        # query_set = serial.serialize("json", query_set)
        # return json.loads(query_set) #list type

        essential_entity = []
        if(story_id == '') :
            pass
        elif(story_id == '2') :
            essential_entity = ["이름"]
        elif(story_id == '3') :
            essential_entity = ["업무"]
        elif(story_id == '4') :
            essential_entity = ["이름","날짜"]
        elif(story_id == '6') :
            essential_entity = ["이름"]
        elif(story_id == '7') :#회의 등록
            essential_entity = ["이름","시간시작","시간끝","장소"]
        return essential_entity