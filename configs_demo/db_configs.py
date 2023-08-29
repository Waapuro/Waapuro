from django.utils.crypto import get_random_string

from waapuro.configs import migrating, FakeModel


def sample():
    if migrating():
        PublishType = FakeModel()
    else:
        from django.apps import apps
        PublishType = apps.get_model('publish', 'PublishType')

    return [
        {
            "key": "SITE_TITLE",
            "value": "無名サイト",
            "help_text": "Main title of the website."
        },
        {
            "key": "SITE_TITLE_YOMI",
            "value": "むめいサイト",
            "help_text": "Phonetic reading of the main title in katakana."
        },
        {
            "key": "SITE_SUBTITLE",
            "value": "創作を始めよう。",
            "help_text": "Subtitle or description of the website in Japanese."
        },
        {
            "key": "SITE_SUBTITLE_YOMI",
            "value": "Let's begin creating.",
            "help_text": "Phonetic reading of the subtitle in katakana."
        },
        {
            "key": "SITE_URL",
            "value": "https://waapuro.org",
            "help_text": "The Homepage URL of the website."
        },
        {
            "key": "ARTICLE_DEFAULT_TYPE",
            "value": PublishType.objects.get(name="post"),
            "help_text": "Default type of the Articles."
        },
        {
            "key": "PAGE_DEFAULT_TYPE",
            "value": PublishType.objects.get(name="page"),
            "help_text": "Default type of the Pages."
        },
        {
            "key": "URL_DJANGO_ADMIN",
            "value": f"admin/{get_random_string(length=12)}",
            "help_text": "You DON'T NEED add '/' in the 'start' AND 'end'!!"
        },
        {
            "key": "URL_ARTICLE",
            "value": "/post/{TITLE}",
            "help_text": "ARTICLE's pattern. See Document at: https://docs.waapuro.org/"
        },
        {
            "key": "CODE_CLASSTAG_ALLOW",
            "value": "disable",
            "help_text": "ARTICLE's pattern. See Document at: https://docs.waapuro.org/"
        },
    ]
