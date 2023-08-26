import random
import sys

""" FAKE MODEL """


class FakeManager:
    @staticmethod
    def get(*args, **kwargs):
        return None


class FakeModel:
    objects = FakeManager()

    def __getattr__(self, name):
        return None


def migrating():
    return 'migrate' in sys.argv or 'makemigrations' in sys.argv


""" LOAD DB CONFIGS """


def db_config(key):
    if not migrating():
        from waapuro.index.models import SiteConfig
        return SiteConfig.objects.get(key=key).value
    else:
        return "migrating"


def db_config_all():
    if not migrating():
        # Auto Add Config

        from waapuro.index.models import SiteConfig
        key_values_query = SiteConfig.objects.values('key', 'value')
        key_value_dict = {}

        for item in key_values_query:
            key = item['key']
            value = item['value']

            key_value_dict[key] = value

        return key_value_dict
    else:
        return None
