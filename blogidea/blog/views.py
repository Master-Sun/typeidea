from blog.models import *
from config.models import SideBar
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.generic import DetailView, ListView


def post_list(request, category_id=None, tag_id=None):
    tag = None
    category = None
    if tag_id:
        post_list, tag = Post.get_by_tag(tag_id)
    elif category_id:
        post_list, category = Post.get_by_category(category_id)
    else:
        post_list = Post.latest_posts()
    context = {
        'post_list': post_list,
        'tag': tag,
        'category': category,
        'sidebars': SideBar.get_all(),
    }
    # 响应数据中加入分类信息
    context.update(Category.get_navs())
    return render(request, 'blog/list.html', context=context)


def post_detail(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        post = None
        tag_list = []
    else:
        # 多对多关系中查询出主表中所有的标签
        tag_list = post.tag.all().filter(status=Tag.STATUS_NORMAL)
    context = {
        'post': post,
        'tag_list': tag_list,
        'sidebars': SideBar.get_all(),
    }
    context.update(Category.get_navs())
    return render(request, 'blog/detail.html', context=context)


class CommonViewMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'sidebars': SideBar.get_all(),
        })
        context.update(Category.get_navs())
        return context


# DetailView继承自View，实现get方法，可以绑定某一模板并获取单个实例数据
class PostDetailView(CommonViewMixin, DetailView):
    queryset = Post.latest_posts()
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'    # 设置url中的参数名，默认为pk


class IndexView(CommonViewMixin, ListView):
    queryset = Post.latest_posts()    # 设置基础的数据集，和model属性二选一，比model多提供了过滤功能
    paginate_by = 2    # 每页显示的数量
    context_object_name = 'post_list'    # 模板中使用的变量名，默认为object_list
    template_name = 'blog/list.html'


# 分类列表页
class CategoryView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')    # 从url中取参数
        category = get_object_or_404(Category, pk=category_id)
        context.update({
            'category': category,
        })
        return context

    def get_queryset(self):
        """重写queryset，根据分类过滤"""
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)


# 标签列表页
class TagView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')  # 从url中取参数
        tag = get_object_or_404(Tag, pk=tag_id)
        context.update({
            'tag': tag,
        })
        return context

    def get_queryset(self):
        """重写queryset，根据分类过滤"""
        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        return queryset.filter(category_id=tag_id)