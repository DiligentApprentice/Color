import datetime
from taggit.managers import TaggableManager
from markdownx.models import MarkdownxField
from slugify import slugify
from markdownx.utils import markdownify

from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class BaseManager(models.Manager):
    '''自定义模型管理器'''

    def get_all_published_articles(self):
        '''返回已经发布的文章列表'''
        return self.filter(article_type=2).all()

    def get_all_draft_articles(self):
        return self.filter(article_type=1).all()

    def get_tags_num(self):
        '''获取所有的标签并统计其数量'''
        tag_dict = {}
        for article in self.all():
            for tag in article.tags.all():
                if tag.name in tag_dict:
                    tag_dict[tag.name] += 1
                else:
                    tag_dict[tag.name] = 1
        return tag_dict


class Articles(models.Model):
    '''文章'''

    article_type_choice = ((1,'Draft'),
                    (2,'Article'))
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name='用户',
                             blank=True,
                             null=True,
                             related_name='articles')
    title = models.CharField(max_length=128,  verbose_name='文章标题')
    content = MarkdownxField(verbose_name='文章内容')
    article_type = models.IntegerField(choices=article_type_choice,default=1, verbose_name='文章类型')
    slug = models.SlugField(verbose_name='转化文章详情页URL', null=True, blank=True,max_length=80)
    # comments = models.ForeignKey(verbose_name='文章评论')
    is_edit = models.BooleanField(default=False, verbose_name='是否可以编辑')
    image = models.ImageField(upload_to='article_pics/%Y-%m-%d/', verbose_name='文章图片', blank=True, null=True)
    tags = TaggableManager(verbose_name='文章标签',related_name='tags', help_text='多个标签可以使用英文,隔开')
    objects = BaseManager()
    created_at = models.DateTimeField(default=datetime.datetime.now(), verbose_name='创建时间', db_index=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='创建时间')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '文章'
        ordering = ('-created_at',)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Articles, self).save(*args, **kwargs)

    def get_markdown(self):
        # 将Markdown文本转换成HTML
        return markdownify(self.content)









