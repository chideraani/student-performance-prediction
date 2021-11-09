"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os
import django_heroku

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-#9m8i73j1%#0gx%-kp7e0u9c%zo0&wyer8bfzq4n)u@o(&t7jo'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['https://student-pattern-prediction-app.herokuapp.com',
'localhost',
'127.0.0.1']

X_FRAME_OPTIONS = 'SAMEORIGIN'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'authenticate',
    # 'django_plotly_dash.apps.DjangoPlotlyDashConfig'
    # 'channels',
    # 'channels_redis'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
]

ROOT_URLCONF = 'mysite.urls'

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
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME':'viz',
#         'USER' : 'postgres',
#         'PASSWORD' : 'chidera',
#         'HOST' : 'localhost'
#     }
# }



# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# ———- Add Django Dash start ——————————–
# Adding ASGI Application
# ASGI_APPLICATION = 'authenticate.routing.application'
#
# To use home.html as default home page
# LOGIN_REDIRECT_URL = '‘home’'
# LOGOUT_REDIRECT_URL = ‘home’
# Define folder location of ‘static’ folder
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# ‘django_dash’: django app name
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'authenticate', 'static'),
    ]
# Static content of Plotly components that should
# be handled by the Django staticfiles infrastructure
# PLOTLY_COMPONENTS = [
#     'dash_core_components',
#     'dash_html_components',
#     'dash_bootstrap_components',
#     'dash_render',
#     'dpd_components',
#     'dpd_static_support'



STATICFILES_LOCATION = 'static'
STATIC_URL = '/static/'
STATIC_ROOT = 'authenticate/static'

STATICFILES_DIRS = [os.path.join(BASE_DIR,'static')]


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Activate Django-Heroku.
django_heroku.settings(locals())
