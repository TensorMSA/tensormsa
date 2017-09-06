import json
from rest_framework.response import Response
from rest_framework.views import APIView
from master.workflow.common.workflow_state_menu import WorkFlowStateMenu
import coreapi

class WorkFlowMenuManager(APIView) :

    coreapi_fields = (
        coreapi.Field(
            name='wf_task_menu_id',
            required=True,
            type='string',
        ),
        coreapi.Field(
            name='wf_task_menu_name',
            required=True,
            type='string',
        ),
        coreapi.Field(
            name='wf_task_menu_desc',
            required=True,
            type='string',
        ),
        coreapi.Field(
            name='visible_flag',
            required=True,
            type='string',
        ),
    )

    def post(self, request):
        """
        This API manages type of nodes \n
        We have several type of node like bellow \n
        (1) Data Extraction node \n
        (2) Data View node \n
        (3) Data Preprocess node \n
        (4) Model configuration and train node  \n
        (5) Model evaluation node \n
        (6) Model inference node \n
        ---
        # Class Name : WorkFlowMenuManager

        # Description:
            Create new type of node if you want but add new category
            doesn'y mean you can use it (need to implement real logic)
        """
        try:
            return_data = WorkFlowStateMenu().put_menu_info(request.data)
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def get(self, request):
        """
        This API manages type of nodes \n
        We have several type of node like bellow \n
        (1) Data Extraction node \n
        (2) Data View node \n
        (3) Data Preprocess node \n
        (4) Model configuration and train node  \n
        (5) Model evaluation node \n
        (6) Model inference node \n
        ---
        # Class Name : WorkFlowMenuManager

        # Description:
            Search node type and status already registered
        """
        try:
            return_data = ""
            WorkFlowStateMenu().get_menu_info()
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def put(self, request):
        """
        This API manages type of nodes \n
        We have several type of node like bellow \n
        (1) Data Extraction node \n
        (2) Data View node \n
        (3) Data Preprocess node \n
        (4) Model configuration and train node  \n
        (5) Model evaluation node \n
        (6) Model inference node \n
        ---
        # Class Name : WorkFlowMenuManager

        # Description:
            Modify node type information
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def delete(self, request):
        """
        This API manages type of nodes \n
        We have several type of node like bellow \n
        (1) Data Extraction node \n
        (2) Data View node \n
        (3) Data Preprocess node \n
        (4) Model configuration and train node  \n
        (5) Model evaluation node \n
        (6) Model inference node \n
        ---
        # Class Name : WorkFlowMenuManager

        # Description:
            Delete node type information
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))
