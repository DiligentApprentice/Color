from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect, HttpResponse
from django.http import HttpResponseBadRequest, JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse,reverse_lazy

from news.models import News
from common import ajax_required

class NewsListView(LoginRequiredMixin,ListView ):
    '''动态列表'''

    model = News
    paginate_by = 20
    template_name = 'news/news_list.html'

    def get_queryset(self):
        return News.objects.filter(reply=False).all()

@login_required
@ajax_required
@require_http_methods(["POST"])
def post_news(request):
    '''创建动态'''
    content = request.POST.get('post').strip()
    if content:
        obj = News.objects.create(
            user=request.user,
            content=content
        )
        template =render_to_string('news/news_single.html', {"news":obj,"request":request})
        return HttpResponse(template)
    return HttpResponseBadRequest('发送内容不能为空')


@login_required
@ajax_required
@require_http_methods(["POST"])
def post_like_or_cancle(request):
    '''点赞或者取消赞'''
    id = request.POST.get('news').strip()
    instance = News.objects.filter(id=id).first()
    instance.like_or_cancle(request.user)
    return JsonResponse({"likes":instance.total_like_num()})


@login_required
@ajax_required
@require_http_methods(["POST"])
def post_comment(request):
    '''用户评论'''
    reply = request.POST.get("reply")
    id = request.POST.get("parent")
    parent = News.objects.get(id=id)
    if reply:
        instance = News.objects.create(parent=parent,user=request.user, content=reply, reply=True)
        return JsonResponse({"comments":parent.total_comment_num()})
    else:
        return HttpResponseBadRequest('回复内容不允许为空')

@login_required
@ajax_required
@require_http_methods(["GET"])
def get_relation_comments(request):
    id = request.GET.get("news")
    print(id,type(id))
    instance = News.objects.get(id=id)
    news = render_to_string('news/news_single.html',{"news":instance})
    comments = render_to_string('news/news_thread.html',{"thread":instance.get_all_relation_comments()})
    return JsonResponse({"id":instance.id ,"news":news,"thread":comments})


class NewsDeleteVieww(LoginRequiredMixin,DeleteView ):
    '''删除动态'''
    model = News
    success_url = reverse_lazy('news:list')
    template_name = 'news/news_confirm_delete.html'






