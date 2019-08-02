from datetime import datetime
from taggit.managers import TaggableManager
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from slugify import slugify

from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

User = get_user_model()


class Vote(models.Model):
    '''投票'''

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='voters', blank=True, null=True, verbose_name='投票用户')
    value = models.BooleanField(verbose_name='投票', default=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name='关联表')
    object_id = models.IntegerField(verbose_name='关联对象id')
    vote = GenericForeignKey('content_type', 'object_id')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='创建时间')

    class Meta:
        verbose_name_plural = '投票'
        index_together = ('content_type', 'object_id')
        unique_together = ('user', 'content_type', 'object_id')



class ModelManeger(models.Manager):


    def get_has_answer_questions(self):
        '''已经有回答的问题'''
        return self.filter(answers__content__isnull=False).all()

    def get_null_answer_questions(self):
        '''未被回答的问题'''
        return self.filter(answers__content__isnull=True).all()

    def total_tag_num(self):
        tag_dict = {}
        for obj in self.all():
            for tag in obj.tags.all():
                if tag.name not in tag_dict:
                    tag_dict[tag.name] = 1
                else:
                    tag_dict[tag.name] += 1
        return tag_dict


class Question(models.Model):
    '''问题模型'''

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='提问者', related_name='questions')
    title = models.CharField(max_length=128, verbose_name='问题标题', unique=True)
    content = MarkdownxField(verbose_name='问题详情')
    tags = TaggableManager(help_text='多个标签可以用逗号隔开')
    slug = models.SlugField(max_length=128, verbose_name='获取详情页面URL')
    q_type_choice = ((1,'Open'),
                     (2,'Draft'),
                     (3,'Closed'))
    q_type = models.IntegerField(choices=q_type_choice,default=1, verbose_name='问题状态')
    is_solved = models.BooleanField(default=False, verbose_name='问题是否已经解决')
    votes = GenericRelation(Vote, verbose_name='投票情况', related_query_name='question')
    objects = ModelManeger()
    create_at = models.DateTimeField(db_index=True, auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='创建时间')

    class Meta:
        verbose_name_plural = '提问'
        ordering = ('-create_at',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Question, self).save(*args, **kwargs)

    def get_markdown(self):
        # 将Markdown文本转换成HTML
        return markdownify(self.content)

    def get_answer_num(self):
        return Answer.objects.filter(questions=self).count()

    def get_all_answers(self):
        return Answer.objects.filter(questions=self).all()

    def get_vote_number(self):
        '''获取投票数'''
        return Vote.objects.filter(question__id =self.id, value=True).count() - Vote.objects.filter(question__id =self.id, value=False).count()

    def get_upvoters(self):
        return [vote.user for vote in  Vote.objects.filter(question__id=self.id, value=True)]

    def get_downvoters(self):
        return [vote.user for vote in  Vote.objects.filter(question__id=self.id, value=False)]


class Answer(models.Model):
    '''回答模型'''

    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='answers', blank=True, null=True, verbose_name='回答者')
    content = MarkdownxField(verbose_name='问题回答')
    questions = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers', verbose_name='回答', null=True,
                               blank=True)
    is_accepted = models.BooleanField(default=False, verbose_name='被采纳')
    votes = GenericRelation(Vote,verbose_name='投票情况', related_query_name='answer')
    create_at = models.DateTimeField(db_index=True, auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='创建时间')

    class Meta:
        verbose_name_plural = '回复'
        ordering = ordering = ('-create_at',)

    def __str__(self):
        return self.content

    def get_markdown(self):
        # 将Markdown文本转换成HTML
        return markdownify(self.content)

    def get_vote_number(self):
        '''获取投票总数'''
        return Vote.objects.filter(answer__id=self.id, value=True).count() - Vote.objects.filter(answer__id=self.id,
                                                                                                   value=False).count()
    def accept_answers(self):
        Answer.objects.filter(questions=self.questions).update(is_accepted = False)
        self.is_accepted =True
        self.save()
        self.questions.is_solved = True
        self.questions.q_type = 3
        self.questions.save()

    def get_upvoters(self):
        return [vote.user for vote in  Vote.objects.filter(answer__id=self.id, value=True)]

    def get_downvoters(self):
        return [vote.user for vote in  Vote.objects.filter(answer__id=self.id, value=False)]
