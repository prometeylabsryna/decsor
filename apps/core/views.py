"""Core views."""
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView

from apps.core.models import (
    Advantage,
    Carrier,
    CooperationBanner,
    FaqItem,
    HeroSection,
    InternalExtension,
    PartnerRegion,
    Service,
    ServiceCenter,
)
from apps.brands.models import Brand
from apps.news.models import NewsArticle


class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["hero"] = HeroSection.objects.filter(is_active=True).first()
        ctx["services"] = Service.objects.filter(is_active=True)
        ctx["advantages"] = Advantage.objects.filter(is_active=True)
        ctx["cooperations"] = CooperationBanner.objects.filter(is_active=True)
        ctx["brands"] = Brand.objects.filter(is_active=True)
        ctx["news"] = NewsArticle.objects.filter(
            is_published=True,
            category=NewsArticle.CATEGORY_COMPANY,
        ).order_by("-published_at")[:3]
        ctx["subscribed"] = self.request.GET.get("subscribed") == "1"
        return ctx

    def post(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse("core:home") + "?subscribed=1")


class AboutView(TemplateView):
    template_name = "core/about.html"


class CooperationView(TemplateView):
    template_name = "core/cooperation.html"


class FaqView(TemplateView):
    template_name = "core/faq.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["faq_items"] = FaqItem.objects.filter(is_active=True)
        return ctx


class DeliveryView(TemplateView):
    template_name = "core/delivery.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        extensions = InternalExtension.objects.filter(is_active=True)
        ctx["internal_extensions"] = extensions
        ctx["internal_extensions_joined"] = ", ".join(e.extension for e in extensions)
        return ctx


class DeliveryOrderView(TemplateView):
    template_name = "core/delivery_order.html"


class DeliveryTransportView(TemplateView):
    template_name = "core/delivery_transport.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["carriers"] = Carrier.objects.filter(is_active=True)
        return ctx


class PartnersView(TemplateView):
    template_name = "core/partners.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["internal_extensions"] = InternalExtension.objects.filter(is_active=True)
        return ctx


class PartnersProgramView(TemplateView):
    template_name = "core/partners_program.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["partner_regions"] = PartnerRegion.objects.filter(is_active=True)
        return ctx


class PartnersBecomeView(TemplateView):
    template_name = "core/partners_become.html"


class PartnersServiceView(TemplateView):
    template_name = "core/partners_service.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["service_centers"] = ServiceCenter.objects.filter(is_active=True)
        return ctx


class ContactsView(TemplateView):
    template_name = "core/contacts.html"
