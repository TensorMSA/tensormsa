import json
from rest_framework.response import Response
from rest_framework.views import APIView
from master.automl.automl_rule import AutoMlRule
from django.core import serializers
import coreapi

class RunManagerAutoRule(APIView):
    # TODO:add document sample for swagger (need to update)
    coreapi_fields = (
        coreapi.Field(
            name='parm1',
            required=True,
            schema=str,
        ),
        coreapi.Field(
            name='parm2',
            required=True,
            schema=str,
        ),
    )
    def post(self, request, graph_id):
        """
        Your docs
        ---
        # Class Name (must be separated by `---`)

        # Description:
            - name: name
              description: Foobar long description goes here
        """
        try:
            return_data = AutoMlRule().set_graph_type_list(graph_id, request.data)
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def get(self, request, graph_id):
        """
        Your docs
        ---
        # Class Name (must be separated by `---`)

        # Description:
            - name: name
              description: Foobar long description goes here
        """
        try:
            if (graph_id == 'all') :
                return_data = AutoMlRule().get_graph_type_list()
            elif (graph_id is not None) :
                return_data = AutoMlRule().get_graph_info(graph_id)
            else :
                raise Exception("no vailed graph_id")
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def put(self, request, graph_id):
        """
        Your docs
        ---
        # Class Name (must be separated by `---`)

        # Description:
            - name: name
              description: Foobar long description goes here
        """
        try:
            return_data = AutoMlRule().update_graph_type_list(graph_id, request.data)
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def delete(self, request, graph_id):
        """
        Your docs
        ---
        # Class Name (must be separated by `---`)

        # Description:
            - name: name
              description: Foobar long description goes here
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))
