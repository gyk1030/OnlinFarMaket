# -*- coding: utf-8 -*-
from django.conf.urls import url
from df_goods import views, tests


urlpatterns=[
    url(r'^$',views.index),
    url(r'^list(\d+)_(\d+)_(\d+)/$', views.goodlist),
    url(r'^(\d+)/$', views.detail),
    url(r'^test/$', tests.test),
    url(r'^search_(\d+)_(\d+)/$', views.search),
]