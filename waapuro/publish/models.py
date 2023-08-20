from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


class Status(models.Model):
    """Status and Settings of page or article"""

    def __str__(self):
        return self.name

    id = models.BigAutoField("ID", primary_key=True, help_text="ID")
    name = models.CharField("Name", unique=True, max_length=24, null=True, help_text="Name")
    actions = models.JSONField("Actions", default=dict, help_text="Actions")

    class Meta:
        permissions = [
            ("can_read_Status".lower(), "Can read Status info"),
            ("can_write_Status".lower(), "Can write Status info"),
        ]
        verbose_name = "Status"
        verbose_name_plural = "Status"


class PublishType(models.Model):
    """
    Type of publish

    * Default
     - Article
        post
        short_post
        comment

     - Pages
     　　page

     - Pages And Article
        image
        video
        attachment
    """

    def __str__(self):
        return self.name

    id = models.BigAutoField("ID", primary_key=True, help_text="ID")
    name = models.CharField("Type Name", unique=True, max_length=24, null=True, help_text="Type Name")
    actions = models.JSONField("Actions", default=dict, help_text="What Actions will be perform in this Type.")
    for_page = models.BooleanField("For Pages", default=True,
                                   help_text="If you don't use this type for pages, uncheck it.")
    for_article = models.BooleanField("For Article", default=True,
                                      help_text="If you don't use this type for article, uncheck it.")

    class Meta:
        permissions = [
            ("can_read_PublishType".lower(), "Can read PublishType info"),
            ("can_write_PublishType".lower(), "Can write PublishType info"),
        ]
        verbose_name = "PublishType"
        verbose_name_plural = "PublishTypes"


class Tag(models.Model):
    """Tags"""

    def __str__(self):
        return self.name

    id = models.BigAutoField("ID", primary_key=True, help_text="ID")
    name = models.CharField("Tag Name", unique=True, max_length=24, null=True, help_text="Tag Name")
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')

    class Meta:
        permissions = [
            ("can_read_Tag".lower(), "Can read Tag info"),
            ("can_write_Tag".lower(), "Can write Tag info"),
        ]
        verbose_name = "Tags"
        verbose_name_plural = "Tags"


class Category(models.Model):
    """分類"""

    def __str__(self):
        return self.name

    id = models.BigAutoField("ID", primary_key=True, help_text="ID")
    name = models.CharField("Category Name", max_length=24, null=True, help_text="Category Name")
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')

    class Meta:
        permissions = [
            ("can_read_Category".lower(), "Can read Category info"),
            ("can_write_Category".lower(), "Can write Category info"),
        ]
        verbose_name = "Category"
        verbose_name_plural = "Categories"


"""#### Publishes Model ####"""


class Article(models.Model):
    """文章"""

    def __str__(self):
        return self.title

    id = models.BigAutoField("ID", primary_key=True, help_text="ID")
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    title = models.CharField("Title", max_length=128, null=True, help_text="Title")
    content = models.TextField("Content", null=True, help_text="Your content")
    excerpt = models.TextField("Excerpt", null=True, help_text="Show at FEED or list")
    publish_date = models.DateTimeField(auto_now_add=True, help_text="Published date")
    update_date = models.DateTimeField(auto_now=True, help_text="Updated date")
    data = models.JSONField(null=True, blank=True, default=dict)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL,
                               help_text="Status and Settings of page or article")
    type = models.ForeignKey(PublishType, null=True, on_delete=models.SET_NULL, help_text="Type of this article")
    status = models.ForeignKey(Status, null=True, on_delete=models.SET_NULL,
                               help_text="etc.Published, Draft or Planned")
    tags = models.ForeignKey(Tag, null=True, blank=True, on_delete=models.SET_NULL, help_text="Tags")
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL, help_text="Category")
    custom_url = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.custom_url:
            self.custom_url = slugify(self.title)
        super(Article, self).save(*args, **kwargs)

    class Meta:
        permissions = [
            ("can_read_Article".lower(), "Can read Article info"),
            ("can_write_Article".lower(), "Can write Article info"),
        ]
        verbose_name = "Article"
        verbose_name_plural = "Articles"


class Page(models.Model):
    """ページ"""

    def __str__(self):
        return self.title

    id = models.BigAutoField("ID", primary_key=True, help_text="ID")
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    title = models.CharField("Title", max_length=128, null=True, help_text="Title")
    content = models.TextField("Content", null=True, help_text="Your content")
    excerpt = models.TextField("Excerpt", null=True, help_text="Show at FEED or list")
    publish_date = models.DateTimeField(auto_now_add=True, help_text="Published date")
    update_date = models.DateTimeField(auto_now=True, help_text="Updated date")
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL,
                               help_text="Status and Settings of page or article")
    type = models.ForeignKey(PublishType, null=True, on_delete=models.SET_NULL, help_text="Type of this article")
    status = models.ForeignKey(Status, null=True, on_delete=models.SET_NULL, help_text="Show at FEED or list")
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL, help_text="Category")
    url = models.SlugField(unique=True)

    class Meta:
        permissions = [
            ("can_read_Page".lower(), "Can read Page info"),
            ("can_write_Page".lower(), "Can write Page info"),
        ]
        verbose_name = "Page"
        verbose_name_plural = "Pages"
