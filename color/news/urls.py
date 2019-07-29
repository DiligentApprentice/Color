from django.urls import include, path

from news.views import NewsListView
from news import views


app_name = "news"
urlpatterns = [
    path('newslist/', NewsListView.as_view(), name="list"),
    path('post-news/',views.post_news, name="post_news"),
    path('like/',views.post_like_or_cancle, name="like"),
    path('get-thread/',views.get_relation_comments, name="comments"),
    path('post-comment/', views.post_comment, name="post_comment"),
    path('delete/<pk>/', views.NewsDeleteVieww.as_view(), name="delete_news"),
]


