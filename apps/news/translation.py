"""modeltranslation registration for news models."""
from modeltranslation.translator import TranslationOptions, register

from apps.news.models import NewsArticle


@register(NewsArticle)
class NewsArticleTranslationOptions(TranslationOptions):
    fields = ("title", "excerpt", "content", "seo_title", "seo_description")
