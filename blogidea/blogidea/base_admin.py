from django.contrib import admin


class BaseOwnerAdmin(object):
    """
    1.自动补充文章，分类，标签等编辑页面保存时自动保存owner字段
    2.针对queryset过滤当前用户的数据
    """
    exclude = ('owner', )    # 设置编辑页中不显示owner字段

    # 保存数据到数据库中时自动给owner字段赋值
    def save_models(self):
        self.new_obj.owner = self.request.user
        return super().save_models()

    # 设置列表页仅显示当前登陆用户的信息
    def get_list_queryset(self):
        request = self.request
        qs = super().get_list_queryset()
        return qs.filter(owner=request.user)