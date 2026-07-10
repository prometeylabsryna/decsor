"""Admin for apps.core editable-content models: FaqItem, ServiceCenter,
PartnerRegion, InternalExtension, PageContent.

Винесено в окремий файл (за правилом «не більше 500 рядків на файл»),
реєстрація підхоплюється через імпорт в кінці admin.py.
"""
from django import forms
from django.contrib import admin
from django.db import models
from modeltranslation.admin import TranslationAdmin as MTTranslationAdmin
from tinymce.widgets import TinyMCE
from unfold.admin import ModelAdmin

from apps.core.models import (
    FaqItem,
    InternalExtension,
    PageContent,
    PartnerRegion,
    ServiceCenter,
)

_TINYMCE = {models.TextField: {"widget": TinyMCE()}}


@admin.register(FaqItem)
class FaqItemAdmin(MTTranslationAdmin, ModelAdmin):
    list_display = ("question", "is_active", "order")
    list_editable = ("is_active", "order")
    list_display_links = ("question",)
    search_fields = ("question", "answer")
    ordering = ("order",)
    compressed_fields = True

    fieldsets = (
        (
            None,
            {
                "fields": ("question", "answer", "order", "is_active"),
            },
        ),
    )

    formfield_overrides = _TINYMCE


@admin.register(ServiceCenter)
class ServiceCenterAdmin(MTTranslationAdmin, ModelAdmin):
    list_display = ("name", "phone", "url", "is_active", "order")
    list_editable = ("is_active", "order")
    list_display_links = ("name",)
    search_fields = ("name", "address")
    ordering = ("order",)
    compressed_fields = True

    fieldsets = (
        (
            None,
            {
                "fields": ("name", "url", "address", "phone", "order", "is_active"),
            },
        ),
    )


@admin.register(PartnerRegion)
class PartnerRegionAdmin(MTTranslationAdmin, ModelAdmin):
    list_display = ("name", "is_active", "order")
    list_editable = ("is_active", "order")
    list_display_links = ("name",)
    search_fields = ("name", "cities")
    ordering = ("order",)
    compressed_fields = True

    fieldsets = (
        (
            None,
            {
                "fields": ("name", "cities", "order", "is_active"),
            },
        ),
    )

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name in ("cities", "cities_uk", "cities_en"):
            kwargs.setdefault("widget", forms.Textarea(attrs={"rows": 6}))
        return super().formfield_for_dbfield(db_field, request, **kwargs)


@admin.register(InternalExtension)
class InternalExtensionAdmin(ModelAdmin):
    list_display = ("extension", "is_active", "order")
    list_editable = ("is_active", "order")
    list_display_links = ("extension",)
    ordering = ("order",)
    compressed_fields = True

    fieldsets = (
        (
            None,
            {
                "fields": ("extension", "order", "is_active"),
            },
        ),
    )


@admin.register(PageContent)
class PageContentAdmin(MTTranslationAdmin, ModelAdmin):
    list_display = ("page",)
    list_display_links = ("page",)
    ordering = ("page",)
    compressed_fields = True

    fieldsets = (
        (
            None,
            {
                "fields": ("page", "body"),
            },
        ),
    )

    formfield_overrides = _TINYMCE
