"""sample_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  re_path(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  re_path(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  re_path(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, re_path

import watchman.views

urlpatterns = [
    re_path(r"^admin/", admin.site.urls),
    re_path(r"^watchman/", include("watchman.urls")),
    re_path(r"^watchman/bare/", watchman.views.bare_status, name="bare_status"),
]
