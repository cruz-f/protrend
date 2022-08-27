"""
Django settings for protrend project.

Generated by 'django-admin startproject' using Django 3.2.11.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os.path
from pathlib import Path

from configuration import Configuration


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = Configuration.secret_key

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = Configuration.debug

ALLOWED_HOSTS = Configuration.allowed_hosts

# Application definition

INSTALLED_APPS = [
    'material',
    'material.frontend',
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_neomodel',
    'drf_yasg',
    'data',
    'interfaces',
    'community.apps.CommunityConfig'
]

# do not change middleware order
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'protrend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'interfaces', 'api', 'templates'),
            os.path.join(BASE_DIR, 'interfaces', 'website', 'templates'),
        ],
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

WSGI_APPLICATION = 'protrend.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': Configuration.community_db_engine,
        'NAME': Configuration.community_db_name,
        'USER': Configuration.community_db_user,
        'PASSWORD': Configuration.community_db_password,
        'HOST': Configuration.community_db_ip,
        'PORT': Configuration.community_db_port,
    }
}

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

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'interfaces', 'api', 'static'),
    os.path.join(BASE_DIR, 'interfaces', 'website', 'static'),
]

# the static root should be only used in production.
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Email settings
EMAIL_BACKEND = Configuration.email_backend
EMAIL_HOST = Configuration.email_host
EMAIL_PORT = Configuration.email_port
EMAIL_HOST_USER = Configuration.email_host_user
EMAIL_HOST_PASSWORD = Configuration.email_host_password
EMAIL_USE_TLS = Configuration.email_use_tls

DEFAULT_FROM_EMAIL = Configuration.email_default

ACCOUNT_EMAIL_VERIFICATION = Configuration.email_verification

# Custom user
AUTH_USER_MODEL = 'community.CommunityUser'

# Login/Logout
LOGOUT_REDIRECT_URL = '/'
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = 'sign-in'

# django-rest framework settings
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 50,
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '3/second',
        'user': '5/second'
    },
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework_csv.renderers.CSVRenderer',
        'drf_renderer_xlsx.renderers.XLSXRenderer',
        'rest_framework_xml.renderers.XMLRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
}

# django-neomodel settings
NEOMODEL_NEO4J_BOLT_URL = Configuration.bolt_url
NEOMODEL_SIGNALS = True
NEOMODEL_FORCE_TIMEZONE = False
NEOMODEL_MAX_CONNECTION_POOL_SIZE = 50

# django admin interface by GRAPPELLI
GRAPPELLI_ADMIN_TITLE = 'ProTReND Admin Area'
GRAPPELLI_SWITCH_USER = True
