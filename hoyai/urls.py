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
    url(r'^api/v1/type/server/target/etl/(?P<type>.*)/',
        csrf_exempt(rest_view.ConfServerData.as_view())),
    url(r'^api/v1/type/server/target/master/(?P<type>.*)/',
        csrf_exempt(rest_view.ConfServerData.as_view())),
    url(r'^api/v1/type/server/target/cluster/(?P<type>.*)/',
        csrf_exempt(rest_view.ConfServerData.as_view())),

    url(r'^api/v1/type/common/target/nninfo/(?P<nnid>.*)/',
        csrf_exempt(rest_view.CommonNNInfoList.as_view())),
    url(r'^api/v1/type/common/target/nninfo/',
        csrf_exempt(rest_view.CommonNNInfoList.as_view())),

    url(r'^api/v1/type/rule/target/cate/',
        csrf_exempt(rest_view.CommonNNInfoList.as_view())),
    url(r'^api/v1/type/rule/target/cate/(?P<cate>.*)/subcate/',
        csrf_exempt(rest_view.CommonNNInfoList.as_view())),

    url(r'^api/v1/type/cluster/target/service/(?P<nnid>.*)/',
        csrf_exempt(rest_view.ClusterTrainRequest.as_view())),
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
]
