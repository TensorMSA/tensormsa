from django.core.serializers.json import json, DjangoJSONEncoder
from rest_framework.response import Response
from rest_framework.views import APIView
from master.network.nn_common_manager import NNCommonManager
import logging
import coreapi

class CommonNNInfoList(APIView):
    """
    """
    coreapi_fields = (
        coreapi.Field(
            name='nn_id',
            required=True,
            type="string"
        ),
        coreapi.Field(
            name='biz_cate',
            required=True,
            type='string',
        ),
        coreapi.Field(
            name='biz_sub_cate',
            required=True,
            type='string',
        ),
        coreapi.Field(
            name='nn_title',
            required=True,
            type='string',
        ),
        coreapi.Field(
            name='nn_desc',
            required=True,
            type='string',
        ),
        coreapi.Field(
            name='use_flag',
            required=True,
            type='string',
        ),
        coreapi.Field(
            name='dir',
            required=True,
            type='string',
        ),
        coreapi.Field(
            name='config',
            required=True,
            type='string',
        ),
    )
    def post(self, request, nnid):
        """
        Common Network Info Post Method
        ---
        # Class Name : CommonNNInfoList

        # Description:
            Structure : <nninfo> - version - batch version
            Define new neural network process
        """
        try:
            input_parm = request.data
            max_nnid = NNCommonManager().get_nn_id_max() + 1
            if nnid == "":
                nnid = "nn" + str(max_nnid).zfill(8)
            else:
                return_data = NNCommonManager().get_nn_id_info(nnid)
                if return_data != []:
                    return Response(json.dumps(nnid+" Network ID already exists"))
            input_parm['nn_id'] = nnid
            if input_parm.get('automl_parms') == None:
                input_parm['automl_parms'] = {}
            if input_parm.get('automl_runtime') == None:
                input_parm['automl_runtime'] = {}
            if input_parm.get('automl_stat') == None:
                input_parm['automl_stat'] = {}

            input_parm_s = {}
            input_parm_s['id'] = max_nnid
            input_parm_s['nn_id'] = nnid
            return_data = NNCommonManager().insert_nn_info(input_parm, input_parm_s)
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def get(self, request, nnid):
        """
        Common Network Info Get Method
        ---
        # Class Name : CommonNNInfoList

        # Description:
            Structure : <nninfo> - version - batch version
            Search deinfed list of neural networks
        """
        try:
            condition = {}
            condition['nn_id'] = nnid
            if str(nnid).lower() == 'all':
                condition['nn_id'] = '%'
            elif str(nnid).lower() == 'seq':
                condition['nn_id'] = 'seq'
            return_data = NNCommonManager().get_nn_info(condition)
            logging.info(return_data)
            return Response(json.dumps(return_data, cls=DjangoJSONEncoder))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data, cls=DjangoJSONEncoder))

    def put(self, request, nnid):
        """
        Common Network Info Put Method
        ---
        # Class Name : CommonNNInfoList

        # Description:
            Structure : <nninfo> - version - batch version
            Modifiy already defined neuralnetwork info
        """
        try:
            input_parm = request.data
            input_parm['nn_id'] = nnid
            if input_parm.get('automl_parms') == None:
                input_parm['automl_parms'] = {}
            if input_parm.get('automl_runtime') == None:
                input_parm['automl_runtime'] = {}
            if input_parm.get('automl_stat') == None:
                input_parm['automl_stat'] = {}
            return_data = NNCommonManager().update_nn_info(input_parm)
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def delete(self, request, nnid):
        """
        Common Network Info Delete Method
        ---
        # Class Name : CommonNNInfoList

        # Description:
            Structure : <nninfo> - version - batch version
            Delete selected neuralnetwork from list (careful cannot be undo)
            Delete all related info list version, batch, model and etc
        """
        try:
            input_parm = request.data
            input_parm['nn_id'] = nnid
            return_data = NNCommonManager().delete_nn_info(input_parm)
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))
