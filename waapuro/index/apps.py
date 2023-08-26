import sys

from django.apps import AppConfig, apps
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_migrate

from waapuro import publish

from configs_demo import db_configs


class IndexConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'waapuro.index'

    def ready(self):
        PublishType = apps.get_model('publish', 'PublishType')
        try:
            post_migrate.connect(add_default_site_config, sender=self)
        except PublishType.DoesNotExist:
            publish.default_app_config()
            self.ready()


def add_default_site_config(**kwargs):
    from .models import SiteConfig

    configs = db_configs.sample()

    for config in configs:
        try:
            SiteConfig.objects.get(key=config['key'])
        except ObjectDoesNotExist:
            SiteConfig.objects.create(**config)
