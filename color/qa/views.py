from django.shortcuts import render
from django.views.generic import CreateView, ListView , DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied

from color.qa.models import Question, Answer, Vote
from color.qa.myform import QuestionForm, AnswerForm
from color.common import ajax_required
from color.notification.views import notification_handler

class QAListView(LoginRequiredMixin, ListView):
    '''问答列表视图'''

    model = Question
    template_name = 'qa/question_list.html'
    context_object_name = 'questions'
    paginate_by = 20

    def get_context_data(self, *args, **kwargs):
        context = super(QAListView, self).get_context_data(*args, **kwargs)
        context["tags"] = Question.objects.total_tag_num()
        context["active"] = "all"
        return context


class QAUnQusestionListView(QAListView):
    '''没有回答的问题列表'''

    def get_context_data(self, *args, **kwargs):
        context = super(QAUnQusestionListView, self).get_context_data(*args, **kwargs)
        context["active"] = "unanswered"
        return context

    def get_queryset(self):
        return Question.objects.get_null_answer_questions()



class QAHaveQusestionListView(QAListView):
    '''已经有回答的问题列表'''

    def get_context_data(self, *args, **kwargs):
        context = super(QAHaveQusestionListView, self).get_context_data(*args, **kwargs)
        context["active"] = "answered"
        return context

    def get_queryset(self):
        return Question.objects.get_has_answer_questions()


class QACreateView(LoginRequiredMixin, CreateView):
    '''创建问题'''
    model = Question
    template_name = 'qa/question_form.html'
    form_class = QuestionForm
    message = '问题已经创建成功'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super(QACreateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse('qa:unanswered_q')

    def form_invalid(self, form):
        print(form.errors)
        return super(QACreateView, self).form_invalid(form)

class QADetailView(LoginRequiredMixin, DetailView):
    '''问题详情'''

    model = Question
    template_name = 'qa/question_detail.html'

    def get_object(self, queryset=None):
        return Question.objects.get(slug=self.kwargs[self.slug_url_kwarg])


class AnswerCreateView(LoginRequiredMixin, CreateView):
    '''回答视图'''
    model = Answer
    template_name = 'qa/answer_form.html'
    form_class = AnswerForm
    message = '回答创建成功'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.questions_id = self.kwargs.get('question_id')
        form.save()
        self.slug = Question.objects.get(id =self.kwargs.get('question_id') ).slug
        return super(AnswerCreateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse('qa:question_detail',kwargs={"slug":self.slug})


@login_required
@ajax_required
@require_http_methods('["POST"]')
def post_question_vote(request):
    '''1、先点赞然后取消
       2、先反对然后取消
       3、先点赞然后在点反对
       4、先点反对然后在点赞
    '''
    q_id = request.POST.get('question')
    q_obj = Question.objects.get(id=q_id)
    value = request.POST.get('value')
    if value =='U':
        if request.user in q_obj.get_upvoters():
            Vote.objects.filter(user=request.user).delete()
        elif request.user in q_obj.get_downvoters():
            Vote.objects.filter(user=request.user).update(value=True)
        else:
            Vote.objects.create(user=request.user, vote=q_obj)
        return JsonResponse({"votes":q_obj.get_vote_number() })
    if value == 'D':
        if request.user in q_obj.get_downvoters():
            Vote.objects.filter(user=request.user).delete()
        elif request.user in q_obj.get_upvoters():
            Vote.objects.filter(user=request.user).update(value=False)
        else:
            Vote.objects.create(user=request.user, vote=q_obj, value=False)
        return JsonResponse({"votes": q_obj.get_vote_number()})


@login_required
@ajax_required
@require_http_methods('["POST"]')
def post_answer_vote(request):
    a_id = request.POST.get('answer')
    a_obj = Answer.objects.get(id=a_id)
    value = request.POST.get('value')
    if value == 'U':
        if request.user in a_obj.get_upvoters():
            Vote.objects.filter(user=request.user).delete()
        elif request.user in a_obj.get_downvoters():
            Vote.objects.filter(user=request.user).update(value=True)
        else:
            Vote.objects.create(user=request.user, vote=a_obj)
        return JsonResponse({"votes": a_obj.get_vote_number()})
    if value == 'D':
        if request.user in a_obj.get_downvoters():
            Vote.objects.filter(user=request.user).delete()
        elif request.user in a_obj.get_upvoters():
            Vote.objects.filter(user=request.user).update(value=False)
        else:
            Vote.objects.create(user=request.user, vote=a_obj, value=False)
        return JsonResponse({"votes": a_obj.get_vote_number()})


@login_required
@ajax_required
@require_http_methods('["POST"]')
def post_accept_answer(request):
    '''回答被采纳'''
    a_id = request.POST.get('answer')
    a_obj = Answer.objects.get(id= a_id)
    if request.user.username != a_obj.questions.user.username:
        raise PermissionDenied
    a_obj.accept_answers()
    notification_handler(trigger=request.user, recipient=a_obj.user, action='T', action_obj=a_obj)
    return JsonResponse({"status":'success'},status=200)











