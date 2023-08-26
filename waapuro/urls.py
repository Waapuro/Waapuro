"""
URL configuration for waapuro project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os
import random

from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include, re_path
from django.views.static import serve

from waapuro import sitemaps, settings
from waapuro.configs import db_config_all, migrating

from waapuro.index import views as index

# Load Database site configs
if not migrating():
    from waapuro.index.apps import add_default_site_config

    add_default_site_config()

site_configs = db_config_all()

urlpatterns = [
    # Basic
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path('favicon.ico', index.favicon),

    # Admin Views
    path(f'{site_configs["URL_DJANGO_ADMIN"] if site_configs is not None else random.random()}/', admin.site.urls),

    # Built-in Web & Static
    re_path(r'^builtin/static/(?P<path>.*)$', serve, {'document_root': 'builtin/static'}),
    path('builtin/version', index.version),
    # WAAAAAPURO!!!!!!!!!!
    path('builtin/waapuro', index.waapuro_logo)
]

# Static files (CSS, JavaScript, Images)
# NOT Django origin

if settings.DEBUG:
    default = True
    for TEMPLATE in settings.TEMPLATES:
        templates_base = TEMPLATE['DIRS'][0]
        static_path = os.path.join(templates_base, "static")
        if default:
            urlpatterns += static('front', document_root=static_path)
        url = os.path.join(os.path.basename(templates_base), 'front').replace('\\', '/')
        urlpatterns += static(url, document_root=static_path)

# Front Views
# etc. page article
urlpatterns.append(path('', include('waapuro.index.urls')))
