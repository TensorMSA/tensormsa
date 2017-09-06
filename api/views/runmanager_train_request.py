import json
from rest_framework.response import Response
from rest_framework.views import APIView
from cluster.service.service_train_task import train
from celery.task.control import inspect
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)
import coreapi

class RunManagerTrainRequest(APIView):

    def post(self, request, nnid, ver):
        """
        We can execute whole process from data extraction > data preprocessing > train model > eval
        Process of execute single graph flow is like bellow
        (1) Set Network Id  \n
        (2) Set Version Id  \n
        (3) Set set graph flow  \n
        (4) Set each nodes params on graph  \n
        (5) Run graph flow of certain version defined on (2)   <-- here .. this step    \n
        (6) Service output model    \n
        ---
        # Class Name : RunManagerTrainRequest

        # Description:
            execute all process at once
        """
        try:
            if(self._same_request_check(nnid, ver) == 'run'):
                result = train.delay(nnid, ver)
                return Response(json.dumps({"status": "200", "id": result.id, "state": result.state}))
            elif(self._same_request_check(nnid, ver) == 'debug'):
                result = train(nnid, ver)
                return Response(json.dumps(result))
            else :
                return_data = {"status": "404", "result": str("same ID is already on training")}
                return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def get(self, request, nnid, ver):
        """
        We can execute whole process from data extraction > data preprocessing > train model > eval
        Process of execute single graph flow is like bellow
        (1) Set Network Id  \n
        (2) Set Version Id  \n
        (3) Set set graph flow  \n
        (4) Set each nodes params on graph  \n
        (5) Run graph flow of certain version defined on (2)   <-- here .. this step    \n
        (6) Service output model    \n
        ---
        # Class Name : RunManagerTrainRequest

        # Description:
            get status of process (scheduled, active, reserved, done.. )
        """
        try:
            return_data = {}
            return_data['scheduled'] = []
            return_data['active'] = []
            return_data['reserved'] = []

            i = inspect()

            for req in i.active()[list(i.scheduled().keys())[0]]:
                return_data['scheduled'].append(req.get('args'))
            for req in i.active()[list(i.active().keys())[0]]:
                return_data['active'].append(req.get('args'))
            for req in i.active()[list(i.reserved().keys())[0]]:
                return_data['reserved'].append(req.get('args'))
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def put(self, request, nnid, ver):
        """
        We can execute whole process from data extraction > data preprocessing > train model > eval
        Process of execute single graph flow is like bellow
        (1) Set Network Id  \n
        (2) Set Version Id  \n
        (3) Set set graph flow  \n
        (4) Set each nodes params on graph  \n
        (5) Run graph flow of certain version defined on (2)   <-- here .. this step    \n
        (6) Service output model    \n
        ---
        # Class Name : RunManagerTrainRequest

        # Description:
            Change status.. like stop processing task..
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def _same_request_check(self, nn_id, ver):
        """
        check if already running job requested again
        :return: boolean
        """
        i = inspect()
        if(i.active() == None) :
            return 'debug'
        for req in i.active()[list(i.active().keys())[0]] :
            if (''.join(['(\'', nn_id, '\', \'' , ver, '\')']) == req.get('args')) :
                return 'reject'
        return 'run'
