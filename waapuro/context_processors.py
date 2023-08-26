import time

from django.db import OperationalError

from waapuro import settings
from waapuro.configs import db_config
from waapuro.index.models import SiteConfig


def sitedata(request):
    config_keys = [
        "SITE_TITLE",
        "SITE_TITLE_YOMI",
        "SITE_SUBTITLE",
        "SITE_SUBTITLE_YOMI",
        "SITE_URL",
        "ESTABLISHMENT_AT"
    ]

    default_values = {
        "SITE_TITLE": "undefined",
        "SITE_TITLE_YOMI": "",
        "SITE_SUBTITLE": "it's look like a new site.",
        "SITE_SUBTITLE_YOMI": "",
        "SITE_URL": "https://example.com/",
        "ESTABLISHMENT_AT": 0.0
    }

    context = {
        'LANGUAGE_CODE': settings.LANGUAGE_CODE,
        'CHARSET': settings.CHARSET,
        'ESTABLISHMENT_AT': time.time(),
    }

    for key in config_keys:
        try:
            value = db_config(key)
        except (OperationalError, SiteConfig.DoesNotExist):
            value = default_values[key]
        context[key] = value

    return context
