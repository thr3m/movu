import os
from .base import *

DEBUG = True
ALLOWED_HOSTS = ["*"]

# * DRF
REST_FRAMEWORK = {
    # Specifies the default authentication classes used by Django REST framework.
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ],
    # Specifies the default permission classes used by Django REST framework.
    "DEFAULT_PERMISSION_CLASSES": [
        # "rest_framework.permissions.IsAuthenticated"
        "rest_framework.permissions.AllowAny"
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_FILTER_BACKENDS": ("rest_framework.filters.OrderingFilter",),
}

# * static
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
PATH_STATIC = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(PATH_STATIC, "staticfiles")

STATICFILES_DIRS = [PATH_STATIC]

MEDIA_ROOT = os.path.join(PATH_STATIC, "media")
MEDIA_URL = "/media/"

# *django-cors-headers
CORS_ALLOWED_ORIGINS = ["http://localhost:3000"]
CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS
CORS_ALLOW_CREDENTIALS = True

