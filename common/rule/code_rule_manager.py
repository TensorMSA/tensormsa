from django.core.cache import cache

class CodeRuleManager:
    """

    """
    def server_start_up(self):
        self.mount_cache()

    def get_code_name(self, column, code):
        """
        create function with cached data
        :param column:
        :param code:
        :return: code mean (string)
        """

        return None

    def get_code_id_by_name(self, column, name):
        """
        create function with cached data
        :param column:
        :param name:
        :return:
        """

        return None

    def _get_all_code_rule(self):
        """

        :return:
        """
        return []

    def mount_cache(self):
        """

        :return:
        """
        #sample uses memcache with django.core.cache
        cache.set("test_sample", "value")
        cache.get("test_sample")
