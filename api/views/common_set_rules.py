from django.core.serializers.json import json
from rest_framework.response import Response
from rest_framework.views import APIView
from common.rule.default_rule_manager import set_all_default_rules

class CommonSetRules(APIView):
    """

    """

    def post(self, request):
        """
        request to setup all necessary rule tables with default data
        ---
        # Class Name : CommonSetRules
        # Description:
            request to setup all necessary rule tables with default data
        """
        try:
            result = set_all_default_rules()
            return_data = {"status": "200", "result": result}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))
