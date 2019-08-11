from django.urls import path
from color.users import views

app_name = "users"
urlpatterns = [
    path("update/", views.UserUpdateView.as_view(), name="update"),
    path("detail/<str:username>/", views.UserDetailView.as_view(), name="detail")
]
