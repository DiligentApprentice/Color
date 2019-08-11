from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core import serializers

User = get_user_model()


class BaseModelManager(models.Manager):
    '''模型管理器'''

    def get_notification_list(self, user):
        '''获取所有未读通知'''
        return self.filter(recipient=user,unread=True).all()

    def mark_all_notification_read(self, user):
        '''全部标记为已读'''
        query = self.get_notification_list(user)
        query.update(unread=False)

    def get_recent_notification(self, user):
        '''获取最近的5条未读信息'''
        return self.get_notification_list(user)[:5]

    def get_recent_notification_serializers(self, user):
        '''获取序列化的5条数据'''
        return  serializers.serialize("json", self.get_recent_notification(user))


class Notification(models.Model):
    '''消息通知模型'''
    trigger = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                verbose_name='消息触发者',
                                related_name='trigger',
                                null=True,
                                blank=True)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='n_recipient',
                                  verbose_name='消息接收者', blank=True, null=True)
    action_type = (('L',"点赞了"),
                   ('R', "回复了"),
                   ("C", "评论了"),
                   ("A", "回答了"),
                   ("T", "接受了回答"))
    action = models.CharField(max_length=1, choices=action_type, verbose_name='动作')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE , null=True, blank=True)
    object_id = models.IntegerField(verbose_name='model数据id', null=True)
    action_obj = GenericForeignKey("content_type", "object_id")
    unread = models.BooleanField(default=True, verbose_name='通知是否未读')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_at = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    objects = BaseModelManager()

    class Meta:
        verbose_name_plural = '通知'
        ordering = ('-created_at',)

    def __str__(self):
        if self.action_obj:
            return f'{self.trigger}{self.get_action_display()}{self.action_obj}'
        return f'{self.trigger}{self.get_action_display()}'

    def mark_as_read(self):
        if self.unread:
            self.unread = False
        self.save()


