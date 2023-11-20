import os
from pathlib import Path
from typing import List

import dj_database_url
from django.core.management.utils import get_random_secret_key
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

SECRET_KEY = os.getenv("SECRET_KEY", get_random_secret_key())

DEBUG = os.getenv("DEBUG", False)

ALLOWED_HOSTS: List[str] = []


# Application definition

UNFOLD_APPS = [
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.guardian",
    "unfold.contrib.simple_history",
    "django.contrib.admin",
]


DEFAULT_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "compressor",
]

AUTH_APPS = ["allauth", "allauth.account", "allauth.socialaccount"]

CORE_APPS = ["accounts", "billing", "crawler"]

THIRD_PARTY_APPS = [
    "simple_history",
    "guardian",
    "django_celery_beat",
    "djmoney",  # MoneyField
    "django_countries",  # CountryField
]

DEV_APPS = [
    "django_browser_reload"
]

INSTALLED_APPS = UNFOLD_APPS + DEFAULT_APPS + AUTH_APPS + CORE_APPS + THIRD_PARTY_APPS
if DEBUG:
    INSTALLED_APPS += DEV_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
]

if DEBUG:
    MIDDLEWARE.append("django_browser_reload.middleware.BrowserReloadMiddleware")

ROOT_URLCONF = "dealscan.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.normpath(os.path.join(BASE_DIR, "dealscan", "templates")),
            os.path.normpath(
                os.path.join(BASE_DIR, "accounts", "templates", "allauth", "account")
            ),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "dealscan.wsgi.application"


# Redis

REDIS_URL = os.getenv("REDIS_URL")

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": dj_database_url.config(
        default="postgres://postgres:postgres@dealscan-db/dealscan",
        conn_max_age=600,
        conn_health_checks=True,
    )
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}


AUTH_USER_MODEL = "accounts.User"

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
    "guardian.backends.ObjectPermissionBackend",
)

SITE_ID = 1
LOGIN_REDIRECT_URL = "/dashboard"
EMAIL_BACKEND = (
    "django.core.mail.backends.console.EmailBackend"
    if DEBUG
    else "django.core.mail.backends.console.EmailBackend"
)  # TODO move to SES
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'none' if DEBUG else 'mandatory'
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Celery

CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = "django-db"
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_IMPORTS = ()
CELERY_REDBEAT_URL = os.getenv("REDBEAT_REDIS_URL", REDIS_URL)

CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers.DatabaseScheduler"

# Stripe

STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = (BASE_DIR / 'locale/', )

# Static

STATIC_ROOT = BASE_DIR / "static"
STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "accounts" / "static",
    BASE_DIR / "dealscan" / "static",
]


MEDIA_ROOT = BASE_DIR / "media"

MEDIA_URL = "/media/"

COMPRESS_ROOT = BASE_DIR / 'static'

COMPRESS_ENABLED = True

STATICFILES_FINDERS = ('compressor.finders.CompressorFinder', 'django.contrib.staticfiles.finders.FileSystemFinder', 'django.contrib.staticfiles.finders.AppDirectoriesFinder',)

# STORAGES = {
#     "default": {
#         "BACKEND": "django.core.files.storage.FileSystemStorage",
#     },
#     "staticfiles": {
#         "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
#     },
# }

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# UNFOLD

UNFOLD = {
    "SITE_TITLE": _("Dealscan.io - Admin Panel"),
    "SITE_HEADER": _("Dealscan.io"),
    "SITE_SYMBOL": "settings",
    "ENVIRONMENT": "dealscan.utils.environment_callback",
    "DASHBOARD_CALLBACK": "dealscan.views.dashboard_callback",
    "LOGIN": {
        "image": lambda request: static("images/admin-bg.jpg"),
    },
    "STYLES": [
        lambda request: static("css/styles.css"),
    ],
    "TABS": [
        {
            "models": ["accounts.user"],
            "items": [
                {
                    "title": _("Users"),
                    "icon": "person",
                    "link": reverse_lazy("admin:accounts_user_changelist"),
                }
            ],
        },
    ],
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        "navigation": [
            {
                "title": _("Navigation"),
                "items": [
                    {
                        "title": _("Dashboard"),
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                    }
                ],
            },
            {
                "title": _("Authorization"),
                "separator": True,
                "items": [
                    {
                        "title": _("Users"),
                        "icon": "person",
                        "link": reverse_lazy("admin:accounts_user_changelist"),
                    },
                    {
                        "title": _("Groups"),
                        "icon": "group",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                    },
                ],
            },
            {
                "title": _("Feeds"),
                "separator": True,
                "items": [
                    {
                        "title": _("Source"),
                        "icon": "feed",
                        "link": reverse_lazy("admin:crawler_source_changelist"),
                    },
                ],
            },
            {
                "title": _("Offers"),
                "separator": True,
                "items": [
                    {
                        "title": _("Offer"),
                        "icon": "article",
                        "link": reverse_lazy("admin:crawler_offer_changelist"),
                    },
                ],
            },
        ],
    },
    "COLORS": {
        "primary": {
            "50": "220 237 200",
            "100": "197 225 165",
            "200": "174 213 129",
            "300": "141 197 93",
            "400": "103 181 77",
            "500": "63 163 72",
            "600": "33 145 78",
            "700": "16 128 84",
            "800": "5 110 79",
            "900": "2 90 61",
            "950": "0 62 42",
        },
    },
    "EXTENSIONS": {
        "modeltranslation": {
            "flags": {
                "en": "🇬🇧",
                "pl": "🇵🇱",
            },
        },
    },
}
