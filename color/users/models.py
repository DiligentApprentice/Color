from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.db import models

class User(AbstractUser):
    '''自定义用户'''

    nick_name = models.CharField(verbose_name='', blank=True, max_length=255)
    picture = models.ImageField(upload_to='', verbose_name='头像')
    title = models.CharField(max_length=32, verbose_name='头衔', null=True, blank=True)
    brief = models.TextField(verbose_name='用户简介',null=True, blank=True)
    city = models.CharField(max_length=32, verbose_name='所在城市',null=True, blank=True)
    link = models.URLField(max_length=500, verbose_name='个人链接', null=True, blank=True)
    wb_link = models.URLField(max_length=500, verbose_name='微博链接', null=True, blank=True)
    zh_link = models.URLField(max_length=500, verbose_name='知乎链接', null=True, blank=True)
    github_link = models.URLField(max_length=500, verbose_name='github链接', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True,verbose_name='修改时间')

    class Meta:
        verbose_name_plural = '用户表'

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    def get_nick_name(self):
        '''获取昵称'''
        if self.nick_name:
            return self.nick_name
        return self.username
