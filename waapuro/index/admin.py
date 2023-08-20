from django.contrib import admin

from django.contrib import admin
from .models import SiteConfig
from waapuro.context_processors import sitedata

admin.site.site_title = f"{sitedata(None)['SITE_TITLE']} - Waapuro"
admin.site.site_header = f"{sitedata(None)['SITE_TITLE']} - Waapuro"
admin.site.index_title = "Django Admin"


@admin.register(SiteConfig)
class SiteConfigsAdmin(admin.ModelAdmin):
    list_display = ('key', 'value', 'help_text')
    list_filter = ('key',)
    search_fields = ('key', 'value', 'help_text')
