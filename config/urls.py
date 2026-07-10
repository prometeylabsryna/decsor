"""URL configuration."""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from django.urls import include, path
from django.conf.urls.i18n import i18n_patterns

from apps.core.views_cron import fetch_market_news_cron


def healthz(_request):
    return HttpResponse("ok", content_type="text/plain")


urlpatterns = [
    path("healthz/", healthz, name="healthz"),
    path("admin/", admin.site.urls),
    path("cron/fetch-market-news/", fetch_market_news_cron, name="cron-fetch-market-news"),
]

urlpatterns += i18n_patterns(
    path("novyny/", include("apps.news.urls")),
    path("", include("apps.core.urls")),
    prefix_default_language=False,
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
