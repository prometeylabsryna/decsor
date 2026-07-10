"""Seed FaqItem, ServiceCenter, PartnerRegion, InternalExtension та PageContent
даними, перенесеними з хардкоджених текстів шаблонів (uk + en).

Дані (великі uk/en тексти) винесено у файли `_seed_data_1.py`, `_seed_data_2.py`
та `_seed_data_3.py` — щоб цей файл-команда лишався компактним.

Ідемпотентна команда: безпечно запускати повторно (update_or_create).
"""
from django.core.management.base import BaseCommand
from django.urls import reverse

from apps.core.management.commands._seed_data_1 import (
    get_faq_items,
    get_partner_regions,
    get_service_centers,
)
from apps.core.management.commands._seed_data_2 import get_page_content_part1
from apps.core.management.commands._seed_data_3 import get_page_content_part2


class Command(BaseCommand):
    help = "Заповнює редаговані текстові блоки (FAQ, сервіс-центри, регіони, тексти сторінок)"

    def handle(self, *args, **options):
        self._seed_hours()
        self._seed_internal_extensions()
        self._seed_faq()
        self._seed_service_centers()
        self._seed_partner_regions()
        self._seed_page_content()
        self.stdout.write(self.style.SUCCESS("✓ Редагований контент заповнено успішно"))

    # ------------------------------------------------------------------
    def _seed_hours(self):
        from apps.core.models import SiteSettings

        settings = SiteSettings.get_solo()
        settings.hours_sunday_uk = "вихідний"
        settings.hours_sunday_en = "closed"
        settings.hours_sunday = settings.hours_sunday_uk
        settings.save()
        self.stdout.write("  ✓ Графік роботи (SiteSettings)")

    # ------------------------------------------------------------------
    def _seed_internal_extensions(self):
        from apps.core.models import InternalExtension

        for order, ext in enumerate(["15", "17", "46", "50", "94"]):
            InternalExtension.objects.get_or_create(
                extension=ext,
                defaults={"order": order, "is_active": True},
            )
        self.stdout.write("  ✓ Внутрішні номери телефону")

    # ------------------------------------------------------------------
    def _seed_faq(self):
        from apps.core.models import FaqItem

        items = get_faq_items(
            delivery_order_url=reverse("core:delivery-order"),
            delivery_url=reverse("core:delivery"),
            partners_service_url=reverse("core:partners-service"),
        )

        for order, data in enumerate(items):
            obj, _ = FaqItem.objects.update_or_create(
                question_uk=data["question_uk"],
                defaults={**data, "order": order, "is_active": True},
            )
            obj.question = obj.question_uk
            obj.answer = obj.answer_uk
            obj.save(update_fields=["question", "answer"])
        self.stdout.write(f"  ✓ FaqItem ({len(items)})")

    # ------------------------------------------------------------------
    def _seed_service_centers(self):
        from apps.core.models import ServiceCenter

        centers = get_service_centers()
        for data in centers:
            obj, _ = ServiceCenter.objects.update_or_create(
                name_uk=data["name_uk"],
                defaults={**data, "is_active": True},
            )
            obj.name = obj.name_uk
            obj.address = obj.address_uk
            obj.save(update_fields=["name", "address"])
        self.stdout.write(f"  ✓ ServiceCenter ({len(centers)})")

    # ------------------------------------------------------------------
    def _seed_partner_regions(self):
        from apps.core.models import PartnerRegion

        regions = get_partner_regions()
        for order, (name_uk, name_en, cities_uk, cities_en) in enumerate(regions):
            obj, _ = PartnerRegion.objects.update_or_create(
                name_uk=name_uk,
                defaults={
                    "name_uk": name_uk,
                    "name_en": name_en,
                    "cities_uk": "\n".join(cities_uk),
                    "cities_en": "\n".join(cities_en),
                    "order": order,
                    "is_active": True,
                },
            )
            obj.name = obj.name_uk
            obj.cities = obj.cities_uk
            obj.save(update_fields=["name", "cities"])
        self.stdout.write(f"  ✓ PartnerRegion ({len(regions)})")

    # ------------------------------------------------------------------
    def _seed_page_content(self):
        from apps.core.models import PageContent, SiteSettings

        settings = SiteSettings.get_solo()
        email = settings.email or "info@ltm.com.ua"
        email_sales = settings.email_sales or "sales@ltm.com.ua"
        email_partner = settings.email_partner or "partner@ltm.com.ua"
        email_hr = settings.email_hr or "hr-manager@ltm.com.ua"
        delivery_transport_url = reverse("core:delivery-transport")

        blocks = {
            **get_page_content_part1(
                email=email,
                email_sales=email_sales,
                delivery_transport_url=delivery_transport_url,
            ),
            **get_page_content_part2(
                email_partner=email_partner,
                email_hr=email_hr,
            ),
        }

        for page, texts in blocks.items():
            obj, _ = PageContent.objects.update_or_create(
                page=page,
                defaults={"body_uk": texts["uk"], "body_en": texts["en"]},
            )
            obj.body = obj.body_uk
            obj.save(update_fields=["body"])
        self.stdout.write(f"  ✓ PageContent ({len(blocks)})")
