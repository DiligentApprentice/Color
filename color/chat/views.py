import json
from django.shortcuts import render, HttpResponse
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from common import ajax_required
from channels.layers import get_channel_layer
from django.template.loader import render_to_string
from asgiref.sync import async_to_sync

from chat.models import Message

User = get_user_model()

class MessageListView(LoginRequiredMixin, ListView):

    model = Message
    template_name = 'messager/message_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(MessageListView, self).get_context_data(*args, **kwargs)
        user_list = User.objects.exclude(username=self.request.user.username).order_by('-last_login')[:10]
        context["users_list"] = user_list
        latest_user = Message.objects.get_latest_message_user(self.request.user)
        context["active"] = latest_user.username
        return context


class SingleMessageListView(MessageListView):
    '''和指定用户的私信'''
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs['username'])
        return Message.objects.get_all_messages(self.request.user, user)

    def get_context_data(self, *args, **kwargs):
        context = super(SingleMessageListView, self).get_context_data(*args, **kwargs)
        context['active'] = self.kwargs['username']
        return context


@login_required
@ajax_required
@require_http_methods(['POST'])
def post_messages(request, *args, **kwargs):
    username = request.POST.get('to')
    message = request.POST.get('message')
    recipient = User.objects.get(username=username)

    if len(message.strip())>0 and recipient != request.user:
        obj = Message.objects.create(sender=request.user, recipient=recipient, message=message)
        channel_layer = get_channel_layer()
        payload = {"type":"receive",
                   "message":render_to_string('messager/single_message.html', {"message":obj}),
                   "sender":request.user.username}
        async_to_sync(channel_layer.group_send)(recipient.username, payload)
        return render(request, 'messager/single_message.html', {"message":obj})
    return HttpResponse()


