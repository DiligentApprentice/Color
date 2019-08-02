from django.forms import ModelForm
from django import forms

from qa.models import Question, Answer
class QuestionForm(ModelForm):

    q_type = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = Question
        fields = ['title', 'content','q_type' , 'tags', ]


class AnswerForm(ModelForm):

    class Meta:
        model = Answer
        fields = ['content']
