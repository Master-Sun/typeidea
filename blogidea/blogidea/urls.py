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
from comment.views import CommentView
from config.views import LinkListView
from django.contrib import admin
from blog.views import *

import xadmin

from .autocomplete import TagAutocomplete, CategoryAutocomplete

from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings

# from blog.apis import post_list, PostList

from rest_framework.routers import DefaultRouter
from blog.apis import PostViewSet, CategoryViewSet
from rest_framework.documentation import include_docs_urls

router = DefaultRouter()
router.register(r'post', PostViewSet, base_name='api-post')
router.register(r'category', CategoryViewSet, base_name='api-category')

urlpatterns = [
    # 此url将提供多个接口，如： 列表页：/api/post/    详情页：/api/post/<post_id>/
    url(r'^api/', include(router.urls, namespace='api')),
    url(r'^api/docs/', include_docs_urls(title='blogidea apis')),
    # url(r'^api/post/', post_list, name='post-list'),
    # url(r'^api/post/', PostList.as_view(), name='post-list'),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'post/(?P<post_id>\d+)/$', PostDetailView.as_view(), name='post-detail'),    # pk为查询过滤参数
    url(r'category/(?P<category_id>\d+)/$', CategoryView.as_view(), name='category-list'),
    url(r'tag/(?P<tag_id>\d+)/$', TagView.as_view(), name='tag-list'),
    url(r'search/$', SearchView.as_view(), name='search'),
    url(r'author/(?P<author_id>\d+)/$', AuthorView.as_view(), name='author'),
    url(r'links/$', LinkListView.as_view(), name='links'),
    url(r'comment/$', CommentView.as_view(), name='comment'),
    url(r'^super_admin/', admin.site.urls, name='super-admin'),    # 管理用户，使用jango自带的site
    url(r'^admin/', xadmin.site.urls, name='xadmin'),         # 设置为xadmin站点
    url(r'^category-autocomplete/$', CategoryAutocomplete.as_view(), name='category-autocomplete'),
    url(r'^tag-autocomplete/$', TagAutocomplete.as_view(), name='tag-autocomplete'),
    # 提供上传图片和浏览图片的接口
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    # 配置图片资源的访问，使用django内置的静态文件处理功能提供静态文件服务
    # 在正式环境中，这个功能由Nginx来完成
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# 在DEBUG=True时配置调试工具的url接口
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
