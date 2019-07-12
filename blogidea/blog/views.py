from blog.models import *
from comment.forms import CommentForm
from comment.models import Comment
from config.models import SideBar
from datetime import date
from django.db.models import Q, F
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.core.cache import cache
from django.views.generic import DetailView, ListView


# def post_list(request, category_id=None, tag_id=None):
#     tag = None
#     category = None
#     if tag_id:
#         post_list, tag = Post.get_by_tag(tag_id)
#     elif category_id:
#         post_list, category = Post.get_by_category(category_id)
#     else:
#         post_list = Post.latest_posts()
#     context = {
#         'post_list': post_list,
#         'tag': tag,
#         'category': category,
#         'sidebars': SideBar.get_all(),
#     }
#     # 响应数据中加入分类信息
#     context.update(Category.get_navs())
#     return render(request, 'blog/list.html', context=context)


def post_detail(request, post_id):
    try:
        # 考虑id不存在的情况
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


# 处理通用数据：导航栏和侧边栏
class CommonViewMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'sidebars': SideBar.get_all(),
        })
        context.update(Category.get_navs())
        return context


# 详情页：DetailView继承自View，实现get方法，可以绑定某一模板并获取单个实例数据
# 继承自CommonViewMixin获取通用数据
class PostDetailView(CommonViewMixin, DetailView):
    queryset = Post.latest_posts()
    template_name = 'blog/detail.html'
    context_object_name = 'post'    #　设置模板中使用的变量名
    pk_url_kwarg = 'post_id'    # 设置url中的参数名，默认为pk

    # 重写get方法，在其中处理访问统计
    def get(self, request, *args, **kwargs):
        self.handle_visited()  # 在拿到响应数据后才调用统计方法，则无法返回实时数据给前端
        # 调用父类中的get方法后，self对象多了一个object属性，应该是指代当前post的实例
        response = super().get(request, *args, **kwargs)
        return response

    def handle_visited(self):
        increase_pv = False
        increase_uv = False
        uid = self.request.uid
        post_id = self.kwargs.get('post_id')
        # 生成针对每篇文章的key值
        pv_key = 'pv:%s:%s' % (uid, self.request.path)
        uv_key = 'uv:%s:%s:%s' % (uid, str(date.today()), self.request.path)
        print(pv_key, uv_key)
        # 判断缓存中是否有pv_key，没有则创建，有效期1分钟，并将标志位改为True
        if not cache.get(pv_key):
            print('进了pv')
            increase_pv = True
            cache.set(pv_key, 1, 1*60)
        if not cache.get(uv_key):
            print('进了uv')
            increase_uv = True
            cache.set(uv_key, 1, 24*60*60)

        # 根据标志位判断是否执行写入操作
        # 此条件可避免出现两次写入操作
        if increase_pv and increase_uv:
            Post.objects.filter(pk=post_id).update(pv=F('pv')+1, uv=F('uv')+1)
        elif increase_pv:
            Post.objects.filter(pk=post_id).update(pv=F('pv') + 1)
        elif increase_uv:
            Post.objects.filter(pk=post_id).update(uv=F('uv') + 1)





# 列表页：ListView继承自View，实现get方法，可通过绑定模板来批量获取数据，提供分页功能
class IndexView(CommonViewMixin, ListView):
    queryset = Post.latest_posts()    # 设置基础的数据集，和model属性二选一，比model多提供了过滤功能
    paginate_by = 2    # 每页显示的数量
    context_object_name = 'post_list'    # 模板中使用的变量名，默认为object_list
    template_name = 'blog/list.html'


# 分类列表页
class CategoryView(IndexView):
    # 拿到需要渲染到模板中的数据
    def get_context_data(self, **kwargs):
        # 逻辑顺序：先调用父类IndexView中的get_context_data，但他没有，于是再去找CommonViewMixin
        # 在里面又调用了一次父类中的方法，此时会去找ListView，最终拿到列表页的数据
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')    # 从url中取参数
        # 获取一个对象的实例，如果不存在则抛出404错误
        category = get_object_or_404(Category, pk=category_id)
        context.update({
            'category': category,
        })
        return context

    # 此方法获取数据源
    def get_queryset(self):
        """重写queryset，根据分类过滤"""
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')    # 从url中获取参数
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


class SearchView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'keyword': self.request.GET.get('keyword', ''),
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get('keyword')
        if not keyword:
            return queryset
        return queryset.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword))


class AuthorView(IndexView):
    def get_queryset(self):
        queryset = super().get_queryset()
        author_id = self.kwargs.get('author_id')
        return queryset.filter(owner_id=author_id)

