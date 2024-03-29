from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views
from django.conf.urls import url, include
from markdownx import urls as markdownx

urlpatterns = [

    path("users/", include("color.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
    path("news/", include("color.news.urls", namespace="news")),
    path("articles/", include("color.articles.urls", namespace='articles')),
    path('markdownx/', include('markdownx.urls')),
    url(r'^comments/', include('django_comments.urls')),
    path("qa/", include('color.qa.urls', namespace='qa')),
    path("chat/", include('color.chat.urls', namespace='chat')),
    path("notification/", include('color.notification.urls', namespace='notification')),
    url(r'^search/', include('haystack.urls'))

    # Your stuff: custom urls includes go here
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
