"""
Django settings for setup_main project.

Generated by 'django-admin startproject' using Django 2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
from environs import Env
import logging.config


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# #############################################################################
# ######################## Sensitive Section ##################################
# #############################################################################
env = Env()
env.read_env(recurse=True)


# Determine the Environment
ENVIRONMENT = env.str("ENVIRONMENT")
ADMIN_ENABLED = env.bool("ADMIN_ENABLED")
IS_LOCAL = env.bool("IS_LOCAL")
DEBUG = env.bool("DEBUG", False)

# Security Variable
SECRET_KEY = env.str("DJANGO_SECRET_KEY")
SESSION_COOKIE_SECURE = env.bool("SESSION_COOKIE_SECURE", False)
CSRF_COOKIE_SECURE = env.bool("CSRF_COOKIE_SECURE", False)
SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT", False)
SECURE_BROWSER_XSS_FILTER = env.bool("SECURE_BROWSER_XSS_FILTER", True)

# set hosts
ALLOWED_HOSTS = ["setupfaq.com",
                 "www.setupfaq.com",
                 "18.188.191.243",
                 "ec2-18-188-191-243.us-east-2.compute.amazonaws.com"]
if ENVIRONMENT == "dev":
    ALLOWED_HOSTS += ["localhost", "127.0.0.1", '0.0.0.0']


# Application definition
ROOT_URLCONF = "setup_main.urls"
LOCAL_INSTALLED_APPS = ["apps.website"]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    # 3rd party apps
    "corsheaders",
    "behave_django",
    'django_extensions',
    'ckeditor',
    'ckeditor_uploader'
] + LOCAL_INSTALLED_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 3rd party middleware
    "corsheaders.middleware.CorsMiddleware",
    "apps.website.middleware.AttachResponseHeaders",
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'setup_main.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
# PostgreSQL Db

DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env.str("POSTGRES_DB_DATABASE"),
        "USER": env.str("POSTGRES_DB_USERNAME"),
        "PASSWORD": env.str("POSTGRES_DB_PASSWORD"),
        "HOST": env.str("POSTGRES_DB_HOST"),
        "PORT": env.str("POSTGRES_DB_PORT"),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

# #############################################################################
# ######################## Authentication Settings ############################
# #############################################################################
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation"
                ".UserAttributeSimilarityValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation"
                ".MinimumLengthValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation"
                ".CommonPasswordValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation"
                ".NumericPasswordValidator"
    },
]

# Log settings
# https://docs.djangoproject.com/en/2.2/topics/logging/

LOG_FORMAT = os.getenv(
    "LOG_FORMAT",
    f"%(asctime)s:{logging.BASIC_FORMAT}"
)
LOG_LEVEL = env.int("LOG_LEVEL", logging.DEBUG)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': LOG_FORMAT,
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'apps': {
            'handlers': ['console'],
            'level': LOG_LEVEL,
            'propagate': True,
        },
        'setup_main': {
            'handlers': ['console'],
            'level': LOG_LEVEL,
            'propagate': True,
        },
    },
}

# CKEditor Settings
CKEDITOR_FILENAME_GENERATOR = 'apps.website.helpers.utils.get_filename'
CKEDITOR_UPLOAD_SLUGIFY_FILENAME = env.bool('CKEDITOR_UPLOAD_SLUGIFY_FILENAME')
CKEDITOR_IMAGE_BACKEND = env.str('CKEDITOR_IMAGE_BACKEND')
CKEDITOR_BROWSE_SHOW_DIRS = env.bool('CKEDITOR_BROWSE_SHOW_DIRS')
CKEDITOR_FORCE_JPEG_COMPRESSION = env.bool('CKEDITOR_FORCE_JPEG_COMPRESSION')
CKEDITOR_IMAGE_QUALITY = env.int('CKEDITOR_IMAGE_QUALITY')
CKEDITOR_THUMBNAIL_SIZE = [env.int('CKEDITOR_THUMBNAIL_WIDTH'),
                           env.int('CKEDITOR_THUMBNAIL_HEIGHT')]
CKEDITOR_ALLOW_NONIMAGE_FILES = False

# Media files (upload path)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.abspath(os.path.join(BASE_DIR, 'media/uploads/'))
CKEDITOR_UPLOAD_PATH = 'images/'

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 600,
        'width': 'auto',
    },
}

# GMAIL Settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_SSL = env.bool('EMAIL_USE_SSL')
EMAIL_PORT = env.int('EMAIL_PORT')
EMAIL_HOST_USER = env.str('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD')
WEBSITE_ADMIN_EMAIL = env.str('WEBSITE_ADMIN_EMAIL')
