"""Production settings (FREEhost.UA / VPS / shared hosting)."""
import os
from pathlib import Path

from .base import *  # noqa: F403

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv("ALLOWED_HOSTS", "").split(",")
    if host.strip()
]

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",")
    if origin.strip()
]

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
# VPS: False до certbot; після SSL — SECURE_SSL_REDIRECT=True у .env
SECURE_SSL_REDIRECT = not DEBUG and os.getenv("SECURE_SSL_REDIRECT", "False") == "True"
SECURE_HSTS_SECONDS = int(os.getenv("SECURE_HSTS_SECONDS", "31536000")) if not DEBUG else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = not DEBUG
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

# VPS: nginx віддає /static/ і /media/ (django-digitalocean-deploy)
# Shared FREEhost: WhiteNoise без nginx alias
NGINX_SERVE_STATIC = os.getenv("NGINX_SERVE_STATIC", "False") == "True"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

if not NGINX_SERVE_STATIC:
    MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")
    STORAGES["staticfiles"] = {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    }

# Logging → logs/ (writable on hosting)
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{asctime} {levelname} {name} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_DIR / "django.log",
            "maxBytes": 5 * 1024 * 1024,
            "backupCount": 3,
            "formatter": "verbose",
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["file", "console"],
        "level": os.getenv("LOG_LEVEL", "INFO"),
    },
    "loggers": {
        "django.request": {
            "handlers": ["file"],
            "level": "ERROR",
            "propagate": False,
        },
        "apps.news": {
            "handlers": ["file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

# Cron wget endpoint (FREEhost panel → «метод wget»)
CRON_SECRET_TOKEN = os.getenv("CRON_SECRET_TOKEN", "")
