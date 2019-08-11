from django.shortcuts import render
from django.views.generic import ListView, DeleteView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse
from django_comments.signals import comment_was_posted
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from color.notification.views import notification_handler
from color.articles.models import Articles
from color.articles.myform import ArticleForm
# Create your views here.

class ArticleListView(LoginRequiredMixin,ListView ):
    '''文章列表'''
    model = Articles
    template_name = 'articles/article_list.html'
    paginate_by = 10
    context_object_name = 'articles'

    def get_queryset(self):
        
        return Articles.objects.get_all_published_articles()

    def get_context_data(self,*args, **kwargs):
        context = super(ArticleListView, self).get_context_data( *args, **kwargs)
        context["tags"] = Articles.objects.get_tags_num()
        print(Articles.objects.get_tags_num(), '结果')
        return context


class ArticleCreateView(LoginRequiredMixin, CreateView):
    '''创建文章'''

    model = Articles
    form_class = ArticleForm
    template_name = 'articles/article_create.html'
    message = '文章已经创建'


    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.article_type = 2
        form.instance.is_edit = True
        return super(ArticleCreateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request,self.message )
        return reverse('articles:list')

    def form_invalid(self, form):
        print(form.errors)
        return super(ArticleCreateView, self).form_invalid(form)



class ArticleDetailView(LoginRequiredMixin, DetailView):
    '''文章详情页面'''

    model = Articles
    template_name = 'articles/article_detail.html'

    def  get_queryset(self):

        return Articles.objects.filter(slug=self.kwargs[self.slug_url_kwarg])


class DraftListView(ArticleListView):
    '''草稿箱'''

    def get_queryset(self):
        return Articles.objects.get_all_draft_articles().filter(user=self.request.user)




class DraftCreateView(LoginRequiredMixin, CreateView):
    '''创建草稿'''

    model = Articles
    form_class = ArticleForm
    template_name = 'articles/article_create.html'
    message = '已经成功创建文章草稿'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.article_type = 1
        form.instance.is_edit = True
        form.save()
        return super(DraftCreateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request,self.message )
        return reverse('articles:drafts')

class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    '''文章或者草稿修改编辑'''

    model = Articles
    form_class = ArticleForm
    template_name = 'articles/article_update.html'
    message = '文章更新成功'

    def get_object(self, queryset=None):
        return Articles.objects.get(id = self.kwargs['pk'])

    def get_success_url(self):
        messages.success(self.request,self.message)
        return reverse('articles:list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.article_type = 2
        form.instance.is_edit = True
        return super(ArticleUpdateView, self).form_valid(form)


def notify_comment(**kwargs):
    user = kwargs['request'].user
    action_obj = kwargs['comment'].content_object
    recipient = action_obj.user
    notification_handler(trigger=user, recipient=recipient, action='C', action_obj=action_obj)


comment_was_posted.connect(receiver=notify_comment)
