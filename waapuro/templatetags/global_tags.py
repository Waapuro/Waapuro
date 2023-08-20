from django import template

from waapuro import settings

register = template.Library()


@register.simple_tag
def front(static_file_path=''):
    return '/front/' + static_file_path


@register.simple_tag
def language_code():
    return settings.LANGUAGE_CODE


@register.simple_tag
def language_code():
    return settings.LANGUAGE_CODE
