from django.db import models
from django.contrib.auth import get_user_model

import datetime

User = get_user_model()
# Create your models here.
class News(models.Model):
    '''首页动态'''

    user = models.ForeignKey(User, verbose_name='用户',related_name='news', on_delete=models.CASCADE,blank=True, null=True)
    content = models.TextField(verbose_name='动态内容', null=True, blank=True)
    liker = models.ManyToManyField(User, verbose_name='点赞用户',on_delete=models.CASCADE,related_name='liker',blank=True, null=True )
    parent = models.ForeignKey('self', verbose_name='关联动态',on_delete=models.CASCADE, related_name='comment',blank=True,null=True)
    reply = models.BooleanField(verbose_name='是否为评论', default=False)
    created_at = models.DateTimeField(default=datetime.datetime.now(), verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    class Meta:
        ordering = ('-created_at',)
        verbose_name_plural = '首页动态'

    def __str__(self):
        return self.content

    def publish(self, user, content):
        '''用户发表动态'''
        self.user = user
        self.content = content
        self.save()

    def like(self,liker):
        '''用户点赞'''
        pass

    def cancel_like(self):
        '''用户取消赞'''
        pass

    def comment(self, content, user):
        '''用户评论'''
        self.parent =self
        self.content = content
        self.reply = True
        self.user = user
        self.save()



