from dal import autocomplete

from blog.models import Category, Tag


# 配置所有需要自动补全的接口，可以理解为自动补全的view层
class CategoryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # 若未登录，则返回空的queryset，因结果还会被其他模块处理，所以不能直接返回None
        if not self.request.user.is_authenticated():
            return Category.objects.none()

        qs = Category.objects.filter(owner=self.request.user)
        # 这里的q是url上传递过来的值
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class TagAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Tag.objects.none()
        qs = Tag.objects.filter(owner=self.request.user)
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs
