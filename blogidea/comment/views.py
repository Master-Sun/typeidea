from comment.forms import CommentForm
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView


# 定义评论提交的视图类
class CommentView(TemplateView):
    http_method_names = ['post']    # 该视图类仅提供post方法
    template_name = 'comment/result.html'

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST)  # 接受form表单数据
        target = request.POST.get('target')

        if comment_form.is_valid():
            # 此处通过form表单对象创建了一个实例，不用再创建comment的对象了
            instance = comment_form.save(commit=False)
            instance.target = target
            instance.nickname = request.user.first_name
            instance.website = reverse('author', args=(request.user.id,))
            email = request.user.email
            instance.save()
            succeed = True
            return redirect(target)
        else:
            succeed = False
        context = {
            'succeed': succeed,
            # 若发生异常，form表单对象中会存入异常信息
            'form': comment_form,
            'target': target,
        }
        # 将数据渲染到响应对象和模板中
        return self.render_to_response(context)
