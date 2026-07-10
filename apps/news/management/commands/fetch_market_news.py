"""Import market news from external RSS feeds into NewsArticle (category=market)."""
import calendar
import hashlib
import html
import logging
import re
import urllib.error
import urllib.request
from datetime import datetime, timezone as dt_timezone

import feedparser
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify

from apps.news.models import NewsArticle

logger = logging.getLogger(__name__)

MAX_EXCERPT = 400
MAX_SLUG_BASE = 200
_TAG_RE = re.compile(r"<[^>]+>")


def _clean_text(text: str) -> str:
    """Strip HTML tags and unescape HTML entities."""
    return html.unescape(_TAG_RE.sub("", text)).strip()


def _unique_slug(base: str) -> str:
    """Return a slug derived from *base* that doesn't collide with existing rows."""
    candidate = base[:MAX_SLUG_BASE]
    if not NewsArticle.objects.filter(slug=candidate).exists():
        return candidate
    suffix = hashlib.md5(base.encode()).hexdigest()[:8]
    return f"{base[:MAX_SLUG_BASE - 9]}-{suffix}"


def _parse_published(entry) -> datetime:
    """Return an aware datetime from the feed entry, falling back to now()."""
    struct = getattr(entry, "published_parsed", None) or getattr(
        entry, "updated_parsed", None
    )
    if struct:
        dt = datetime.fromtimestamp(calendar.timegm(struct), tz=dt_timezone.utc)
        return dt
    return timezone.now()


def _fetch_feed(feed_url: str) -> feedparser.FeedParserDict:
    """Download and parse an RSS feed with a network timeout."""
    timeout = getattr(settings, "MARKET_NEWS_FETCH_TIMEOUT", 30)
    request = urllib.request.Request(
        feed_url,
        headers={"User-Agent": "LedLeaderNewsBot/1.0 (+https://ltm.com.ua)"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return feedparser.parse(response.read())


def import_feed(
    feed_url: str,
    *,
    dry_run: bool = False,
    stdout=None,
) -> int:
    """Import new entries from a single RSS feed. Returns count of new items."""
    style = getattr(stdout, "style", None) if stdout is not None else None
    write = stdout.write if stdout is not None else print

    write(f"  Завантаження: {feed_url}")
    logger.info("job=fetch_market_news feed=%s status=fetching", feed_url)

    try:
        parsed = _fetch_feed(feed_url)
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        logger.error(
            "job=fetch_market_news feed=%s status=network_error error=%s",
            feed_url,
            exc,
        )
        if style:
            write(style.WARNING(f"  ⚠ Помилка мережі: {feed_url} — {exc}"))
        else:
            write(f"  ⚠ Помилка мережі: {feed_url} — {exc}")
        raise

    if parsed.bozo and not parsed.entries:
        logger.warning(
            "job=fetch_market_news feed=%s status=parse_error bozo=%s",
            feed_url,
            parsed.bozo_exception,
        )
        if style:
            write(style.WARNING(f"  ⚠ Не вдалося розібрати стрічку: {feed_url}"))
        else:
            write(f"  ⚠ Не вдалося розібрати стрічку: {feed_url}")
        raise ValueError(f"Invalid RSS feed: {feed_url}")

    feed_new = 0
    for entry in parsed.entries:
        url: str = entry.get("link", "").strip()
        if not url:
            continue

        if NewsArticle.objects.filter(source_url=url).exists():
            continue

        title: str = _clean_text(entry.get("title", ""))
        if not title:
            continue

        raw_desc: str = entry.get("summary", entry.get("description", ""))
        clean_desc = _clean_text(raw_desc)
        excerpt = clean_desc[:MAX_EXCERPT]
        published_at = _parse_published(entry)
        base_slug = slugify(title, allow_unicode=True)
        slug = _unique_slug(base_slug)

        if dry_run:
            write(f"    [dry-run] {title[:80]}")
            feed_new += 1
            continue

        NewsArticle.objects.create(
            title_uk=title,
            slug=slug,
            category=NewsArticle.CATEGORY_MARKET,
            excerpt_uk=excerpt,
            content_uk=clean_desc,
            source_url=url,
            published_at=published_at,
            is_published=True,
        )
        feed_new += 1

    label = "[dry-run] " if dry_run else ""
    success_msg = f"  {label}✓ {feed_new} нових записів з {feed_url}"
    if style:
        write(style.SUCCESS(success_msg))
    else:
        write(success_msg)

    logger.info(
        "job=fetch_market_news feed=%s status=done items_processed=%d dry_run=%s",
        feed_url,
        feed_new,
        dry_run,
    )
    return feed_new


class Command(BaseCommand):
    help = "Імпортує новини ринку з RSS-стрічок liga.net/telecom та itc.ua"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Показати що буде імпортовано, без запису в БД",
        )

    def handle(self, *args, **options):
        dry_run: bool = options["dry_run"]
        feeds = getattr(settings, "MARKET_NEWS_RSS_FEEDS", [])

        logger.info("job=fetch_market_news status=start dry_run=%s feeds=%d", dry_run, len(feeds))

        if not feeds:
            logger.error("job=fetch_market_news status=error reason=no_feeds_configured")
            self.stderr.write(self.style.ERROR("MARKET_NEWS_RSS_FEEDS не налаштовано."))
            raise SystemExit(1)

        total_new = 0
        failed_feeds = 0

        for feed_url in feeds:
            try:
                total_new += import_feed(feed_url, dry_run=dry_run, stdout=self.stdout)
            except (urllib.error.URLError, TimeoutError, OSError, ValueError):
                failed_feeds += 1

        if failed_feeds == len(feeds):
            logger.error(
                "job=fetch_market_news status=error reason=all_feeds_failed failed=%d",
                failed_feeds,
            )
            self.stderr.write(self.style.ERROR("Жодна RSS-стрічка не оброблена успішно."))
            raise SystemExit(1)

        logger.info(
            "job=fetch_market_news status=done items_processed=%d failed_feeds=%d",
            total_new,
            failed_feeds,
        )
        self.stdout.write(
            self.style.SUCCESS(f"Імпорт завершено. Всього нових: {total_new}")
        )

        if failed_feeds:
            self.stderr.write(
                self.style.WARNING(
                    f"Увага: {failed_feeds} стрічок не вдалося обробити."
                )
            )
