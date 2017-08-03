from chatbot import serializers
from rest_framework.views import APIView
from chatbot.botbuilder.bot_def_list_info import BotDefListInfo
from chatbot.botbuilder.bot_entity_list_info import BotEntityListInfo
from chatbot.botbuilder.bot_model_list_info import BotModelListInfo
from chatbot.botbuilder.bot_intent_list_info import BotIntentListInfo
from chatbot.botbuilder.bot_story_list_info import BotStoryListInfo
from chatbot.botbuilder.bot_tagging_info import BotTaggingInfo
from chatbot.botbuilder.bot_entity_relation_info import BotEntityRelationInfo

class BotBuilder(APIView):

    def run_builder(self, data, type):
        """
        insert nn_info version data
        :param req:
        :return:
        """
        try:

            if type == "def":
                return_value = BotDefListInfo.run_def_builder(self,data=data)

            elif type == "intent":
                return_value = BotIntentListInfo.run_intent_builder(self,data=data)

            elif type == "entitylist":
                return_value = BotEntityListInfo.run_entity_builder(self,data=data)

            elif type == "model":
                return_value = BotModelListInfo.run_model_builder(self,data=data)

            elif type == "tagging":
                return_value = BotTaggingInfo.run_tagging_builder(self,data=data)

            elif type == "story":
                return_value = BotStoryListInfo.run_story_builder(self,data=data)

            elif type == "entityrelation":
                return_value = BotEntityRelationInfo.run_entity_relation_builder()

            return return_value

        except Exception as e:
            raise Exception(e)
