from django.contrib import admin

from django.contrib import admin
from .models import Status, PublishType, Tag, Category, Article, Page

# Register your models here.
admin.site.register(Status)
admin.site.register(PublishType)
admin.site.register(Tag)
admin.site.register(Category)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publish_date', 'update_date')
    list_filter = ('author', 'publish_date')
    search_fields = ('title', 'content')


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publish_date', 'update_date')
    list_filter = ('author', 'publish_date')
    search_fields = ('title', 'content')
    prepopulated_fields = {'url': ('title',)}
