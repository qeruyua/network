import upfile.views
from django.urls import path,include

urlpatterns = [
    path('index',upfile.views.index),
    path('showfeature',upfile.views.showfeature),
    path('getfeatures',upfile.views.getfeatures),
    path('search',upfile.views.search),
    path('bigdataArea',upfile.views.bigdataArea),
    path('portpie',upfile.views.portpie),
    path('upfilemodel',upfile.views.upfilemodel),

    path('cutsession',upfile.views.cutsession),
    path('cutflow',upfile.views.cutflow),
    path('composesession',upfile.views.composesession),
    path('composeflow',upfile.views.composeflow),
    path('getcomposeflow',upfile.views.getcomposeflow),
    path('searchflow',upfile.views.searchflow),
    path('searchsession',upfile.views.searchsession),
    path('getcomposesession',upfile.views.getcomposesession),

    path('test1',upfile.views.test1),
    path('test',upfile.views.test),

]