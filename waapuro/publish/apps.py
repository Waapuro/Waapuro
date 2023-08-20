import time

from django.apps import AppConfig
from django.db import IntegrityError
from django.db.models.signals import post_migrate


class PublishConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'waapuro.publish'

    def ready(self):
        post_migrate.connect(add_default_publish_type, sender=self)
        post_migrate.connect(add_default_status, sender=self)
        post_migrate.connect(add_default_category, sender=self)


def add_default_publish_type(**kwargs):
    from .models import PublishType

    default_publish_types = [
        # Article
        {
            "name": "post",
            "actions": {
                "view": "post",
                "allow_comment": True,
            }, "for_page": False, "for_article": True
        },
        {
            "name": "short_post",
            "actions": {
                "view": "comment",
                "allow_comment": True,
            }, "for_page": False, "for_article": True
        },
        {
            "name": "comment",
            "actions": {
                "view": "comment",
                "allow_comment": True,
            }, "for_page": False, "for_article": True
        },
        # Pages
        {
            "name": "page",
            "actions": {
                "view": "html_page",
                "allow_comment": True,
            }, "for_page": True, "for_article": False
        },
        # Pages And Article
        {
            "name": "image",
            "actions": {
                "view": "image",
                "allow_comment": True,
            }, "for_page": True, "for_article": True
        },
        {
            "name": "video",
            "actions": {
                "view": "video",
                "allow_comment": True,
            }, "for_page": True, "for_article": True
        },
        {
            "name": "attachment",
            "actions": {
                "view": "attachment",
                "allow_comment": False,
            }, "for_page": True, "for_article": True
        },
    ]

    for publish_type_data in default_publish_types:
        PublishType.objects.get_or_create(**publish_type_data)


def add_default_status(**kwargs):
    from .models import Status

    default_publish_types = [
        # Article
        {
            "name": "published",
            "actions": {
                "public": True,
                "password": False,
                "ping_on_top": False,
                "hide_on_list": False,
                "plan_to_publish": False,
                "plan_publish_time": 0.0,
                "allow_comment": True,
            }
        },
        {
            "name": "draft",
            "actions": {
                "public": False,
                "password": False,
                "ping_on_top": False,
                "hide_on_list": True,
                "plan_to_publish": False,
                "plan_publish_time": 0.0,
                "allow_comment": False,
            }
        },
        {
            "name": "planned",
            "actions": {
                "public": False,
                "password": False,
                "ping_on_top": False,
                "hide_on_list": False,
                "plan_to_publish": True,
                "plan_publish_time": time.time() + float(10 ^ 9),
                "allow_comment": False,
            }
        },

    ]

    for publish_type_data in default_publish_types:
        try:
            Status.objects.get_or_create(**publish_type_data)
        except IntegrityError:
            pass


def add_default_category(**kwargs):
    from .models import Category

    default_publish_types = [
        # Article
        {
            "name": "miss",
        }
    ]

    for publish_type_data in default_publish_types:
        try:
            Category.objects.get_or_create(**publish_type_data)
        except IntegrityError:
            pass
