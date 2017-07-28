from chatbot import models
from django.core import serializers as serial
import json

class ChatStoryConfData:

    def __init__(self, intent_id):
        self.intent_id = intent_id

    def get_intent_story(self):
        query_set = models.CB_STORYBOARD_LIST_INFO.objects.filter(intent_id = self.intent_id)
        query_set = serial.serialize("json", query_set)
        return json.loads(query_set)

    def get_story_response(self, story_id):
        query_set = models.CB_RESPONSE_LIST_INFO.objects.filter(story_id = story_id)
        query_set = serial.serialize("json", query_set)
        return json.loads(query_set)

    def get_story_service(self, story_id):
        query_set = models.CB_SERVICE_LIST_INFO.objects.filter(story_id = story_id)
        query_set = serial.serialize("json", query_set)
        return json.loads(query_set)