# -*- coding: utf-8 -*-

from django.conf.urls import url

from watchman import views


urlpatterns = [
    url(r'^$', views.status, name="status"),
    url(r'^dashboard/$', views.dashboard, name="dashboard"),
    url(r'^ping/$', views.ping, name="ping"),
]
