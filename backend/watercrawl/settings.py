"""
Django settings for watercrawl project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from datetime import timedelta
from pathlib import Path

from celery.schedules import crontab
from corsheaders.defaults import default_headers
from environ import Env

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Read environment variables from .env file
env = Env()
env.read_env(BASE_DIR / ".env")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env(
    "SECRET_KEY",
    cast=str,
    default="django-insecure-el4wo4a4--=f0+ag#omp@^w4eq^8v4(scda&1a(td_y2@=sh6&",
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG", cast=bool, default=True)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "django_celery_results",
    "django_celery_beat",
    "django_minio_backend",
    "rest_framework_simplejwt",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "corsheaders",
    "django_filters",
    "common",
    "core",
    "user",
    "plan",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "watercrawl.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "watercrawl.wsgi.application"

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": env.db("DATABASE_URL", default="sqlite:///db.sqlite3"),
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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

# cache and lock settings

REDIS_LOCKER_CONFIG = env.db_url("REDIS_LOCKER_URL", default="redis://redis:6379/3")

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = env("LANGUAGE_CODE", cast=str, default="en-us")

TIME_ZONE = env("TIME_ZONE", cast=str, default="UTC")

USE_I18N = env("USE_I18N", cast=bool, default=True)

USE_TZ = env("USE_TZ", cast=bool, default=True)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STORAGES = {
    "staticfiles": {
        "BACKEND": env(
            "STATICFILES_STORAGE",
            cast=str,
            default="django_minio_backend.models.MinioBackendStatic",
        ),
    },
    "default": {
        "BACKEND": env(
            "DEFAULT_FILE_STORAGE",
            cast=str,
            default="django_minio_backend.models.MinioBackend",
        ),
    },
    "media": {
        "BACKEND": env(
            "DEFAULT_FILE_STORAGE",
            cast=str,
            default="django_minio_backend.models.MinioBackend",
        ),
    },
}
STATIC_URL = "/static/"
STATIC_ROOT = env("STATIC_ROOT", cast=str, default="storage/static/")
MEDIA_URL = "/media/"
MEDIA_ROOT = env("MEDIA_ROOT", cast=str, default="storage/media/")

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "user.User"

# Rest Framework settings
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PAGINATION_CLASS": "common.pagination.PageNumberPagination",
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_SCHEMA_CLASS": "common.schema.WatterCrawlAutoSchema",
    "EXCEPTION_HANDLER": "common.handlers.water_crawl_exception_handler",
    "PAGE_SIZE": 10,
}

# DRF Spectacular settings
SPECTACULAR_SETTINGS = {
    "TITLE": "WaterCrawl API",
    "DESCRIPTION": "API documentation for WaterCrawl",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    # 'SORT_OPERATIONS': 'common.schema.sort_operations',
}

# Simple JWT settings
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(
        minutes=env("ACCESS_TOKEN_LIFETIME_MINUTES", cast=int, default=5)
    ),
    "REFRESH_TOKEN_LIFETIME": timedelta(
        days=env("REFRESH_TOKEN_LIFETIME_DAYS", cast=int, default=30)
    ),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "uuid",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(
        minutes=env("ACCESS_TOKEN_LIFETIME_MINUTES", cast=int, default=5)
    ),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(
        days=env("REFRESH_TOKEN_LIFETIME_DAYS", cast=int, default=30)
    ),
    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}

CELERY_BROKER_URL = env(
    "CELERY_BROKER_URL", cast=str, default="redis://localhost:6379/0"
)
CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND", cast=str, default="django-db")
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE  # Use Django's TIME_ZONE
CELERY_ENABLE_UTC = USE_TZ  # Use Django's USE_TZ
CELERY_BEAT_SCHEDULE = {
    "reset_daily_page_credits": {
        "task": "plan.tasks.reset_daily_page_credits",
        "schedule": crontab(hour="0", minute="1"),
    },
}
DJANGO_CELERY_RESULTS_TASK_ID_MAX_LENGTH = 191

# You are not allowed in OpenSource usage change this flag
# This is just for purchased version with a valid license
IS_ENTERPRISE_MODE_ACTIVE = env("IS_ENTERPRISE_MODE_ACTIVE", cast=bool, default=False)
FRONTEND_URL = env("FRONTEND_URL", cast=str, default="http://localhost:5173")
IS_LOGIN_ACTIVE = env("IS_LOGIN_ACTIVE", cast=bool, default=True)
IS_SIGNUP_ACTIVE = env("IS_SIGNUP_ACTIVE", cast=bool, default=True)
IS_GITHUB_LOGIN_ACTIVE = env("IS_GITHUB_LOGIN_ACTIVE", cast=bool, default=True)
IS_GOOGLE_LOGIN_ACTIVE = env("IS_GOOGLE_LOGIN_ACTIVE", cast=bool, default=True)

GOOGLE_CLIENT_ID = env("GOOGLE_CLIENT_ID", cast=str, default="")
GOOGLE_CLIENT_SECRET = env("GOOGLE_CLIENT_SECRET", cast=str, default="")

GITHUB_CLIENT_ID = env("GITHUB_CLIENT_ID", cast=str, default="")
GITHUB_CLIENT_SECRET = env("GITHUB_CLIENT_SECRET", cast=str, default="")

EMAIL_BACKEND = env(
    "EMAIL_BACKEND", cast=str, default="django.core.mail.backends.smtp.EmailBackend"
)
EMAIL_HOST = env("EMAIL_HOST", cast=str, default="")
EMAIL_PORT = env("EMAIL_PORT", cast=int, default=587)
EMAIL_USE_TLS = env("EMAIL_USE_TLS", cast=bool, default=True)
EMAIL_HOST_USER = env("EMAIL_HOST_USER", cast=str, default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", cast=str, default="")
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", cast=str, default="")

LOG_LEVEL = env("LOG_LEVEL", cast=str, default="INFO")
MINIO_ENDPOINT = env("MINIO_ENDPOINT", cast=str, default="localhost:9000")
MINIO_EXTERNAL_ENDPOINT = env(
    "MINIO_EXTERNAL_ENDPOINT", cast=str, default="localhost:9000"
)  # Default is same as MINIO_ENDPOINT
MINIO_EXTERNAL_ENDPOINT_USE_HTTPS = env(
    "MINIO_EXTERNAL_ENDPOINT_USE_HTTPS", cast=bool, default=False
)  # Default is same as MINIO_USE_HTTPS
MINIO_REGION = env("MINIO_REGION", cast=str, default=None)  # Default is set to None
MINIO_ACCESS_KEY = env("MINIO_ACCESS_KEY", cast=str, default="minio")
MINIO_SECRET_KEY = env("MINIO_SECRET_KEY", cast=str, default="minio123")
MINIO_USE_HTTPS = env("MINIO_USE_HTTPS", cast=bool, default=False)
MINIO_URL_EXPIRY_HOURS = timedelta(
    hours=env("MINIO_URL_EXPIRY_HOURS", cast=int, default=7)
)
MINIO_CONSISTENCY_CHECK_ON_START = env(
    "MINIO_CONSISTENCY_CHECK_ON_START", cast=bool, default=False
)
MINIO_PRIVATE_BUCKET = env("MINIO_PRIVATE_BUCKET", cast=str, default="private")
MINIO_PUBLIC_BUCKET = env("MINIO_PUBLIC_BUCKET", cast=str, default="public")
MINIO_PRIVATE_BUCKETS = [
    MINIO_PRIVATE_BUCKET,
]
MINIO_PUBLIC_BUCKETS = [
    MINIO_PUBLIC_BUCKET,
]

MINIO_MEDIA_FILES_BUCKET = MINIO_PRIVATE_BUCKET  # replacement for MEDIA_ROOT
MINIO_STATIC_FILES_BUCKET = MINIO_PUBLIC_BUCKET  # replacement for STATIC_ROOT
MINIO_BUCKET_CHECK_ON_SAVE = env("MINIO_BUCKET_CHECK_ON_SAVE", cast=bool, default=False)

CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[])
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=[])
CORS_ALLOWED_ORIGIN_REGEXES = env.list("CORS_ALLOWED_ORIGIN_REGEXES", default=[])
CORS_ALLOW_ALL_ORIGINS = env.bool("CORS_ALLOW_ALL_ORIGINS", default=False)
CORS_ALLOW_HEADERS = [
    *default_headers,
    "X-TEAM-ID",
]

# Plugins
WATERCRAWL_PLUGINS = env.list(
    "WATER_CRAWL_PLUGINS",
    default=[
        "watercrawl_openai.OpenAIPlugin",
    ],
)

# ML Plugins
OPENAI_API_KEY = env("OPENAI_API_KEY", cast=str, default="")

# Scrapy settings
SCRAPY_USER_AGENT = env(
    "SCRAPY_USER_AGENT",
    cast=str,
    default="WaterCrawl/0.1 (+https://github.com/watercrawl/watercrawl)",
)
SCRAPY_ROBOTSTXT_OBEY = env("SCRAPY_ROBOTSTXT_OBEY", cast=bool, default=True)
SCRAPY_CONCURRENT_REQUESTS = env("SCRAPY_CONCURRENT_REQUESTS", cast=int, default=16)
SCRAPY_DOWNLOAD_DELAY = env("SCRAPY_DOWNLOAD_DELAY", cast=float, default=0)
SCRAPY_CONCURRENT_REQUESTS_PER_DOMAIN = env(
    "SCRAPY_CONCURRENT_REQUESTS_PER_DOMAIN", cast=int, default=4
)
SCRAPY_CONCURRENT_REQUESTS_PER_IP = env(
    "SCRAPY_CONCURRENT_REQUESTS_PER_IP", cast=int, default=4
)
SCRAPY_COOKIES_ENABLED = env("SCRAPY_COOKIES_ENABLED", cast=bool, default=False)
SCRAPY_HTTPCACHE_ENABLED = env("SCRAPY_HTTPCACHE_ENABLED", cast=bool, default=True)
SCRAPY_HTTPCACHE_EXPIRATION_SECS = env(
    "SCRAPY_HTTPCACHE_EXPIRATION_SECS", cast=int, default=3600
)
SCRAPY_HTTPCACHE_DIR = env("SCRAPY_HTTPCACHE_DIR", cast=str, default="httpcache")
SCRAPY_LOG_LEVEL = env("SCRAPY_LOG_LEVEL", cast=str, default="ERROR")

PLAYWRIGHT_SERVER = env("PLAYWRIGHT_SERVER", cast=str, default=None)
PLAYWRIGHT_API_KEY = env("PLAYWRIGHT_API_KEY", cast=str, default=None)

STRIPE_SECRET_KEY = env("STRIPE_SECRET_KEY", cast=str, default="")
STRIPE_WEBHOOK_SECRET = env("STRIPE_WEBHOOK_SECRET", cast=str, default="")

MAX_CRAWL_DEPTH = env("MAX_CRAWL_DEPTH", cast=int, default=-1)

CAPTURE_USAGE_HISTORY = (
    env.bool("CAPTURE_USAGE_HISTORY", default=True) or IS_ENTERPRISE_MODE_ACTIVE
)

GOOGLE_ANALYTICS_ID = env("GOOGLE_ANALYTICS_ID", cast=str, default="")
