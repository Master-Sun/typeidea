"""blogidea URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from blogidea.custom_site import custom_site
from django.conf.urls import url
from django.contrib import admin
from blog.views import *


urlpatterns = [
    url(r'^$', post_list, name='index'),
    url(r'post/(?P<post_id>\d+)/$', post_detail, name='post-detail'),
    url(r'category/(?P<category_id>\d+)/$', post_list, name='category-list'),
    url(r'tag/(?P<tag_id>\d+)/$', post_list, name='tag-list'),
    url(r'^super_admin/', admin.site.urls, name='super-admin'),    # 管理用户，使用jango自带的site
    url(r'^admin/', custom_site.urls, name=admin),         # 管理业务，使用自定义的站点
]
