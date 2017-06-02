from chatbot import models
from django.core import serializers as serial
import json

class ChatKnowledgeDataDict:

    def __init__(self, cb_id):
        pass

    def get_entity_keys(self, cb_id):
        query_set = models.CB_ENTITY_LIST_INFO.objects.filter(story_id='7', entity_type = 'key')
        query_set = serial.serialize("json", query_set)
        return json.loads(query_set)[0]['fields']['entity_list']['key'] # list type

    def get_entity_types(self, cb_id):
        #TODO : need to get data from db or cache
        #['이름', '직급', '직책', '근태코드', '실', 'Grade', '그룹', '근무조', '부', '지역']
        temp_entitiy = {}
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

        query_set = models.CB_ENTITY_LIST_INFO.objects.filter(story_id = '7', entity_type = 'essential')
        query_set = serial.serialize("json", query_set)
        return json.loads(query_set)[0]['fields']['entity_list']['essential']  # list type


