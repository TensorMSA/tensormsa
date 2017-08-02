from django.core.serializers.json import json, DjangoJSONEncoder
from rest_framework.response import Response
from rest_framework.views import APIView
from master.network.nn_common_manager import NNCommonManager
import logging
import coreapi

class CommonNNInfoList(APIView):
    """
    """
    # TODO:add document sample for swagger (need to update)
    coreapi_fields = (
        coreapi.Field(
            name='parm1',
            required=True,
            schema=coreapi.Field(name='parm3',
                                 required=True,
                                 description='haha',
                                 type='float')
        ),
        coreapi.Field(
            name='parm2',
            required=True,
            type='string',
        ),
    )
    def post(self, request, nnid):
        """
        Your docs
        ---
        # Class Name (must be separated by `---`)

        # Description:
            - name: name
              description: Foobar long description goes here
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
        Your docs
        ---
        # Class Name (must be separated by `---`)

        # Description:
            - name: name
              description: Foobar long description goes here
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
        Your docs
        ---
        # Class Name (must be separated by `---`)

        # Description:
            - name: name
              description: Foobar long description goes here
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
        Your docs
        ---
        # Class Name (must be separated by `---`)

        # Description:
            - name: name
              description: Foobar long description goes here
        """
        try:
            input_parm = request.data
            input_parm['nn_id'] = nnid
            return_data = NNCommonManager().delete_nn_info(input_parm)
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))
