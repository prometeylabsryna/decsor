"""Admin for apps.core: SiteSettings, HeroSection, Service, Advantage, CooperationBanner."""
from django import forms
from django.contrib import admin
from django.db import models
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html
from modeltranslation.admin import TranslationAdmin as MTTranslationAdmin
from tinymce.widgets import TinyMCE
from unfold.admin import ModelAdmin

from apps.core.models import (
    Advantage,
    Carrier,
    CooperationBanner,
    HeroSection,
    Service,
    SiteSettings,
)

_TINYMCE = {models.TextField: {"widget": TinyMCE()}}

# Реєстрація адмінки для FaqItem, ServiceCenter, PartnerRegion,
# InternalExtension, PageContent (винесено в окремий файл).
from apps.core import admin_content  # noqa: E402,F401


@admin.register(SiteSettings)
class SiteSettingsAdmin(MTTranslationAdmin, ModelAdmin):
    """Singleton — завжди редірект на єдиний об'єкт, без «Додати» та «Видалити»."""

    compressed_fields = True

    fieldsets = (
        (
            "Загальна інформація",
            {
                "fields": (
                    "site_name",
                    "tagline",
                    "description",
                    "founded_year",
                ),
            },
        ),
        (
            "Брендинг",
            {
                "fields": ("logo", "favicon"),
            },
        ),
        (
            "Документи (сторінка «Партнери»)",
            {
                "fields": ("partner_contract_file", "warranty_act_file"),
                "description": (
                    "Завантажте файли договору та гарантійного акту — вони одразу "
                    "з'являться для скачування на сайті замість поточних."
                ),
            },
        ),
        (
            "Контакти",
            {
                "fields": (
                    "email",
                    "phone",
                    "address",
                    "email_partner",
                    "email_advertising",
                    "email_sales",
                    "email_manager_1",
                    "email_manager_2",
                    "email_hr",
                ),
            },
        ),
        (
            "Графік роботи",
            {
                "fields": ("hours_weekdays", "hours_saturday", "hours_sunday"),
                "description": (
                    "Відображається на сторінках «Контакти» та «Співпраця»."
                ),
            },
        ),
        (
            "Соціальні мережі",
            {
                "fields": ("facebook_url", "instagram_url", "telegram_url"),
                "classes": ["collapse"],
            },
        ),
        (
            "Карта (сторінки «Партнери» та «Співпраця»)",
            {
                "fields": ("map_embed_code",),
                "description": (
                    "Відкрийте Google Maps → знайдіть потрібне місце (напр. Київ) → "
                    "«Поділитися» → вкладка «Вставити карту» → «Копіювати HTML» "
                    "і вставте весь код нижче."
                ),
            },
        ),
        (
            "SEO",
            {
                "fields": ("seo_title", "seo_description", "og_image"),
                "classes": ["collapse"],
            },
        ),
    )

    formfield_overrides = {
        models.TextField: {"widget": TinyMCE()},
    }

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        # map_embed_code містить сирий HTML <iframe> — TinyMCE його б понівечив,
        # тож для цього поля примусово повертаємо звичайну textarea.
        if db_field.name == "map_embed_code":
            kwargs["widget"] = forms.Textarea(attrs={"rows": 8, "style": "font-family: monospace;"})
            return db_field.formfield(**kwargs)
        return super().formfield_for_dbfield(db_field, request, **kwargs)

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj = SiteSettings.get_solo()
        url = reverse(
            "admin:core_sitesettings_change",
            args=[obj.pk],
        )
        return HttpResponseRedirect(url)


@admin.register(HeroSection)
class HeroSectionAdmin(MTTranslationAdmin, ModelAdmin):
    list_display = ("title", "is_active", "order", "image_preview")
    list_editable = ("is_active", "order")
    list_display_links = ("title",)
    search_fields = ("title", "subtitle")
    ordering = ("order",)
    compressed_fields = True

    fieldsets = (
        (
            "Контент",
            {
                "fields": (
                    "title",
                    "subtitle",
                    "body",
                    "cta_text",
                    "cta_url",
                ),
            },
        ),
        (
            "Медіа та відображення",
            {
                "fields": ("background_image", "is_active", "order"),
            },
        ),
    )

    formfield_overrides = _TINYMCE

    @admin.display(description="Превью")
    def image_preview(self, obj):
        if obj.background_image:
            return format_html(
                '<img src="{}" style="height:40px;border-radius:4px;" />',
                obj.background_image.url,
            )
        return "—"


@admin.register(Service)
class ServiceAdmin(MTTranslationAdmin, ModelAdmin):
    list_display = ("title", "icon", "is_active", "order")
    list_editable = ("is_active", "order")
    list_display_links = ("title",)
    search_fields = ("title",)
    ordering = ("order",)
    compressed_fields = True

    fieldsets = (
        (
            None,
            {
                "fields": ("icon", "title", "description", "order", "is_active"),
            },
        ),
    )

    formfield_overrides = _TINYMCE


@admin.register(Advantage)
class AdvantageAdmin(MTTranslationAdmin, ModelAdmin):
    list_display = ("title", "icon", "is_active", "order")
    list_editable = ("is_active", "order")
    list_display_links = ("title",)
    ordering = ("order",)
    compressed_fields = True

    fieldsets = (
        (
            None,
            {
                "fields": ("icon", "title", "order", "is_active"),
            },
        ),
    )


@admin.register(Carrier)
class CarrierAdmin(MTTranslationAdmin, ModelAdmin):
    list_display = ("name", "logo_preview", "is_active", "order")
    list_editable = ("is_active", "order")
    list_display_links = ("name",)
    search_fields = ("name",)
    ordering = ("order",)
    compressed_fields = True

    fieldsets = (
        (
            None,
            {
                "fields": ("name", "logo", "description", "order", "is_active"),
            },
        ),
    )

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name in ("description", "description_uk", "description_en"):
            kwargs.setdefault("widget", forms.Textarea(attrs={"rows": 3}))
        return super().formfield_for_dbfield(db_field, request, **kwargs)

    @admin.display(description="Логотип")
    def logo_preview(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" style="height:36px;object-fit:contain;" />',
                obj.logo.url,
            )
        return "—"


@admin.register(CooperationBanner)
class CooperationBannerAdmin(MTTranslationAdmin, ModelAdmin):
    list_display = ("heading", "cta_email", "is_active")
    list_editable = ("is_active",)
    list_display_links = ("heading",)
    compressed_fields = True

    fieldsets = (
        (
            None,
            {
                "fields": ("heading", "body", "cta_email", "is_active"),
            },
        ),
    )

    formfield_overrides = _TINYMCE
