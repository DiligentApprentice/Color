from django.db import models
from django.contrib.auth import get_user_model
from channels.layers import get_channel_layer
from asgiref.sync import  async_to_sync
from color.notification.views import notification_handler

import datetime

User = get_user_model()
# Create your models here.
class News(models.Model):
    '''首页动态'''

    user = models.ForeignKey(User, verbose_name='用户',related_name='news', on_delete=models.CASCADE,blank=True, null=True)
    content = models.TextField(verbose_name='动态内容', null=True, blank=True)
    liker = models.ManyToManyField(User, verbose_name='点赞用户', related_name='likers',blank=True )
    parent = models.ForeignKey('self', verbose_name='关联动态',on_delete=models.CASCADE, related_name='comment',blank=True,null=True)
    reply = models.BooleanField(verbose_name='是否为评论', default=False)
    created_at = models.DateTimeField(default=datetime.datetime.now(), verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    class Meta:
        ordering = ('-created_at',)
        verbose_name_plural = '首页动态'

    def __str__(self):
        return self.content

    def like_or_cancle(self, user):
        '''用户取消或者点赞'''
        if user in self.liker.all():
            self.liker.remove(user)
        else:
            self.liker.add(user)
            notification_handler(trigger=user, recipient=self.user, action_obj=self, action='L',
                                 id=self.id, key="news_update")

    def total_like_num(self):
        '''动态点赞数统计'''
        return self.liker.all().count()

    def total_comment_num(self):
        '''动态评论数统计'''
        return self.get_all_relation_comments().count()

    def get_likers(self):
        '''获取所有点赞对象'''
        return self.liker.all()

    def get_all_relation_comments(self):
        '''动态所有评论对象'''
        return self.comment.filter(reply=True).select_related('user').all()

    def save(self, *args, **kwargs):
        '''默认在创建new时，将消息发送通知'''
        super(News, self).save(*args, **kwargs)
        if not self.reply:
            channel_layer = get_channel_layer()
            payload ={
                "type":'receive',
                "key":"add_news",
                "trigger":self.user.username
            }
            async_to_sync(channel_layer.group_send)('notification', payload)




