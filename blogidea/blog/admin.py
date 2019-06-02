from django.contrib import admin
from blog.models import *


# Register your models here.
from django.urls import reverse
from django.utils.html import format_html


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'is_nav', 'owner', 'created_time')
    fields = ('name', 'status', 'is_nav')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(CategoryAdmin, self).save_model(request, obj, form, change)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'owner', 'created_time')
    fields = ('name', 'status')

    # 该方法是将编辑页中得数据保存到数据库中，此处添加owner字段的数据
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(TagAdmin, self).save_model(request, obj, form, change)


# 自定义过滤器
class CategoryOwnerFilter(admin.SimpleListFilter):
    """自定义过滤器：只显示当前用户的分类(category)"""
    title = '分类过滤器'    # 过滤器名称，页面显示：以 分类过滤器
    parameter_name = 'owner_category'    # 过滤查询时URL的参数名

    # 返回要展示的内容(分类名)和查询用的id，此方法关乎过滤器的显示
    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    # 根据选择的过滤参数过滤列表页的显示结果，此方法关乎列表页的显示
    def queryset(self, request, queryset):
        category_id = self.value()    # 获取过滤参数，category的id
        if category_id:
            return queryset.filter(category_id=category_id)
        return queryset


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # operator 为自定义的显示字段
    list_display = ('title', 'status', 'category', 'owner', 'created_time', 'operator')
    # 定义可点击进入编辑页面的字段，不写的话默认为第一个
    list_display_links = []
    # 定义右侧过滤器的参考字段
    list_filter = [CategoryOwnerFilter]
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
    fields = (
        ('category', 'title'),
        'desc',
        'status',
        'content',
        'tag',
    )

    # 定义 自定义显示字段的方法,返回值显示在列表页中>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>', reverse('admin:blog_post_change', args=(obj.id,))
        )
    # 显示自定义显示字段的名称
    operator.short_description = '操作'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(PostAdmin, self).save_model(request, obj, form, change)

    # 自定义列表页中只显示当前登陆用户自己的博客
    def get_queryset(self, request):
        # 先调用父类中的方法得到查询结果集，然后再进行过滤
        qs = super(PostAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)
