from .base import *

DEBUG = True
ALLOWED_HOSTS = []


# * DRF
REST_FRAMEWORK = {
    # Specifies the default authentication classes used by Django REST framework.
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ],
    # Specifies the default permission classes used by Django REST framework.
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated"
        # "rest_framework.permissions.AllowAny"
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.OrderingFilter",
    ),
}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "test_movu_app",
        "USER": config("DB_USER", default="none_var"),
        "PASSWORD": config("DB_PASSWORD", default="none_var"),
        "HOST": config("DB_HOST", default="none_var"),
        "PORT": config("DB_PORT", default="none_var"),
        "OPTIONS": {
            "options": f'-c search_path=public',
        },
    },
}