import datetime

from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

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
    content = models.TextField(verbose_name='文章内容')
    article_type = models.IntegerField(choices=article_type_choice,default=1, verbose_name='文章类型')
    slug = models.SlugField(verbose_name='转化文章详情页URL', null=True, blank=True)
    comments = models.ForeignKey(verbose_name='文章评论')
    is_edit = models.BooleanField(default=False, verbose_name='是否可以编辑')
    tags = models.ManyToManyField(verbose_name='文章标签')
    created_at = models.DateTimeField(default=datetime.datetime.now(), verbose_name='创建时间', db_index=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='创建时间')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '文章'
        ordering = ('-created_at')




class ArticleImage(models.Model):
    '''文章图片'''

    aritcle = models.ForeignKey(Articles, on_delete=models.CASCADE, verbose_name='关联文章', related_name='images')
    image = models.ImageField(upload_to='article_pics/%Y-%m-%d/', verbose_name='文章图片', blank=True, null=True)

    class Meta:
        verbose_name_plural = '文章图片'

    def __str__(self):
        return self.aritcle.title




