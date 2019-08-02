from django.urls import include, path

from qa import views



app_name = "qa"
urlpatterns = [
    path('un-answer-questionlist/',views.QAUnQusestionListView.as_view(), name='unanswered_q' ),
    path('has-answer-questionlist/', views.QAHaveQusestionListView.as_view(), name='answered_q'),
    path('all-questionlist/', views.QAListView.as_view(), name='all_q'),
    path('create-question/', views.QACreateView.as_view(), name='ask_question'),
    path('detail-question/<str:slug>/', views.QADetailView.as_view(), name='question_detail'),
    path('create-answer/<int:question_id>/', views.AnswerCreateView.as_view(), name='propose_answer'),
    path('question/vote/', views.post_question_vote, name='post_question_vote'),
    path('answer/vote/', views.post_answer_vote, name='post_answer_vote'),
    path('accept-answer/', views.post_accept_answer ,name='post_accept_answer')
]


