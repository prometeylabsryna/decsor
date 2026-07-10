"""HTTP cron endpoints for FREEhost panel (wget method)."""
import logging
import os

from django.conf import settings
from django.core.management import call_command
from django.http import HttpResponse, HttpResponseForbidden

logger = logging.getLogger(__name__)


def fetch_market_news_cron(request):
    """
    Імпорт новин ринку через HTTP (панель FREEhost → Cron → wget).

    URL: /cron/fetch-market-news/?token=CRON_SECRET_TOKEN
    """
    token = getattr(settings, "CRON_SECRET_TOKEN", "") or os.getenv("CRON_SECRET_TOKEN", "")
    if not token or request.GET.get("token") != token:
        return HttpResponseForbidden("Forbidden")

    try:
        call_command("fetch_market_news")
    except Exception:
        logger.exception("cron fetch_market_news failed")
        return HttpResponse("ERROR", status=500)

    return HttpResponse("OK")
