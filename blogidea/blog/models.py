import mistune
from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Category(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )

    name = models.CharField(max_length=50, verbose_name="名称")
    # 正整数或0
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="状态")
    is_nav = models.BooleanField(default=False, verbose_name="是否为导航")
    owner = models.ForeignKey(User, verbose_name="作者")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = verbose_name_plural = '分类'

    def __str__(self):
        return self.name

    @classmethod
    def get_navs(cls):
        nav_categories = []
        normal_categories = []
        categories = Category.objects.filter(status=Category.STATUS_NORMAL)
        # 查询一次即可拿到所有分类
        for cate in categories:
            if cate.is_nav:
                nav_categories.append(cate)
            else:
                normal_categories.append(cate)
        return {
            'nav_categories': nav_categories,
            'normal_categories': normal_categories,
        }


class Tag(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )

    name = models.CharField(max_length=10, verbose_name="名称")
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="状态")
    owner = models.ForeignKey(User, verbose_name="作者")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = verbose_name_plural = '标签'

    def __str__(self):
        return self.name


class Post(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
        (STATUS_DRAFT, '草稿'),
    )

    title = models.CharField(max_length=255, verbose_name="标题")
    desc = models.CharField(max_length=1024, blank=True, verbose_name="摘要")
    # help_text:后台管理中编辑页上的提示内容
    content = models.TextField(verbose_name="正文", help_text="正文必须为MarkDown格式")
    content_html = models.TextField(verbose_name='正文html代码', blank=True, editable=False)
    # 字段类型：正整数或0；choices：显示为一个下拉选择框
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="状态")
    category = models.ForeignKey(Category, verbose_name="分类")
    tag = models.ManyToManyField(Tag, verbose_name="标签")
    owner = models.ForeignKey(User, verbose_name="作者")
    # 设置自动写入时间
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    pv = models.PositiveIntegerField(default=1)
    uv = models.PositiveIntegerField(default=1)
    # 新增字段，用来标注使用markdown还是富文本编辑器
    is_md = models.BooleanField(default=False, verbose_name='markdown语法')

    # 重写save方法，根据is_md的值切换存储格式
    def save(self, *args, **kwargs):
        if self.is_md:
            self.content_html = mistune.markdown(self.content)
        else:
            # 如果是非markdown语法的，则直接保存content即可(ckeditor已做好转换)
            self.content_html = self.content
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = verbose_name_plural = '文章'
        # 根据id进行降序排列，通过模型查询时先显示最新的数据
        ordering = ['-id']

    # 在模型中定义数据查询的方法，项目初期尽量简化View层的逻辑
    # 避免后期维护麻烦，因为后续业务需求的调整大多发生在View层
    @classmethod
    def hot_posts(cls):
        return cls.objects.filter(status=cls.STATUS_NORMAL).order_by('-pv')

    # with_related：不用显示外键数据时传入False
    @classmethod
    def latest_posts(cls, with_related=True):
        queryset =  cls.objects.filter(status=Post.STATUS_NORMAL)
        # 解决外键引起的N+1问题，查询时一并查出外键对应的数据
        if with_related:
            queryset.select_related("owner", 'category')
        return queryset

    @staticmethod
    def get_by_tag(tag_id):
        try:
            # get得到的Tag的实例对象，而filter得到的是查询结果集queryset(懒加载)
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            tag = None
            post_list = []
        else:
            # 外键关联时(一对多或多对多)，主表查从表，此方法必须由主表的实例调用，因此上方要用get方法
            # select_related()解决N+1问题，查询时会一并查出post中外键关联的owner和category字段，适用一对多
            # 多对多为prefetch_related()
            post_list = tag.post_set.filter(status=Post.STATUS_NORMAL).select_related('owner', 'category')
        return post_list, tag

    @staticmethod
    def get_by_category(category_id):
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            post_list = []
            category = None
        else:
            post_list = category.post_set.filter(status=Post.STATUS_NORMAL)
        return post_list, category

