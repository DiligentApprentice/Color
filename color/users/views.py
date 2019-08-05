from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, RedirectView, UpdateView
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _


User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    template_name = 'users/user_detail.html'
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        user = User.objects.get(username=self.request.user.username)
        context["news_num"] = user.news.filter(reply=False).all().count()
        context["article_num"] = user.articles.filter(article_type=2).all().count()
        context["comment_num"] = user.comment_comments.all().count()
        context["question_num"] = user.questions.all().count()
        context["answer_num"] = user.answers.all().count()
        #互动数
        message_user_set = set()
        recipient_list = user.m_sender.all()
        for recipient in recipient_list:
            message_user_set.add(recipient.recipient)
        sneder_list = user.m_recipient.all()
        for sender in recipient_list:
            message_user_set.add(sender.sender)

        context["interaction_num"] =user.likers.all().count()+user.voters.all().count()+ \
                                    user.comment_comments.all().count()+len(message_user_set)
        return context





class UserUpdateView(LoginRequiredMixin, UpdateView):

    model = User
    fields = ["nick_name", "picture", "title", "brief", "city", "link", "wb_link", "zh_link", "github_link"]
    template_name = 'users/user_form.html'

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self):
        return User.objects.get(username=self.request.user.username)

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.INFO, _("Infos successfully updated")
        )
        return super(UserUpdateView, self).form_valid(form)



