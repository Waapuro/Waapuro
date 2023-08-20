import re

from django.urls import path
from django.conf.urls.static import static
from . import views
from .models import SiteConfig
from .. import settings

"""### resolver ###"""


def convert_to_django_pattern(input_format):
    url = re.sub(r'{(.*?)}', r'<str:\1>', input_format) + "/"
    return url[1:] if url.startswith('/') else url


def url_articles_resolver(URL_ARTICLE=SiteConfig.objects.get(key="URL_ARTICLE").value):
    using_args = re.findall(r"{(.*?)}", URL_ARTICLE)
    if not set(using_args).issubset(set(settings.URL_ARTICLE_SUPPORT_ARGS)):
        raise ValueError("An unexpected value was received. \r"
                         f"URL_ARTICLE: {URL_ARTICLE}\r"
                         f"settings.URL_ARTICLE_SUPPORT_ARGS: {settings.URL_ARTICLE_SUPPORT_ARGS}")
    return [
        path(convert_to_django_pattern(URL_ARTICLE), views.article, name='article_detail')
    ]


def url_pages_resolver():
    return [

    ]


"""### url profile ###"""

urlpatterns = [
    path('', views.index),
]
urlpatterns += url_articles_resolver() + url_pages_resolver()
