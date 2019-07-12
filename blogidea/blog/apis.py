from rest_framework import viewsets

from .models import Post, Category
from .serializers import PostSerializer, PostDetailSerializer, CategorySerializer, CategoryDetailSerializer


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    """文档说明，这里的内容可以在接口文档中看到"""
    # 指定序列化的类
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=Post.STATUS_NORMAL)

    # 重写获取详情页数据的接口
    def retrieve(self, request, *args, **kwargs):
        # 重新赋值给serializer_class，以区分列表页和详情页的Serializer
        self.serializer_class = PostDetailSerializer
        return super().retrieve(request, *args, **kwargs)

    # 获取某个分类下的文章列表
    # http://127.0.0.1:8000/api/post/?category=2
    def filter_queryset(self, queryset):
        # 获取URL中category参数，然后进行过滤
        category_id = self.request.query_params.get('category')
        if category_id:
            return queryset.filter(category_id=category_id)
        return queryset


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(status=Category.STATUS_NORMAL)

    # 重写分类的详情页接口，展示分类下的所有文章列表
    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = CategoryDetailSerializer
        return super().retrieve(request, *args, **kwargs)
