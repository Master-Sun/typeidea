from blog.models import *
from config.models import SideBar
from django.shortcuts import render


# Create your views here.
from django.views.generic import DetailView


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


# DetailView继承自View，实现get方法，可以绑定某一模板并获取单个实例数据
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'