from blogidea.custom_site import custom_site
from blog.adminforms import PostAdminForm
from blogidea.base_admin import BaseOwnerAdmin

# Register your models here.
from django.contrib.admin.models import LogEntry
from django.urls import reverse
from django.utils.html import format_html
from blog.models import *
from django.contrib import admin

from xadmin.layout import Row, Fieldset, Container

from xadmin.filters import manager
from xadmin.filters import RelatedFieldListFilter
import xadmin


# 后台站点注册日志查询
# @xadmin.site.register(LogEntry)
# class LogEntryAdmin(admin.ModelAdmin):
#     list_display = ('action_time', 'user', 'content_type', 'object_repr', 'change_message', 'object_id')


# p123:同一页面编辑关联数据
class PostInline:
    form_layout = (
        Container(
            Row('title', 'desc'),
        )
    )
    extra = 1    # 控制额外多几个
    model = Post


# 注册后台管理，指定要注册的实体类和对应的站点,后台管理的内容会通过url后指定的站点进行区分
@xadmin.sites.register(Category)
class CategoryAdmin(BaseOwnerAdmin):
    # 设置列表页显示的字段，其中post_count为自定义字段
    list_display = ('name', 'status', 'is_nav', 'owner', 'created_time', 'post_count')
    # 编辑页显示的字段
    form_layout = (
        Fieldset('分类', 'name', 'status', 'is_nav'),
    )

    # 自定义列表页显示字段：该分类下的博客数量
    def post_count(self, obj):
        # 一对多关系时，主表查询关联子表的数据,查询语法：主表对象.从表小写_set.过滤器方法
        return obj.post_set.count()
    # 列表页自定义字段名
    post_count.short_description = '文章数量'

    # inlines = [PostInline, ]


@xadmin.sites.register(Tag)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'owner', 'created_time')
    form_layout = (
        Fieldset('name', 'status'),
    )


# xadmin自定义过滤器：通过字段名的检测动态创建对应的过滤器
class CategoryOwnerFilter(RelatedFieldListFilter):
    # 设置当前过滤器需要处理的字段
    @classmethod
    def test(cls, field, request, params, model, admin_view, field_path):
        return field.name == 'category'

    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        # 该值默认是查询所有数据，此时根据owner进行过滤
        self.lookup_choices = Category.objects.filter(owner=request.user).values_list('id', 'name')


# 将过滤器注册到过滤器管理器中，并设置优先权，这样页面加载时会使用我们自定义的过滤器
manager.register(CategoryOwnerFilter, take_priority=True)


# 装饰器参数：注册的实体类以及所属的站点
@xadmin.sites.register(Post)
class PostAdmin(BaseOwnerAdmin):
    # 修改编辑页面中form表单元素的样式
    form = PostAdminForm
    # operator 为自定义的显示字段
    list_display = ('title', 'status', 'category', 'owner', 'created_time', 'operator')
    # 定义可点击进入编辑页面的字段，不写的话默认为第一个
    list_display_links = []
    # xadmin自定义过滤器，此处使用字段名
    list_filter = ['category']
    # 定义搜索字段，此处category为外键，双下划线指定关联Category类中的name字段
    search_fields = ['title', 'category__name']

    # 动作相关的配置，是否展示在顶部和底部
    actions_on_top = True
    actions_on_bottom = True

    # 开启顶部的编辑按钮
    save_on_top = True

    # 指定不显示的字段，字段名不能同时出现在exclude和fields中
    # 感觉只写fields不就行了
    # exclude = ('owner', 'created_time')
    # 编辑页显示的字段，与fieldsets不可共存
    # fields = (
    #     ('category', 'title'),
    #     'desc',
    #     'status',
    #     'content',
    #     'tag',
    # )
    # fieldsets = (
    #     ('基础配置', {
    #         'description': '基础配置',    # 标题下的描述
    #         'fields': (
    #             ('title', 'category'),
    #             'status',
    #         )
    #     }),
    #     ('内容', {
    #         'fields': (
    #             'desc',
    #             'content',
    #         )
    #     }),
    #     ('额外信息', {
    #         'classes': ('collapse',),    # 控制显示和隐藏
    #         'fields': ('tag',)
    #     })
    # )

    # xadmin关于编辑页的布局设置
    form_layout = (
        Fieldset(
            '基础信息',
            Row('title', 'category'),
            'status',
            'tag',
        ),
        Fieldset(
            '内容信息',
            'desc',
            'is_md',
            'content_ck',
            'content_md',
            'content',
        ),
    )

    # 设置字段横向或纵向展示
    filter_horizontal = ('tag',)

    # 定义 自定义显示字段的方法,返回值显示在列表页中
    def operator(self, obj):
        # return format_html(
        #     '<a href="{}">编辑</a>', reverse('xadmin:blog_post_change', args=(obj.id,))
        # )
        return format_html(
            '<a href="{}">编辑</a>', self.model_admin_url('change', obj.id)
        )
    # 显示自定义显示字段的名称
    operator.short_description = '操作'

    # 自定义了继承自admin.ModelAdmin的基类，并重写了save_model和get_queryset方法，所以此处省略
    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user
    #     return super(PostAdmin, self).save_model(request, obj, form, change)
    #
    # # 自定义列表页中只显示当前登陆用户自己的博客
    # def get_queryset(self, request):
    #     # 先调用父类中的方法得到查询结果集，然后再进行过滤
    #     qs = super(PostAdmin, self).get_queryset(request)
    #     return qs.filter(owner=request.user)

    # 向页面中添加css和js，如果是项目本身的静态资源，直接写名称即可
    # class Media:
    #     css = {
    #         'all': ('http://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css',),
    #     }
        # js = ('https://cdn.jsdelivr.net/gh/bootcdn/BootCDN/ajax/libs/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js',)

    # xadmin关于静态资源Media的配置，此写法可兼容admin
    # @property
    # def media(self):
    #     # xadmin是基于bootstrap的，引入会导致页面样式冲突，此处仅做演示
    #     media = super().media
    #     media.add_js(['https://cdn.jsdelivr.net/gh/bootcdn/BootCDN/ajax/libs/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js'])
    #     media.add_css({
    #         'all': ('http://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css',),
    #     })
    #     return media
