from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from django.db import models
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect,reverse, render, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from color.notification.models import Notification

class NotificationList(LoginRequiredMixin, ListView):
    '''未读消息通知列表'''
    model = Notification
    template_name = 'notifications/notification_list.html'

    def get_queryset(self):
        return Notification.objects.get_notification_list(user=self.request.user)


@login_required
def mark_all_notification_read(request, *args, **kwargs):
    '''标记所有的通知已读'''
    Notification.objects.mark_all_notification_read(user=request.user)
    messages.success(request, '全部消息已标记为已读')
    return redirect(reverse('notification:list'))


@login_required()
def get_recent_notification(request,*args, **kwargs):
    '''获取最近的消息通知'''
    notifications = Notification.objects.get_recent_notification(request.user)
    if notifications:
        return render(request, 'notifications/most_recent.html', {"notifications":notifications})
    return HttpResponse('没有未读通知')


@login_required
def make_single_read(request, *args, **kwargs):
    '''单个标记为已读'''
    id = kwargs.get('id')
    try:
        object = Notification.objects.get(id=id)
        object.mark_as_read()
        messages.success(request, '已经标记为已读')
        return redirect(reverse('notification:list'))
    except models.ObjectDoesNotExist as e:
        return HttpResponse(e)


def notification_handler(trigger, recipient, action, action_obj, **kwargs):
    '''消息处理器
    '''
    key = kwargs.get('key', 'notification') #对不同的操作，前端的处理方式不同，通过key进行判断
    id = kwargs.get('id') #获取被操作对象id，方便通过前端传入到后端进行逻辑处理

    if recipient.username == action_obj.user.username and trigger.username != recipient.username:
        Notification.objects.create(trigger=trigger,
                                    recipient=recipient,
                                    action=action,
                                    action_obj=action_obj)

        channel_layer = get_channel_layer()
        payload = {
            "type":"receive",
            "trigger":trigger.username,
            "key":key,
            "id":id
        }
        async_to_sync(channel_layer.group_send)('notification',payload )



