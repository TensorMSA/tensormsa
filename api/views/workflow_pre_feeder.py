import json
from rest_framework.response import Response
from rest_framework.views import APIView
from master.workflow.preprocess.workflow_feed_fr2seq import WorkflowFeedFr2Seq
from master.workflow.preprocess.workflow_feed_fr2wv import WorkflowFeedFr2Wv
from master.workflow.preprocess.workflow_feed_fr2auto import WorkflowFeedFr2Auto
from master.workflow.preprocess.workflow_feed_fr2wcnn import WorkflowFeedFr2Wcnn
from master.workflow.preprocess.workflow_feed_iob2bilstmcrf import WorkflowFeedIob2BiLstmCrf
import coreapi

class WorkFlowPreFeeder(APIView) :
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
    def post(self, request, src, net, nnid, ver, node):
        """
        - desc : insert data
        """
        try:
            nodeid = ''.join([nnid, '_', ver, '_', node])
            if(src == 'frame' and net == 'seq2seq') :
                return_data = WorkflowFeedFr2Seq().set_view_obj(nodeid , request.data)
            elif(src == 'frame' and net == 'word2vec') :
                return_data = WorkflowFeedFr2Wv().set_view_obj(nodeid, request.data)
            elif (src == 'frame' and net == 'autoencoder'):
                return_data = WorkflowFeedFr2Auto().set_view_obj(nodeid, request.data)
            elif (src == 'frame' and net == 'wcnn'):
                return_data = WorkflowFeedFr2Wcnn().set_view_obj(nodeid, request.data)
            elif (src == 'iob' and net == 'bilstmcrf'):
                return_data = WorkflowFeedIob2BiLstmCrf().set_view_obj(nodeid, request.data)
            else :
                raise Exception("not supported converting type")
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def get(self, request, src, net, nnid, ver, node):
        """
        - desc : get data
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def put(self, request, src, net, nnid, ver, node):
        """
        - desc ; update data
        """
        try:
            nodeid = ''.join([nnid, '_', ver, '_', node])
            if(src == 'frame' and net == 'seq2seq') :
                return_data = WorkflowFeedFr2Seq().set_view_obj(nodeid , request.data)
            elif (src == 'frame' and net == 'word2vec'):
                return_data = WorkflowFeedFr2Wv(nodeid).set_view_obj(nodeid, request.data)
            elif (src == 'frame' and net == 'autoencoder'):
                return_data = WorkflowFeedFr2Auto().set_view_obj(nodeid, request.data)
            elif (src == 'frame' and net == 'wcnn'):
                return_data = WorkflowFeedFr2Wcnn().set_view_obj(nodeid, request.data)
            elif (src == 'iob' and net == 'bilstmcrf'):
                return_data = WorkflowFeedIob2BiLstmCrf().set_view_obj(nodeid, request.data)
            else :
                raise Exception("not supported converting type")
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def delete(self, request, src, net, nnid, ver, node):
        """
        - desc : delete  data
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))
