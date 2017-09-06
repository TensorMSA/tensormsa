import json
from rest_framework.response import Response
from rest_framework.views import APIView
from master.network.nn_common_manager import NNCommonManager
import coreapi
from master.workflow.init.workflow_init_simple import WorkFlowSimpleManager
from common.utils import *
import os

class CommonNNInfoVersion(APIView):
    """
    """

    # TODO:add document sample for swagger (need to update)
    coreapi_fields = (
        coreapi.Field(
            name='nn_def_list_info_nn_id',
            required=True,
            type='string',
        ),
        coreapi.Field(
            name='nn_wf_ver_info',
            required=True,
            type='string',
        ),
        coreapi.Field(
            name='condition',
            required=True,
            type='string',
        ),
        coreapi.Field(
            name='active_flag',
            required=True,
            type='string',
        ),
    )
    def post(self, request, nnid):
        """
        Common Network Version Info Post Method
        ---
        # Class Name : CommonNNInfoVersion

        # Description:
            Structure : nninfo - <version> - batch version
            need to define version info under network definition
        """
        try:
            input_data = request.data
            input_data['nn_id'] = nnid
            nnManager = NNCommonManager()
            nn_wf_ver_id = nnManager.get_nn_max_ver(nnid) + 1
            input_data['nn_wf_ver_id'] = nn_wf_ver_id
            return_data = nnManager.insert_nn_wf_info(input_data)
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def get(self, request, nnid):
        """
        Common Network Version Info Get Method
        ---
        # Class Name : CommonNNInfoVersion

        # Description:
            Structure : nninfo - <version> - batch version
            Get version information of selected nnid
        """
        try:
            return_data = NNCommonManager().get_nn_wf_info(nnid)
            conv = []

            node = WorkFlowSimpleManager().get_train_node()

            for row in return_data:
                row["model"] = "N"
                train_filename = row["train_batch_ver_id"]
                pred_filename  = row["pred_batch_ver_id"]
                ver = str(row["nn_wf_ver_id"])
                model_path = get_model_path(nnid, ver, node)
                for fn in os.listdir(model_path):
                    fnsplit = fn.split(".")
                    fnsplitName = fnsplit[0]
                    if (fnsplitName == train_filename):
                        row["train_model"] = fn
                        row["train_model_exists"] = "Y"
                    if (fnsplitName == pred_filename):
                        row["pred_model"] = fn
                        row["pred_model_exists"] = "Y"
                conv.append(row)
            return Response(json.dumps(conv))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def put(self, request, nnid):
        """
        Common Network Version Info Delete Method
        ---
        # Class Name : CommonNNInfoVersion

        # Description:
            Structure : nninfo - <version> - batch version
            Modify seleted nnid's information
        """
        try:
            return_data = NNCommonManager().update_nn_wf_info(nnid, request.data)
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def delete(self, request, nnid):
        """
        Common Network Version Info Delete Method
        ---
        # Class Name : CommonNNInfoVersion

        # Description:
            Structure : nninfo - <version> - batch version
            delete selected network info and related data
        """
        try:

            return_data = NNCommonManager().delete_nn_wf_info(request.data)
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))
