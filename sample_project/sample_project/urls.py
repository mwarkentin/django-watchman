from django.conf.urls import include, url
from django.contrib import admin
import watchman.views


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^watchman/', include('watchman.urls')),
    url(r'^watchman/bare/', watchman.views.bare_status, name='bare_status'),
]
