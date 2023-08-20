import os.path

from django import template

from waapuro import paginate_queryset, settings
from waapuro.publish.models import *

register = template.Library()
template_gears_path = os.path.join(settings.TEMPLATES[0]["DIRS"][0], "gears")


@register.inclusion_tag(os.path.join(template_gears_path, "articles_list.html"))
def articles_list(p=1, per_page=15):
    article = Article.objects.all().order_by('-publish_date')
    return paginate_queryset(article, p, per_page)
