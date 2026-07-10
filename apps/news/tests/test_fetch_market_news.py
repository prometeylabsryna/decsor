from io import StringIO
from unittest.mock import MagicMock, patch

from django.core.management import call_command
from django.test import TestCase, override_settings

from apps.news.management.commands.fetch_market_news import import_feed
from apps.news.models import NewsArticle


SAMPLE_FEED = {
    "entries": [
        {
            "title": "Тестова новина ринку",
            "link": "https://itc.ua/news/test-market-news-item/",
            "summary": "<p>Короткий опис тестової новини.</p>",
            "published_parsed": (2026, 3, 1, 12, 0, 0, 0, 0, 0),
        }
    ],
    "bozo": 0,
    "bozo_exception": None,
}


@override_settings(
    MARKET_NEWS_RSS_FEEDS=[
        "https://example.com/feed-a/",
        "https://example.com/feed-b/",
    ]
)
class FetchMarketNewsCommandTest(TestCase):
    @patch("apps.news.management.commands.fetch_market_news._fetch_feed")
    def test_imports_new_article(self, mock_fetch):
        mock_fetch.return_value = MagicMock(**SAMPLE_FEED)

        call_command("fetch_market_news", stdout=StringIO())

        article = NewsArticle.objects.get(source_url=SAMPLE_FEED["entries"][0]["link"])
        self.assertEqual(article.category, NewsArticle.CATEGORY_MARKET)
        self.assertTrue(article.is_published)
        self.assertEqual(article.title_uk, "Тестова новина ринку")

    @patch("apps.news.management.commands.fetch_market_news._fetch_feed")
    def test_dry_run_does_not_create_articles(self, mock_fetch):
        mock_fetch.return_value = MagicMock(**SAMPLE_FEED)

        call_command("fetch_market_news", dry_run=True, stdout=StringIO())

        self.assertEqual(NewsArticle.objects.count(), 0)

    @patch("apps.news.management.commands.fetch_market_news._fetch_feed")
    def test_skips_duplicate_source_url(self, mock_fetch):
        NewsArticle.objects.create(
            title_uk="Існуюча",
            slug="isnuvala",
            category=NewsArticle.CATEGORY_MARKET,
            excerpt_uk="Опис",
            content_uk="Контент",
            source_url=SAMPLE_FEED["entries"][0]["link"],
            is_published=True,
        )
        mock_fetch.return_value = MagicMock(**SAMPLE_FEED)

        call_command("fetch_market_news", stdout=StringIO())

        self.assertEqual(NewsArticle.objects.count(), 1)

    @patch("apps.news.management.commands.fetch_market_news._fetch_feed")
    def test_exits_when_all_feeds_fail(self, mock_fetch):
        mock_fetch.side_effect = TimeoutError("network down")

        with self.assertRaises(SystemExit) as ctx:
            call_command("fetch_market_news", stdout=StringIO())

        self.assertEqual(ctx.exception.code, 1)


class ImportFeedTest(TestCase):
    @patch("apps.news.management.commands.fetch_market_news._fetch_feed")
    def test_import_feed_returns_count(self, mock_fetch):
        mock_fetch.return_value = MagicMock(**SAMPLE_FEED)

        count = import_feed("https://example.com/feed/", dry_run=True)

        self.assertEqual(count, 1)
        self.assertEqual(NewsArticle.objects.count(), 0)
