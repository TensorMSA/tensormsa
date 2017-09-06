import json
from rest_framework.response import Response
from rest_framework.views import APIView
from master.workflow.netconf.workflow_netconf_autoencoder import WorkFlowNetConfAutoEncoder as AutoEncoder
from common.utils import *
import coreapi

class WorkFlowNetConfAutoEncoder(APIView) :

    coreapi_fields = (
        coreapi.Field(
            name='learning_rate',
            required=True,
            type='float',
        ),
        coreapi.Field(
            name='iter',
            required=True,
            type='int',
        ),
        coreapi.Field(
            name='batch_size',
            required=True,
            type='int',
        ),
        coreapi.Field(
            name='examples_to_show',
            required=True,
            type='10',
        ),
        coreapi.Field(
            name='n_hidden',
            required=True,
            type='list',
        ),
    )
    def post(self, request, nnid):
        """
        This API handles network node information \n
        This is for Stacked AutoEncoder \n
        We designed general form of Autoencoder \n
        You can modify hyperparameters with rest api \n
        ---
        # Class Name : WorkFlowNetConfAutoEncoder

        # Description:
            Set Network configuration for AutoEncoder
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def get(self, request, nnid):
        """
        This API handles network node information \n
        This is for Stacked AutoEncoder \n
        We designed general form of Autoencoder \n
        You can modify hyperparameters with rest api \n
        ---
        # Class Name : WorkFlowNetConfAutoEncoder

        # Description:
            Get Network configuration for AutoEncoder
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def put(self, request, nnid, ver, node):
        """
        This API handles network node information \n
        This is for Stacked AutoEncoder \n
        We designed general form of Autoencoder \n
        You can modify hyperparameters with rest api \n
        ---
        # Class Name : WorkFlowNetConfAutoEncoder

        # Description:
            Modify Network configuration for AutoEncoder
        """
        try:
            input_data = request.data
            #Add Model Path from utils
            input_data['model_path'] = get_model_path(nnid, ver, node)
            node_id = ''.join([nnid, '_', ver , '_', node])
            return_data = AutoEncoder().set_view_obj(node_id, input_data)
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def delete(self, request, nnid):
        """
        This API handles network node information \n
        This is for Stacked AutoEncoder \n
        We designed general form of Autoencoder \n
        You can modify hyperparameters with rest api \n
        ---
        # Class Name : WorkFlowNetConfAutoEncoder

        # Description:
            Reset Network configuration for AutoEncoder
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))
