import json
from rest_framework.response import Response
from rest_framework.views import APIView
import coreapi

class RuleCateList(APIView):

    def post(self, request, nnid):
        """
        Manage simple rules for framework
        ---
        # Class Name : RuleCateList

        # Description:
            Manage simple rules in a dict format
            Provide CRDU method for rules
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def get(self, request, nnid):
        """
        Manage simple rules for framework
        ---
        # Class Name : RuleCateList

        # Description:
            Manage simple rules in a dict format
            Provide CRDU method for rules
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def put(self, request, nnid):
        """
        Manage simple rules for framework
        ---
        # Class Name : RuleCateList

        # Description:
            Manage simple rules in a dict format
            Provide CRDU method for rules
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def delete(self, request, nnid):
        """
        Manage simple rules for framework
        ---
        # Class Name : RuleCateList

        # Description:
            Manage simple rules in a dict format
            Provide CRDU method for rules
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))
