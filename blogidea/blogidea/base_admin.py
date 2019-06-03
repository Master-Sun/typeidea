from django.contrib import admin


class BaseOwnerAdmin(admin.ModelAdmin):
    """
    1.自动补充文章，分类，标签等编辑页面保存时自动保存owner字段
    2.针对queryset过滤当前用户的数据
    """
    exclude = ('owner', )

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(BaseOwnerAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super(BaseOwnerAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)