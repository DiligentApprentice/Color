from django.urls import include, path

from articles import views


app_name = "articles"
urlpatterns = [
   path('list/', views.ArticleListView.as_view(), name='list'),
    path('create-article/', views.ArticleCreateView.as_view(), name='write_new'),
    path('detail/<str:slug>/',views.ArticleDetailView.as_view(), name='detail' ),
    path('drafts/', views.DraftListView.as_view(), name="drafts"),
    path('create-draft/', views.DraftCreateView.as_view(), name='write_draft'),
    path('edit/<int:pk>', views.ArticleUpdateView.as_view(), name='update')

]


