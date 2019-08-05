from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Min, Count

User = get_user_model()


class ModelManager(models.Manager):

    def get_all_messages(self, sender, recipient):
        sender_mes = self.filter(sender=sender,recipient=recipient).all()
        recipient_mes = self.filter(sender=recipient, recipient=sender).all()
        messages = recipient_mes.union(sender_mes).order_by('created_at')
        return messages

    def get_latest_message_user(self, user):
        '''返回最近一次的用户'''
        try:
            sender_mes = self.filter(sender=user).all() #当前登录用户发送过的所有消息
            recipient_mes = self.filter(recipient = user).all()#当前登录用户接收到的所有消息
            latest_mes = sender_mes.union(recipient_mes).latest('created_at') #返回最近的一条消息
            if latest_mes.sender == user:
                return latest_mes.recipient
            return latest_mes.sender
        except self.model.DoesNotExist:  #如果没有消息话，在union做并集时会报错
            return user

    def get_conversation_userlist(self, user):
        '''获取当前用户所有发送过私信用户的列表'''
        recipient_list = self.filter(sender=user).values('recipient').annotate(time=Min('created_at')).values('recipient', 'time')
        sender_lsit = self.filter(recipient=user).values('sender').annotate(time=Min('created_at'))
        return sender_lsit


class Message(models.Model):
    '''消息模型'''
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='发送者', related_name='m_sender', null=True)
    recipient = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='接受者', related_name='m_recipient', null=True)
    message = models.TextField(verbose_name='消息')
    unread = models.BooleanField(default=True, verbose_name='消息是未读')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='发送时间', db_index=True)
    objects = ModelManager()
    class Meta:
        verbose_name_plural = '消息'
        ordering = ('created_at',)

    def __str__(self):
        return self.message

    def set_read(self):
        '''标记为已读'''
        if self.unread:
            self.unread = False
        self.save()


