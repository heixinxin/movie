from django.urls import path,re_path
from . import views

app_name='[xiaoshuo]'

urlpatterns = [
    path(r'xiaoshuo/',views.xiaoshuo,name='xiaoshuo'),
    re_path(r'^xiaoshuo/(?P<id>[0-9]+)$',views.xiaoshuoMu,name='xiaoshuoMu'),
]
