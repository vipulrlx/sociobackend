from django.apps import AppConfig
from django.conf import settings
from django.template.context_processors import request


class WebConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "web"


def google_client_id(request):
    return {"GOOGLE_CLIENT_ID": settings.GOOGLE_OAUTH_CLIENT_ID}
