"""hoyai URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt

from api import views as rest_view

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # server info
    url(r'^api/v1/type/server/target/etl/(?P<type>.*)/',
        csrf_exempt(rest_view.ConfServerData.as_view())),
    url(r'^api/v1/type/server/target/master/(?P<type>.*)/',
        csrf_exempt(rest_view.ConfServerData.as_view())),
    url(r'^api/v1/type/server/target/cluster/(?P<type>.*)/',
        csrf_exempt(rest_view.ConfServerData.as_view())),

    # net definition manager
    url(r'^api/v1/type/common/target/nninfo/(?P<nnid>.*)/',
        csrf_exempt(rest_view.CommonNNInfoList.as_view())),
    url(r'^api/v1/type/common/target/nninfo/',
        csrf_exempt(rest_view.CommonNNInfoList.as_view())),

    # rule management
    url(r'^api/v1/type/rule/target/cate/',
        csrf_exempt(rest_view.CommonNNInfoList.as_view())),
    url(r'^api/v1/type/rule/target/cate/(?P<cate>.*)/subcate/',
        csrf_exempt(rest_view.CommonNNInfoList.as_view())),

    # run management (cluster)
    url(r'^api/v1/type/train/nnid/(?P<nnid>.*)/node/(?P<node>.*)/',
        csrf_exempt(rest_view.ClusterSingleRequest.as_view())),
    url(r'^api/v1/type/cluster/target/service/(?P<nnid>.*)/',
        csrf_exempt(rest_view.ClusterTrainRequest.as_view())),

    # workflow init
    url(r'^api/v1/type/wf/target/init/mode/easy/(?P<nnid>.*)/',
        csrf_exempt(rest_view.WorkFlowInitEasy.as_view())),
    url(r'^api/v1/type/wf/target/init/mode/custom/(?P<nnid>.*)/',
        csrf_exempt(rest_view.WorkFlowInitCustom.as_view())),
    url(r'^api/v1/type/wf/target/init/mode/history/(?P<nnid>.*)/ver//(?P<ver>.*)/batch//(?P<bver>.*)/',
        csrf_exempt(rest_view.WorkFlowInitHistory.as_view())),
    url(r'^api/v1/type/wf/target/init/mode/history/(?P<nnid>.*)/active/(?P<ver>.*)/',
        csrf_exempt(rest_view.WorkFlowInitHistory.as_view())),
    url(r'^api/v1/type/wf/target/init/mode/history/(?P<nnid>.*)/',
        csrf_exempt(rest_view.WorkFlowInitHistory.as_view())),
    url(r'^api/v1/type/wf/target/state/nnid/(?P<nnid>.*)/wfver/(?P<wfver>.*)/',
        csrf_exempt(rest_view.WorkFlowStateManager.as_view())),
    url(r'^api/v1/type/wf/target/node/nnid/(?P<nnid>.*)/wfver/(?P<wfver>.*)/',
        csrf_exempt(rest_view.WorkFlowNodeManager.as_view())),
    url(r'^api/v1/type/wf/target/menu/',
        csrf_exempt(rest_view.WorkFlowMenuManager.as_view())),

    # data APIs
    url(r'^api/v1/type/wf/state/data/detail/localimg/prg/source/nnid/(?P<nnid>.*)/ver/(?P<ver>.*)/',
        csrf_exempt(rest_view.WorkFlowDataImgSourceLocal.as_view())),
    url(r'^api/v1/type/wf/state/data/detail/localimg/prg/pre/nnid/(?P<nnid>.*)/ver/(?P<ver>.*)/',
        csrf_exempt(rest_view.WorkFlowDataImgPre.as_view())),
    url(r'^api/v1/type/wf/state/data/detail/localimg/prg/store/nnid/(?P<nnid>.*)/ver/(?P<ver>.*)/',
        csrf_exempt(rest_view.WorkFlowDataImgStore.as_view())),
    url(r'^api/v1/type/wf/state/data/detail/s3img/prg/source/nnid/(?P<nnid>.*)/ver/(?P<ver>.*)/',
        csrf_exempt(rest_view.WorkFlowDataImgSourceS3.as_view())),
    url(r'^api/v1/type/wf/state/data/detail/s3img/pre/source/nnid/(?P<nnid>.*)/ver/(?P<ver>.*)/',
        csrf_exempt(rest_view.WorkFlowDataImgPre.as_view())),
    url(r'^api/v1/type/wf/state/data/detail/s3img/store/source/nnid/(?P<nnid>.*)/ver/(?P<ver>.*)/',
        csrf_exempt(rest_view.WorkFlowDataImgStore.as_view())),

    url(r'^api/v1/type/wf/state/data/detail/localcsv/prg/source/nnid/(?P<nnid>.*)/ver/(?P<ver>.*)/',
        csrf_exempt(rest_view.WorkFlowDataFrameSourceLocal.as_view())),
    url(r'^api/v1/type/wf/state/data/detail/localcsv/prg/pre/nnid/(?P<nnid>.*)/ver/(?P<ver>.*)/',
        csrf_exempt(rest_view.WorkFlowDataFramePre.as_view())),
    url(r'^api/v1/type/wf/state/data/detail/localcsv/prg/store/nnid/(?P<nnid>.*)/ver/(?P<ver>.*)/',
        csrf_exempt(rest_view.WorkFlowDataFrameStore.as_view())),

    url(r'^api/v1/type/wf/state/data/detail/rdb/prg/source/nnid/(?P<nnid>.*)/ver/(?P<ver>.*)/',
        csrf_exempt(rest_view.WorkFlowDataFrameSourceRdb.as_view())),
    url(r'^api/v1/type/wf/state/data/detail/rdb/prg/pre/nnid/(?P<nnid>.*)/ver/(?P<ver>.*)/',
        csrf_exempt(rest_view.WorkFlowDataFramePre.as_view())),
    url(r'^api/v1/type/wf/state/data/detail/rdb/prg/store/nnid/(?P<nnid>.*)/ver/(?P<ver>.*)/',
        csrf_exempt(rest_view.WorkFlowDataFrameStore.as_view())),

    url(r'^api/v1/type/wf/state/data/detail/hbase/prg/source/nnid/(?P<nnid>.*)/ver/(?P<ver>.*)/',
        csrf_exempt(rest_view.WorkFlowDataFrameSourceHbase.as_view())),
    url(r'^api/v1/type/wf/state/data/detail/hbase/prg/pre/nnid/(?P<nnid>.*)/ver/(?P<ver>.*)/',
        csrf_exempt(rest_view.WorkFlowDataFramePre.as_view())),
    url(r'^api/v1/type/wf/state/data/detail/hbase/prg/store/nnid/(?P<nnid>.*)/ver/(?P<ver>.*)/',
        csrf_exempt(rest_view.WorkFlowDataFrameStore.as_view())),

    url(r'^api/v1/type/wf/state/data/detail/s3/prg/source/nnid/(?P<nnid>.*)/ver/(?P<ver>.*)/',
        csrf_exempt(rest_view.WorkFlowDataFrameSourceS3.as_view())),
    url(r'^api/v1/type/wf/state/data/detail/s3/prg/pre/nnid/(?P<nnid>.*)/ver/(?P<ver>.*)/',
        csrf_exempt(rest_view.WorkFlowDataFramePre.as_view())),
    url(r'^api/v1/type/wf/state/data/detail/s3/prg/store/nnid/(?P<nnid>.*)/ver/(?P<ver>.*)/',
        csrf_exempt(rest_view.WorkFlowDataFrameStore.as_view())),

    # data config APIs
    url(r'^api/v1/type/wf/state/dataconf/detail/frame/nnid/(?P<nnid>.*)/ver/(?P<ver>.*)/',
        csrf_exempt(rest_view.WorkFlowDataConfFrame.as_view())),
    url(r'^api/v1/type/wf/state/dataconf/detail/image/nnid/(?P<nnid>.*)/ver/(?P<ver>.*)/',
        csrf_exempt(rest_view.WorkFlowDataConfImage.as_view())),

    # preprocess APIs
    url(r'^api/v1/type/wf/state/pre/detail/predict/nnid/(?P<nnid>.*)/ver/(?P<ver>.*)/',
        csrf_exempt(rest_view.WorkFlowPrePredict.as_view())),
    url(r'^api/v1/type/wf/state/pre/detail/merge/nnid/(?P<nnid>.*)/ver/(?P<ver>.*)/',
        csrf_exempt(rest_view.WorkFlowPreMerge.as_view())),

    # net config APIs
    url(r'^api/v1/type/wf/state/netconf/detail/autoencoder/nnid/(?P<nnid>.*)/ver/(?P<ver>.*)/',
        csrf_exempt(rest_view.WorkFlowNetConfAutoEncoder.as_view())),
    url(r'^api/v1/type/wf/state/netconf/detail/cnn/nnid/(?P<nnid>.*)/ver/(?P<ver>.*)/',
        csrf_exempt(rest_view.WorkFlowNetConfCnn.as_view())),
    url(r'^api/v1/type/wf/state/netconf/detail/gru/nnid/(?P<nnid>.*)/ver/(?P<ver>.*)/',
        csrf_exempt(rest_view.WorkFlowNetConfGru.as_view())),
    url(r'^api/v1/type/wf/state/netconf/detail/lstm/nnid/(?P<nnid>.*)/ver/(?P<ver>.*)/',
        csrf_exempt(rest_view.WorkFlowNetConfLstm.as_view())),
    url(r'^api/v1/type/wf/state/netconf/detail/predefined/nnid/(?P<nnid>.*)/ver/(?P<ver>.*)/',
        csrf_exempt(rest_view.WorkFlowNetConfPredefined.as_view())),
    url(r'^api/v1/type/wf/state/netconf/detail/rnn/nnid/(?P<nnid>.*)/ver/(?P<ver>.*)/',
        csrf_exempt(rest_view.WorkFlowNetConfRnn.as_view())),
    url(r'^api/v1/type/wf/state/netconf/detail/wdnn/nnid/(?P<nnid>.*)/ver/(?P<ver>.*)/',
        csrf_exempt(rest_view.WorkFlowNetConfWdnn.as_view())),
]
