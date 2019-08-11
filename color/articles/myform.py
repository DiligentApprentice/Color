from django.forms import Form ,ModelForm
from django import forms
from django.forms.widgets import HiddenInput

from markdownx.fields import MarkdownxFormField

from color.articles.models import Articles

class ArticleForm(ModelForm):
    '''文章Form'''

    content = MarkdownxFormField()
    # article_type = forms.IntegerField(widget=HiddenInput() )
    # is_edit = forms.BooleanField(widget=HiddenInput())


    class Meta:
        model = Articles
        fields = ['title', 'content', 'image', 'tags', ]



