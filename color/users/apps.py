from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "color.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import color.users.signals  # noqa F401
        except ImportError:
            pass
