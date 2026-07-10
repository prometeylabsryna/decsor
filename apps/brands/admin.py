"""Admin for apps.brands: Brand."""
from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from apps.brands.models import Brand


@admin.register(Brand)
class BrandAdmin(ModelAdmin):
    list_display = ("name", "logo_preview", "url", "is_active", "order")
    list_editable = ("is_active", "order")
    list_display_links = ("name",)
    search_fields = ("name",)
    ordering = ("order", "name")
    compressed_fields = True

    fieldsets = (
        (
            None,
            {
                "fields": ("name", "logo", "url", "order", "is_active"),
            },
        ),
    )

    @admin.display(description="Логотип")
    def logo_preview(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" style="height:36px;object-fit:contain;" />',
                obj.logo.url,
            )
        return "—"
