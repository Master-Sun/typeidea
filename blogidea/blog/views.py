from blog.models import *
from django.shortcuts import render


# Create your views here.
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
    }
    return render(request, 'blog/list.html', context=context)

def post_detail(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        post = None
        tag_list = []
    else:
        print(post.tag, type(post.tag))
        tag_list = []
        # tag_list = post.tag_set.filter(status=Tag.STATUS_NORMAL)
    context = {
        'post': post,
        'tag_list': tag_list
    }
    return render(request, 'blog/detail.html', context=context)