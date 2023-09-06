import re

from django.urls import path
from django.conf.urls.static import static
from . import views
# from .models import SiteConfig
from .. import settings
from ..configs import db_config

urlpatterns = [
    path('status/', views.index_status),
]
