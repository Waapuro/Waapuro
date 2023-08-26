"""
Django's settings for Waapuro project.
https://waapuro.org/

Generated by 'django-admin startproject' using Django 4.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
import secrets
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Load templates
def __interface__init():
    return (
        BASE_DIR / "interface/__init__.py",
        open(BASE_DIR / "configs_demo/interface__init__.py", 'r').read()
    )


try:
    with open(__interface__init()[0], 'r') as init:
        init.close()
except FileNotFoundError:
    with open(__interface__init()[0], 'w+') as init:
        if len(init.read()) <= 0:
            init.write(__interface__init()[1])
        init.close()

with open(__interface__init()[0], 'w+') as init:
    if len(init.read()) <= 0:
        init.write(__interface__init()[1])
    init.close()

import interface

######################################################

# ------------------------------
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.environ.get("DEBUG"))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'waapuro-secretkey'
SECRET_KEY = SECRET_KEY if DEBUG is True else secrets.token_hex(24)

# ------------------------------
# SET ALLOWED HOSTs
ALLOWED_HOSTS = ["*"]

# ------------------------------
# Set template by TEMP_NAME in template's config.json
USING_TEMPLATE = "syoseki"

# ------------------------------
# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'waapuro',
    'waapuro.publish',
    'waapuro.index',
    'waapuro.editor',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

SITEMAPS = {
    # 'yourmodel': YourModelSitemap,
}

# ------------------------------
# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ja'
TIME_ZONE = 'Asia/Tokyo'
USE_I18N = True
USE_TZ = True
CHARSET = 'UTF-8'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# URL_ARTICLE Supported args
# https://docs.waapuro.org/guideline/jyokyusyamuke/articlesnourlpatn
URL_ARTICLE_SUPPORT_ARGS = [
    "Y", "WY", "M", "D", "H", "m", "S",
    "ID", "AUTHOR", "TYPE", "CATEGORY", "TITLE",
]

# Context Processors
CONTEXT_PROCESSORS = [
    "waapuro.context_processors.sitedata",
]

# The config is done.
######################################################

ROOT_URLCONF = 'waapuro.urls'

INTERFACE_DIR = BASE_DIR / "interface"
INSTALLED_TEMPLATES = interface.installed_templates(BASE_DIR, INTERFACE_DIR)

TEMPLATES = []
# Add front templates
for TEMP in INSTALLED_TEMPLATES:
    if TEMP['NAME'].lower() == USING_TEMPLATE.lower():
        del TEMP['TEMP_INFO']
        # add context processors
        TEMP["OPTIONS"]["context_processors"] = TEMP["OPTIONS"]["context_processors"] + CONTEXT_PROCESSORS
        TEMPLATES = [TEMP]

if TEMPLATES is None:
    raise FileNotFoundError('Template "%s" is not found.' % USING_TEMPLATE)

# Add panel templates
# !! DO NOT change here if you don't have a special need.
TEMPLATES.append(
    {
        'NAME': 'waapuro',
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'builtin/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    }
)

WSGI_APPLICATION = 'waapuro.wsgi.application'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATIC_URL = "static/"

# Waapuro Version
# See /README.md
try:
    with open('file.txt', 'r', encoding='utf-8') as f:
        last_line = None
        for line in f:
            latest_version = line
except FileNotFoundError:
    latest_version = 'dev-version'

WAAPURO_VERSION = latest_version
