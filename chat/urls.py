from django.urls import path,re_path
from . import views
app_name = '[chat]'

urlpatterns = [
    path(r'login.html/', views.login,name='login'),
    path(r'check-login.html/', views.check_login),
    path(r'chat.html/', views.chat),
    path(r'contact-list.html/', views.contact_list),
    path(r'send-msg.html/', views.send_msg),
    path(r'get-msg.html/', views.get_msg),

    path(r'liaotian/',views.liaotian),
    path(r'xianshi/',views.xianshi),
    path(r'baidu/',views.baidu,name='baidu')
]