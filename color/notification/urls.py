from django.urls import include, path


from color.notification import views


app_name = "notification"
urlpatterns = [
    path('list/', views.NotificationList.as_view(), name='list'),
    path('make_all_read/', views.mark_all_notification_read, name='all_read'),
    path('recent_notifications/', views.get_recent_notification, name='recent_notifications'),
    path('single/<int:id>', views.make_single_read, name='single_read')
]


