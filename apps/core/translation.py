"""modeltranslation registration for core models."""
from modeltranslation.translator import TranslationOptions, register

from apps.core.models import (
    Advantage,
    Carrier,
    CooperationBanner,
    FaqItem,
    HeroSection,
    PageContent,
    PartnerRegion,
    Service,
    ServiceCenter,
    SiteSettings,
)


@register(HeroSection)
class HeroSectionTranslationOptions(TranslationOptions):
    fields = ("title", "subtitle", "body", "cta_text")


@register(Service)
class ServiceTranslationOptions(TranslationOptions):
    fields = ("title", "description")


@register(Advantage)
class AdvantageTranslationOptions(TranslationOptions):
    fields = ("title",)


@register(CooperationBanner)
class CooperationBannerTranslationOptions(TranslationOptions):
    fields = ("heading", "body")


@register(SiteSettings)
class SiteSettingsTranslationOptions(TranslationOptions):
    fields = (
        "site_name",
        "tagline",
        "description",
        "seo_title",
        "seo_description",
        "hours_sunday",
    )


@register(Carrier)
class CarrierTranslationOptions(TranslationOptions):
    fields = ("name", "description")


@register(FaqItem)
class FaqItemTranslationOptions(TranslationOptions):
    fields = ("question", "answer")


@register(ServiceCenter)
class ServiceCenterTranslationOptions(TranslationOptions):
    fields = ("name", "address")


@register(PartnerRegion)
class PartnerRegionTranslationOptions(TranslationOptions):
    fields = ("name", "cities")


@register(PageContent)
class PageContentTranslationOptions(TranslationOptions):
    fields = ("body",)
