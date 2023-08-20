from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.template import engines

from waapuro import settings
from waapuro.publish.models import Article


def index(request):
    return render(request, 'index.html')


def article(request, *args, **kwargs):
    filters = {}

    search_fields = ['id', 'author', 'type', 'category', 'title']

    # 将kwargs的键转换为小写
    kwargs_lower = {k.lower(): v for k, v in kwargs.items()}

    for field in search_fields:
        value = kwargs_lower.get(field)
        if value is not None:
            filters[field] = value

    matched = Article.objects.filter(**filters).first()

    if not matched:
        raise Http404()
    else:
        return render(request, "article.html", {
            "article": matched,
        })


""" Build-in Pages """


def version(request):
    return render(request, 'waapuro.html', {
        'settings': settings
    }, using='waapuro')
