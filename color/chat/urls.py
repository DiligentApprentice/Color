from django.urls import include, path

from chat import views


app_name = "chat"
urlpatterns = [
   path("list/", views.MessageListView.as_view(), name='list'),
    path("singeldetail/<str:username>/", views.SingleMessageListView.as_view(), name='single'),
    path("messages/send-message/", views.post_messages, name="post_message")
]


