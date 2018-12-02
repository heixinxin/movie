from django.urls import path,re_path
from . import views

app_name ='[aqiyi]'
urlpatterns = [

    path(r'aqiyi/sousuo',views.sousuo,name ='sousuo'),
    re_path(r'^aqiyi/sousuo/fenji/(?P<aqiyimovieLists>[0-9]+)$',views.sousuo_fenji,name="sousuo_fenji"),
    path(r'aqiyi/',views.aqiyi,name = 'home'),
    re_path(r'^aqiyi/dianyin/(?P<page_id>[0-9])$', views.aqiyi_movie_dianyin, name='dianyin'),
    re_path(r'^aqiyi/TV/(?P<page_id>[0-9])$',views.aqi_movie_TV,name="TVju"),
    re_path(r'aqiyi/zongyi/(?P<page_id>[0-9])',views.aqi_movie_zongyi,name="zongyi"),
    re_path(r'aqiyi/dongman/(?P<page_id>[0-9])',views.aqi_movie_dongman,name="dongman"),
    re_path(r'aqiyi/jilu/(?P<page_id>[0-9])',views.aqi_movie_jilu,name="jilu"),
    re_path(r'^aqiyi/TV/fenji/(?P<aqiyimovieLists>[0-9]+)$',views.aqi_movie_fenji_TV,name="fenji_TV"),
    re_path(r'^aqiyi/zongyi/fenji/(?P<aqiyimovieLists>[0-9]+)$',views.aqi_movie_fenji_zongyi,name="fenji_zongyi"),
    re_path(r'^aqiyi/dongman/fenji/(?P<aqiyimovieLists>[0-9]+)$',views.aqi_movie_fenji_dongman,name="fenji_dongman"),
    re_path(r'^aqiyi/jilu/fenji/(?P<aqiyimovieLists>[0-9]+)$',views.aqi_movie_fenji_jilu,name="fenji_jilu"),

    path(r'youku/',views.youku,name = 'you_home'),
    re_path(r'^youku/dianyin/(?P<page_id>[0-9])$', views.you_movie_dianyin, name='you_dianyin'),
    re_path(r'^youku/TV/(?P<page_id>[0-9])$', views.you_movie_TV, name="you_TVju"),
    re_path(r'youku/zongyi/(?P<page_id>[0-9])', views.you_movie_zongyi, name="you_zongyi"),
    re_path(r'youku/dongman/(?P<page_id>[0-9])', views.you_movie_dongman, name="you_dongman"),
    re_path(r'youku/jilu/(?P<page_id>[0-9])', views.you_movie_jilu, name="you_jilu"),
    re_path(r'^youku/TV/fenji/(?P<aqiyimovieLists>[0-9]+)$', views.you_movie_fenji_TV, name="you_fenji_TV"),
    re_path(r'^youku/zongyi/fenji/(?P<aqiyimovieLists>[0-9]+)$', views.you_movie_fenji_zongyi, name="you_fenji_zongyi"),
    re_path(r'^youku/dongman/fenji/(?P<aqiyimovieLists>[0-9]+)$', views.you_movie_fenji_dongman, name="you_fenji_dongman"),
    re_path(r'^youku/jilu/fenji/(?P<aqiyimovieLists>[0-9]+)$', views.you_movie_fenji_jilu, name="you_fenji_jilu"),

    path(r'tengxu/',views.teng,name = 'teng_home'),
    re_path(r'^tengxu/dianyin/(?P<page_id>[0-9])$', views.teng_movie_dianyin, name='teng_dianyin'),
    re_path(r'^tengxu/TV/(?P<page_id>[0-9])$', views.teng_movie_TV, name="teng_TVju"),
    re_path(r'tengxu/zongyi/(?P<page_id>[0-9])', views.teng_movie_zongyi, name="teng_zongyi"),
    re_path(r'tengxu/dongman/(?P<page_id>[0-9])', views.teng_movie_dongman, name="teng_dongman"),
    re_path(r'tengxu/jilu/(?P<page_id>[0-9])', views.teng_movie_jilu, name="teng_jilu"),
    re_path(r'^tengxu/TV/fenji/(?P<aqiyimovieLists>[0-9]+)$', views.teng_movie_fenji_TV, name="teng_fenji_TV"),
    re_path(r'^tengxu/zongyi/fenji/(?P<aqiyimovieLists>[0-9]+)$', views.teng_movie_fenji_zongyi, name="teng_fenji_zongyi"),
    re_path(r'^tengxu/dongman/fenji/(?P<aqiyimovieLists>[0-9]+)$', views.teng_movie_fenji_dongman, name="teng_fenji_dongman"),
    re_path(r'^tengxu/jilu/fenji/(?P<aqiyimovieLists>[0-9]+)$', views.teng_movie_fenji_jilu, name="teng_fenji_jilu"),
]