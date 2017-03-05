from django.apps import AppConfig
from common.rule.cate_rule_manager import CateRuleManager
from common.rule.code_rule_manager import CodeRuleManager


class CommonConfig(AppConfig):
    name = 'common'

    def ready(self):
        """
        set cache on server start up
        :return:
        """
        CodeRuleManager().server_start_up()
        CateRuleManager().server_start_up()