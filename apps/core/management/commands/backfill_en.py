"""Fill empty English (_en) fields for modeltranslation content."""
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Заповнює порожні англійські поля (_en) для контенту з БД (без новин)"

    def handle(self, *args, **options):
        from apps.core.models import (
            Advantage,
            CooperationBanner,
            HeroSection,
            Service,
            SiteSettings,
        )

        updated = 0

        settings = SiteSettings.get_solo()
        patches = {
            "description_en": (
                "Led leader — Digital Equipment has been on the mobile communications market "
                "since 2006. Wholesale sales of digital goods from verified manufacturers."
            ),
            "seo_title_en": "Led leader Digital Equipment — wholesale digital equipment",
            "seo_description_en": (
                "Led leader — wholesale distributor of digital equipment since 2006. "
                "Delivery across Ukraine. Quality guarantee."
            ),
        }
        for field, value in patches.items():
            current = getattr(settings, field, None) or ""
            if not str(current).strip():
                setattr(settings, field, value)
                updated += 1
        if updated:
            settings.save()
            self.stdout.write(f"  ✓ SiteSettings ({updated} fields)")

        model_defaults = [
            (
                HeroSection,
                "order",
                {
                    "title_en": "LED LEADER — DIGITAL EQUIPMENT",
                    "subtitle_en": "On the mobile communications market since 2006",
                    "body_en": (
                        "Through years of dedicated work the company has set clear priorities "
                        "that are an integral part of its operations."
                    ),
                    "cta_text_en": "Get in touch",
                },
            ),
            (
                Service,
                "icon",
                {
                    "handshake": {
                        "title_en": "Cooperation",
                        "description_en": (
                            "Led leader is open to mutually beneficial cooperation with both "
                            "customers and suppliers of any digital equipment."
                        ),
                    },
                    "truck": {
                        "title_en": "Product delivery",
                        "description_en": (
                            "Led leader delivers orders via the carrier or courier service "
                            "of the customer's choice across Ukraine."
                        ),
                    },
                    "shield-check": {
                        "title_en": "Quality guarantee",
                        "description_en": (
                            "The quality of products supplied by Led leader is confirmed by "
                            "all required manufacturer certificates."
                        ),
                    },
                    "wrench": {
                        "title_en": "Reliable service",
                        "description_en": (
                            "Led leader service centre provides warranty for the full range "
                            "of digital equipment supplied to the customer."
                        ),
                    },
                },
            ),
            (
                Advantage,
                "icon",
                {
                    "star": {"title_en": "Only quality products"},
                    "tag": {"title_en": "Reasonable pricing policy"},
                    "globe": {"title_en": "Work with global brands"},
                    "heart": {"title_en": "We value our customers"},
                },
            ),
        ]

        for hero in HeroSection.objects.all():
            count = self._fill_empty(hero, model_defaults[0][2])
            if count:
                hero.save()
                self.stdout.write(f"  ✓ HeroSection #{hero.pk} ({count} fields)")

        for service in Service.objects.all():
            defaults = model_defaults[1][2].get(service.icon, {})
            count = self._fill_empty(service, defaults)
            if count:
                service.save()
                self.stdout.write(f"  ✓ Service {service.icon} ({count} fields)")

        for advantage in Advantage.objects.all():
            defaults = model_defaults[2][2].get(advantage.icon, {})
            count = self._fill_empty(advantage, defaults)
            if count:
                advantage.save()
                self.stdout.write(f"  ✓ Advantage {advantage.icon} ({count} fields)")

        for banner in CooperationBanner.objects.all():
            count = self._fill_empty(
                banner,
                {
                    "heading_en": "Within wholesale purchasing and cooperation",
                    "body_en": (
                        "If you have a cooperation proposal for our company — drop us an "
                        "email, and our manager will get back to you shortly."
                    ),
                },
            )
            if count:
                banner.save()
                self.stdout.write(f"  ✓ CooperationBanner #{banner.pk} ({count} fields)")

        self.stdout.write(self.style.SUCCESS("✓ Backfill EN завершено"))

    @staticmethod
    def _fill_empty(obj, field_values: dict) -> int:
        updated = 0
        for field, value in field_values.items():
            current = getattr(obj, field, None) or ""
            if not str(current).strip():
                setattr(obj, field, value)
                updated += 1
        return updated
