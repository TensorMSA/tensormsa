from rest_framework.views import APIView
from master.network.nn_common_manager import NNCommonManager
from rest_framework.response import Response
import json
import coreapi
from master.workflow.init.workflow_init_simple import WorkFlowSimpleManager
from common.utils import *
import os

class CommonNNInfoBatch(APIView):
    """
    
    """
    # TODO:add document sample for swagger (need to update)
    coreapi_fields = (
        coreapi.Field(
            name='parm1',
            required=True,
            type='string',
        ),
        coreapi.Field(
            name='parm2',
            required=True,
            type='string',
        ),
    )
    def get(self, request, nnid, ver):
        """
        Your docs
        ---
        # Class Name (must be separated by `---`)

        # Description:
            - name: name
              description: Foobar long description goes here
        """
        try:
            return_data = NNCommonManager().get_nn_batch_info(nnid, ver)
            conv = []

            node = WorkFlowSimpleManager().get_train_node()
            model_path = get_model_path(nnid, ver, node)

            for row in return_data:
                row["model"] = "N"
                filename = row["nn_batch_ver_id"]

                for fn in os.listdir(model_path):
                    fnsplit = fn.split(".")
                    fnsplitName = fnsplit[0]
                    if (fnsplitName == filename):
                        row["model"] = fn
                        row["model_exists"] = "Y"
                if row["result_info"] != None:
                    predicts = row["result_info"]["predicts"]

                    tfTot = 0
                    fTot = 0
                    tTot = 0
                    for i in range(len(predicts)):
                        for j in range(len(predicts[i])):
                            if i == j:
                                tTot += predicts[i][j]
                            else:
                                fTot += predicts[i][j]
                    row["true_cnt"] = tTot
                    row["false_cnt"] = fTot
                    tfTot = tTot+fTot
                    row["true_false_cnt"] = tfTot
                    if tfTot == 0:
                        tfTot = 1
                    row["true_false_percent"] = round(tTot/tfTot*100)

                conv.append(row)
            return Response(json.dumps(conv))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def put(self, request, nnid, ver):
        """
        Your docs
        ---
        # Class Name (must be separated by `---`)

        # Description:
            - name: name
              description: Foobar long description goes here
        """
        try:
            return_data = NNCommonManager().update_nn_batch_info(nnid, ver, request.data)
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))
