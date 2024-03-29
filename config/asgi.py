import os
import sys
import django
from channels.routing import get_default_application

app_path = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)
)
sys.path.append(os.path.join(app_path, "color"))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
django.setup()
application = get_default_application()
