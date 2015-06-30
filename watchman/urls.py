# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^$', 'watchman.views.status', name="status"),
    url(r'^dashboard/$', 'watchman.views.dashboard', name="dashboard"),
)
