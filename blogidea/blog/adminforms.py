from django import forms


# 自定义编辑页面中表单元素的样式
class PostAdminForm(forms.ModelForm):
    desc = forms.CharField(widget=forms.Textarea, label='摘要', required=False)

