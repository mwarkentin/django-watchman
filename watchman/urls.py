# -*- coding: utf-8 -*-

from django.urls import re_path

from watchman import views


urlpatterns = [
    re_path(r'^$', views.status, name="status"),
    re_path(r'^dashboard/$', views.dashboard, name="dashboard"),
    re_path(r'^ping/$', views.ping, name="ping"),
]
