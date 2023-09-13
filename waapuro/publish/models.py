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


class PublishIndex(models.Model):
    """PublishIndex"""

    def __str__(self):
        return self.id

    id = models.AutoField("Index ID", primary_key=True)
    filepath = models.CharField("Filepath", max_length=4096, help_text="Waapuro files path.")

    class Meta:
        permissions = [
            ("can_read_PublishIndex".lower(), "Can read PublishIndex info"),
            ("can_write_PublishIndex".lower(), "Can write PublishIndex info"),
        ]
        verbose_name = "PublishIndex"
        verbose_name_plural = "PublishIndex"


class Tags(models.Model):
    """Tags Index"""

    def __str__(self):
        return self.name

    id = models.AutoField("ID", primary_key=True)
    name = models.CharField("Tag name", max_length=64, help_text="Content of tag.")
    author = models.ForeignKey(PublishIndex, on_delete=models.CASCADE)

    class Meta:
        permissions = [
            ("can_read_Tags".lower(), "Can read Tags info"),
            ("can_write_Tags".lower(), "Can write Tags info"),
        ]
        verbose_name = "Tags Index"
        verbose_name_plural = "Tags Index"


class Article(models.Model):
    """文章"""

    def __str__(self):
        return self.title

    index_id = models.BigAutoField("ID", primary_key=True, help_text="ID")
    status = models.ForeignKey(
        Status, null=True, on_delete=models.SET_NULL,
        help_text="https://docs.waapuro.org/start/guideline/waapurocode/profile-tag/status"
    )
    url = models.SlugField(
        unique=True, null=True, blank=True
    )
    """Just cache at database for index, The following must be based on the Waapuro XML"""
    wc_id = models.CharField("Waapuro Code ID", max_length=36, help_text="ID")
    parent = models.ForeignKey(
        'self',  # TODO: Change it: To save parent's id
        on_delete=models.SET_NULL, null=True, blank=True, related_name='children'
    )
    last_version = models.CharField(
        "Last Version",  # TODO: Just cache at database for index
        max_length=128, null=True, help_text="Article ID of Last version (It's First version when 'None')"
    )
    title = models.CharField(
        "Title",  # TODO: Just cache at database for index
        max_length=128, null=True, help_text="Title"
    )
    excerpt = models.TextField(
        "Excerpt",  # Auto generate or write by author  # TODO: Just cache at database for index
        null=True, help_text="It will be show at FEED or List. Auto generate & write by author"
    )  # Just cache at database for index
    publish_date = models.DateTimeField(
        "Publish Date",  # TODO: Just cache at database for index
        auto_now_add=True, help_text="Published date"
    )
    author = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL,  # TODO: Just cache at database for index
        help_text="Status and Settings of page or article"
    )
    type = models.ForeignKey(  # TODO: Just cache at database for index
        PublishType, null=True, on_delete=models.SET_NULL, help_text="Type of this article"
    )
    content = models.TextField(
        "Content",  # Waapuro code
        null=True, help_text="Waapuro Code <content>"
    )

    def save(self, *args, **kwargs):
        if not self.url:
            self.url = slugify(self.title)
        super(Article, self).save(*args, **kwargs)

    class Meta:
        permissions = [
            ("can_read_Article".lower(), "Can read Article info"),
            ("can_write_Article".lower(), "Can write Article info"),
        ]
        verbose_name = "Article"
        verbose_name_plural = "Articles"


class ArticleUrlWcfMapping(models.Model):
    """Article URL <=> WaapuroCode File Mapping"""

    url = models.TextField("URL", unique=True)
    wc_path = models.TextField("WaapuroCode Path", unique=True)

    class Meta:
        permissions = [
            ("can_read_ArticleUrlWcfMapping".lower(), "Can read ArticleUrlWcfMapping info"),
            ("can_write_ArticleUrlWcfMapping".lower(), "Can write ArticleUrlWcfMapping info"),
        ]
        verbose_name = "Article URL WaapuroCode File Mapping"
        verbose_name_plural = "URL-File Mapping"


class Page(models.Model):
    """ページ"""

    def __str__(self):
        return self.title

    id = models.BigAutoField("ID", primary_key=True, help_text="ID")
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    title = models.CharField("Title", max_length=128, null=True, blank=True, help_text="Title")
    content = models.TextField("Content", null=True, blank=True, help_text="Your content")
    excerpt = models.TextField("Excerpt", null=True, blank=True, help_text="Show at FEED or list")
    publish_date = models.DateTimeField(auto_now_add=True, help_text="Published date")
    update_date = models.DateTimeField(auto_now=True, help_text="Updated date")
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL,
                               help_text="Status and Settings of page or article")
    type = models.ForeignKey(PublishType, null=True, blank=True, on_delete=models.SET_NULL,
                             help_text="Type of this article")
    status = models.ForeignKey(Status, null=True, blank=True, on_delete=models.SET_NULL,
                               help_text="Show at FEED or list")
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL, help_text="Category")
    url = models.SlugField(unique=True)

    class Meta:
        permissions = [
            ("can_read_Page".lower(), "Can read Page info"),
            ("can_write_Page".lower(), "Can write Page info"),
        ]
        verbose_name = "Page"
        verbose_name_plural = "Pages"
