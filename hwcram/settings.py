from __future__ import absolute_import
"""
Django settings for hwcram project.

Generated by 'django-admin startproject' using Django 1.11.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import sys
from datetime import timedelta

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'o)3$s33s7efi^m)ho6@&_j#v4#y59yyrv8j0&mmrcf%)cdj0(r'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['49.4.1.107']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ecs',
    'vpc',
    'account',
    'xadmin',
    'crispy_forms',
    'import_export',
    'django_crontab',
    'kombu.transport.django',
    'djcelery',
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

ROOT_URLCONF = 'hwcram.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'hwcram.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hwcram',
        'USER': 'root',
        'PASSWORD': 'asdf#199991',
        'HOST': '',
        'PORT': '',
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

#LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'zh-Hans'

#TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

#django_crontab
CRONJOBS = [
    ('*/1 * * * *', 'crontab.cron.cron_nginx','> /dev/null'),
    ('*/1 * * * *', 'crontab.cron.cron_uwsgi','> /dev/null'),
    ('*/1 * * * *', 'crontab.cron.cron_celery','> /dev/null'),
    ('*/1 * * * *', 'crontab.cron.cron_celerybeat','> /dev/null'),
    #('*/1 * * * *', 'crontab.cron.update_token','> /dev/null'),
]

BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
#CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_TIMEZONE = TIME_ZONE

CELERYBEAT_SCHEDULE = {
    'ecs-task-20-seconds': {
        'task': 'ecs.tasks.ecs_task',
        'schedule': timedelta(seconds=20),
        'args': ()
    },
    'ip-task-20-seconds': {
        'task': 'vpc.tasks.ip_task',
        'schedule': timedelta(seconds=20),
        'args': ()
    },
    'token-task-30-minutes': {
        'task': 'account.tasks.token_task',
        'schedule': timedelta(minutes=30),
        'args': ()
    },
#    # Executes every Monday morning at 7:30 A.M
#    'add-every-1-minute': {
#        'task': 'apptest.tasks.test_celery3',
#        'schedule': crontab(minute='*/1'),
#        'args': ('test_celery3',),
#    },
}
