import mistune
from comment.models import Comment
from django import forms


# 如果不考虑样式，仅需定义model和fields即可
class CommentForm(forms.ModelForm):
    # nickname = forms.CharField(
    #     label='昵称',
    #     max_length=50,
    #     # 可以在定义form表单时设置限制和样式
    #     widget=forms.widgets.Input(
    #         attrs={'class': 'form-control', 'style': 'width: 60%'}
    #     )
    # )
    # email = forms.CharField(
    #     label='Email',
    #     max_length=50,
    #     widget=forms.widgets.EmailInput(
    #         attrs={'class': 'form-control', 'style': 'width: 60%'}
    #     )
    # )
    # website = forms.CharField(
    #     label='网站',
    #     max_length=100,
    #     widget=forms.widgets.URLInput(
    #         attrs={'class': 'form-control', 'style': 'width: 60%'}
    #     )
    # )
    content = forms.CharField(
        label='内容',
        max_length=500,
        widget=forms.widgets.Textarea(
            attrs={'rows': 6, 'cols': 60, 'class': 'form-control'}
        )
    )

    # 定义需要进行数据清洗的字段和规则
    def clean_content(self):
        content = self.cleaned_data.get('content')  #　获取字段内容
        if len(content) < 10:
            raise forms.ValidationError('评论不可少于10个字')
        content = mistune.markdown(content)
        return content

    class Meta:
        model = Comment
        fields = ['content',]