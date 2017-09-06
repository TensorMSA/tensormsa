import json
from rest_framework.response import Response
from rest_framework.views import APIView
import coreapi

class RunManagerSchedule(APIView):
    # TODO:add document sample for swagger (need to update)
    coreapi_fields = (
        coreapi.Field(
            name='interval',
            required=True,
            type='time',
        ),
        coreapi.Field(
            name='start',
            required=True,
            type='date',
        ),
        coreapi.Field(
            name='end',
            required=True,
            type='date',
        ),
        coreapi.Field(
            name='repeat',
            required=True,
            type='int',
        ),
    )
    def post(self, request, nnid):
        """
        Training Job schedule management
        We have predefined set of graph flow.. on Scheduler you can set a schedule this graph flow
        run on exact time. (everyday 1pm, every 5hours ... somting like this)
        So that we can feed new data and update model automatically
        ---
        # Class Name : RunManagerSchedule

        # Description:
            create schedule params sets
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def get(self, request, nnid):
        """
        Training Job schedule management
        We have predefined set of graph flow.. on Scheduler you can set a schedule this graph flow
        run on exact time. (everyday 1pm, every 5hours ... somting like this)
        So that we can feed new data and update model automatically
        ---
        # Class Name : RunManagerSchedule

        # Description:
            get schedule params for selected nn_id
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def put(self, request, nnid):
        """
        Training Job schedule management
        We have predefined set of graph flow.. on Scheduler you can set a schedule this graph flow
        run on exact time. (everyday 1pm, every 5hours ... somting like this)
        So that we can feed new data and update model automatically
        ---
        # Class Name : RunManagerSchedule

        # Description:
            modify schedule params for selected nn_id
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def delete(self, request, nnid):
        """
        Training Job schedule management
        We have predefined set of graph flow.. on Scheduler you can set a schedule this graph flow
        run on exact time. (everyday 1pm, every 5hours ... somting like this)
        So that we can feed new data and update model automatically
        ---
        # Class Name : RunManagerSchedule

        # Description:
            delete schedule params for selected nn_id
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))
