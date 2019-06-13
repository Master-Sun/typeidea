from django import forms


# 自定义编辑页面中表单元素的样式，将输入框设置显示为多行文本域
class PostAdminForm(forms.ModelForm):
    desc = forms.CharField(widget=forms.Textarea, label='摘要', required=False)

