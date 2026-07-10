"""Base settings for ltm.com.ua clone."""
import os
from pathlib import Path
from django.urls import reverse_lazy
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-change-me")

INSTALLED_APPS = [
    # Unfold MUST precede django.contrib.admin
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    # modeltranslation must precede django.contrib.admin and local apps
    "modeltranslation",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party
    "solo",
    "tinymce",
    # Local apps
    "apps.core",
    "apps.news",
    "apps.brands",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.template.context_processors.i18n",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.core.context_processors.site_settings",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

from config.settings.database import build_databases  # noqa: E402

DATABASES = build_databases()

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "uk"
TIME_ZONE = "Europe/Kyiv"
USE_I18N = True
USE_TZ = True

LANGUAGES = [
    ("uk", "Українська"),
    ("en", "English"),
]

LOCALE_PATHS = [BASE_DIR / "locale"]

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------------------------------------------------------------------------
# Market news RSS import (liga.net/telecom, itc.ua/mobilnaya-svyaz)
# ---------------------------------------------------------------------------
MARKET_NEWS_RSS_FEEDS = [
    "https://tech.liga.net/ua/telecom/rss.xml",
    "https://itc.ua/tag/mobilnaya-svyaz/feed/",
]
MARKET_NEWS_FETCH_TIMEOUT = int(os.getenv("MARKET_NEWS_FETCH_TIMEOUT", "30"))

# ---------------------------------------------------------------------------
# Unfold Admin Theme
# ---------------------------------------------------------------------------
UNFOLD = {
    "SITE_TITLE": "Led leader Admin",
    "SITE_HEADER": "Led leader Panel",
    "SITE_URL": "/",
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                "title": "Загальне",
                "separator": True,
                "items": [
                    {
                        "title": "Налаштування сайту",
                        "icon": "settings",
                        "link": reverse_lazy("admin:core_sitesettings_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                ],
            },
            {
                "title": "Головна сторінка",
                "separator": False,
                "items": [
                    {
                        "title": "Hero секції",
                        "icon": "view_carousel",
                        "link": reverse_lazy("admin:core_herosection_changelist"),
                    },
                    {
                        "title": "Послуги",
                        "icon": "build",
                        "link": reverse_lazy("admin:core_service_changelist"),
                    },
                    {
                        "title": "Переваги",
                        "icon": "star",
                        "link": reverse_lazy("admin:core_advantage_changelist"),
                    },
                    {
                        "title": "Банер Співпраця",
                        "icon": "handshake",
                        "link": reverse_lazy("admin:core_cooperationbanner_changelist"),
                    },
                ],
            },
            {
                "title": "Контент",
                "separator": False,
                "items": [
                    {
                        "title": "Новини",
                        "icon": "article",
                        "link": reverse_lazy("admin:news_newsarticle_changelist"),
                    },
                    {
                        "title": "Тексти сторінок",
                        "icon": "description",
                        "link": reverse_lazy("admin:core_pagecontent_changelist"),
                    },
                    {
                        "title": "F.A.Q.",
                        "icon": "help",
                        "link": reverse_lazy("admin:core_faqitem_changelist"),
                    },
                ],
            },
            {
                "title": "Доставка",
                "separator": False,
                "items": [
                    {
                        "title": "Транспортні компанії",
                        "icon": "local_shipping",
                        "link": reverse_lazy("admin:core_carrier_changelist"),
                    },
                ],
            },
            {
                "title": "Партнери",
                "separator": False,
                "items": [
                    {
                        "title": "Бренди",
                        "icon": "business",
                        "link": reverse_lazy("admin:brands_brand_changelist"),
                    },
                    {
                        "title": "Сервісні центри",
                        "icon": "build",
                        "link": reverse_lazy("admin:core_servicecenter_changelist"),
                    },
                    {
                        "title": "Регіони партнерів",
                        "icon": "map",
                        "link": reverse_lazy("admin:core_partnerregion_changelist"),
                    },
                ],
            },
            {
                "title": "Контакти",
                "separator": False,
                "items": [
                    {
                        "title": "Внутрішні номери",
                        "icon": "call",
                        "link": reverse_lazy("admin:core_internalextension_changelist"),
                    },
                ],
            },
            {
                "title": "Доступи",
                "separator": True,
                "items": [
                    {
                        "title": "Користувачі",
                        "icon": "person",
                        "link": reverse_lazy("admin:auth_user_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": "Групи",
                        "icon": "group",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                ],
            },
        ],
    },
}

# ---------------------------------------------------------------------------
# TinyMCE Rich Text Editor
# ---------------------------------------------------------------------------
TINYMCE_DEFAULT_CONFIG = {
    "height": 400,
    "width": "100%",
    "menubar": False,
    "plugins": (
        "advlist autolink lists link image charmap preview anchor "
        "searchreplace visualblocks code fullscreen insertdatetime "
        "media table paste code"
    ),
    "toolbar": (
        "undo redo | formatselect | bold italic underline strikethrough | "
        "forecolor backcolor | alignleft aligncenter alignright alignjustify | "
        "bullist numlist outdent indent | link image | code fullscreen"
    ),
    "content_style": "body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; font-size: 14px; }",
    "forced_root_block": "p",
    "branding": False,
}
