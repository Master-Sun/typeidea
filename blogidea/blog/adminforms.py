from django import forms
from dal import autocomplete

from .models import Tag, Category, Post

from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget


# 自定义编辑页面中表单元素的样式，调用自动补全接口
class PostAdminForm(forms.ModelForm):
    desc = forms.CharField(widget=forms.Textarea, label='摘要', required=False)
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        # 调用自动补全的接口，参数url对应的是url中的name
        widget=autocomplete.ModelSelect2(url='category-autocomplete'),
        label='分类',
    )
    # tag为多对对字段，组件名跟category有差异
    tag = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        # 这边也不一样
        widget=autocomplete.ModelSelect2Multiple(url='tag-autocomplete'),
        label='标签',
    )
    # content = forms.CharField(widget=CKEditorWidget(), label='正文', required=True)
    # 这个插件是带图片上传功能的，上面的只能处理文字，上传的同名图片，ckeditor会自动追加随机码区分
    # 这边的required都要写成false，因为用户最终提交的时候，总有两个输入框是空的
    # 原生的content字段设置隐藏
    content = forms.CharField(widget=forms.HiddenInput(), label='正文', required=False)
    # 增加额外的forms组件,通过js隐藏默认的content组件(但会接收最终的内容)
    # 以下两个组件根据is_md的值选择一个进行展示
    content_ck = forms.CharField(widget=CKEditorUploadingWidget(), label='正文', required=False)
    content_md = forms.CharField(widget=forms.Textarea(), label='正文', required=False)


    # 可以不配置Meta，此处是为避免出现js资源冲突问题
    class Meta:
        model = Post
        # 需要自动补全的字段要放到前面
        fields = ('category', 'tag', 'title', 'desc', 'is_md',
                  'content', 'content_ck', 'content_md', 'status')

    def __init__(self, instance=None, initial=None, **kwargs):
        # initial为form对象中各字段初始化的值，首次编写则为各字段初始化的值
        # 再次编辑时即为当前文章的实例
        initial = initial or {}
        if instance:
            # 基于instance对象，对新增的两个form层字段进行处理
            if instance.is_md:
                initial['content_md'] = instance.content
            else:
                initial['content_ck'] = instance.content
        super().__init__(instance=instance, initial=initial, **kwargs)

    # 在clean方法中对用户提交的内容进行处理
    def clean(self):
        is_md = self.cleaned_data.get('is_md')
        # 根据is_md的值，判断用户是在哪个编辑器中输入的，然后取对应的内容
        if is_md:
            content_field_name = 'content_md'
        else:
            content_field_name = 'content_ck'
        # 此处content为取到的markdown或ckeditor中的内容
        content = self.cleaned_data.get(content_field_name)
        # 在此处进行空值控制，若为空则返回异常
        if not content:
            self.add_error(content_field_name, '必须填')
            return
        # 将取到的内容赋值给原生的content字段
        self.cleaned_data['content'] = content
        return super().clean()

    class Media:
        js = ('js/post_editor.js',)
