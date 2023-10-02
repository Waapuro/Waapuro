import re

from django.http import Http404
from django.urls import path
from django.conf.urls.static import static
from . import views
from .views import article
# from .models import SiteConfig
from .. import settings
from ..configs import db_config


def handle_request(request, sub_path):
    try:
        return article(request, sub_path)
    except Http404:
        raise Http404()


urlpatterns = [
    path('', views.index),
    path("<path:sub_path>", handle_request, name='handle_request'),
]
