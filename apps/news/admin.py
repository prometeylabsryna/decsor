"""Admin for apps.news: NewsArticle."""
from io import StringIO

from django.contrib import admin, messages
from django.core.management import call_command
from django.utils.html import format_html
from modeltranslation.admin import TranslationAdmin as MTTranslationAdmin
from tinymce.widgets import TinyMCE
from unfold.admin import ModelAdmin

from apps.news.models import NewsArticle


@admin.action(description="Імпортувати новини з RSS (liga.net/telecom, itc.ua)")
def fetch_market_news_action(modeladmin, request, queryset):
    out = StringIO()
    try:
        call_command("fetch_market_news", stdout=out)
        result = out.getvalue().strip().replace("\n", " | ")
        messages.success(request, result or "Імпорт завершено.")
    except Exception as exc:  # noqa: BLE001
        messages.error(request, f"Помилка імпорту: {exc}")


@admin.register(NewsArticle)
class NewsArticleAdmin(MTTranslationAdmin, ModelAdmin):
    list_display = (
        "title",
        "category",
        "is_published",
        "published_at",
        "image_preview",
        "updated_at",
    )
    list_editable = ("is_published",)
    list_display_links = ("title",)
    list_filter = ("is_published", "category", "published_at")
    search_fields = ("title", "excerpt", "content")
    prepopulated_fields = {"slug": ("title_uk",)}
    readonly_fields = ("created_at", "updated_at", "source_url")
    date_hierarchy = "published_at"
    ordering = ("-published_at",)
    compressed_fields = True
    actions = [fetch_market_news_action]

    fieldsets = (
        (
            "Контент",
            {
                "fields": (
                    "title",
                    "slug",
                    "category",
                    "excerpt",
                    "content",
                    "image",
                ),
            },
        ),
        (
            "Публікація",
            {
                "fields": ("is_published", "published_at"),
            },
        ),
        (
            "Джерело",
            {
                "fields": ("source_url",),
                "classes": ["collapse"],
            },
        ),
        (
            "SEO",
            {
                "fields": ("seo_title", "seo_description"),
                "classes": ["collapse"],
            },
        ),
        (
            "Мета",
            {
                "fields": ("created_at", "updated_at"),
                "classes": ["collapse"],
            },
        ),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        for lang in ("uk", "en"):
            field_name = f"content_{lang}"
            if field_name in form.base_fields:
                form.base_fields[field_name].widget = TinyMCE()
        return form

    @admin.display(description="Фото")
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:40px;border-radius:4px;" />',
                obj.image.url,
            )
        return "—"
