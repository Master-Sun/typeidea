from django import template
from comment.forms import CommentForm
from comment.models import Comment


# 自定义模板标签
register = template.Library()
# 配置评论模板，前端页面直接当成标签渲染
@register.inclusion_tag('comment/block.html')
def comment_block(target):
    return {
        # 自定义标签中默认没有request对象，因此需要手动将target添加到页面中
        'target': target,
        'comment_form': CommentForm,
        'comment_list': Comment.get_by_target(target),
    }