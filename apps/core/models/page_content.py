"""PageContent — editable rich-text blocks for static informational pages.

Кожен запис відповідає одному текстовому блоку на конкретній сторінці сайту
(наприклад, вступний абзац на «Про компанію» або умови гарантійного ремонту
на «Сервіс і гарантія»). Це дозволяє редагувати весь «прозовий» контент
сторінок через TinyMCE в адмінці без втручання в шаблони.
"""
from django.db import models


class PageContent(models.Model):
    ABOUT_INTRO = "about_intro"
    COOPERATION_INTRO = "cooperation_intro"
    COOPERATION_NOTE = "cooperation_note"
    PARTNERS_INTRO = "partners_intro"
    DELIVERY_INTRO = "delivery_intro"
    DELIVERY_CONDITIONS = "delivery_conditions"
    DELIVERY_DISCOUNTS = "delivery_discounts"
    DELIVERY_ORDER_STEPS = "delivery_order_steps"
    DELIVERY_ORDER_PAYMENT = "delivery_order_payment"
    DELIVERY_TRANSPORT_INTRO = "delivery_transport_intro"
    DELIVERY_TRANSPORT_NOTE = "delivery_transport_note"
    PARTNERS_PROGRAM_INTRO = "partners_program_intro"
    PARTNERS_PROGRAM_OUTRO = "partners_program_outro"
    PARTNERS_BECOME_CONTRACT = "partners_become_contract"
    PARTNERS_BECOME_CONTRACT_FOLLOWUP = "partners_become_contract_followup"
    PARTNERS_BECOME_CAREERS = "partners_become_careers"
    PARTNERS_SERVICE_INTRO = "partners_service_intro"
    PARTNERS_SERVICE_TERMS = "partners_service_terms"
    PARTNERS_SERVICE_KIT = "partners_service_kit"

    PAGE_CHOICES = [
        (ABOUT_INTRO, "Про компанію — основний текст"),
        (COOPERATION_INTRO, "Співпраця — вступний текст"),
        (COOPERATION_NOTE, "Співпраця — примітка перед контактами"),
        (PARTNERS_INTRO, "Партнери — вступний текст"),
        (DELIVERY_INTRO, "Доставка — вступний текст"),
        (DELIVERY_CONDITIONS, "Доставка — умови співпраці"),
        (DELIVERY_DISCOUNTS, "Доставка — умови знижок"),
        (DELIVERY_ORDER_STEPS, "Замовлення та оплата — кроки замовлення"),
        (DELIVERY_ORDER_PAYMENT, "Замовлення та оплата — способи оплати"),
        (DELIVERY_TRANSPORT_INTRO, "Транспортні компанії — вступний текст"),
        (DELIVERY_TRANSPORT_NOTE, "Транспортні компанії — примітка"),
        (PARTNERS_PROGRAM_INTRO, "Партнерська програма — вступ і переваги"),
        (PARTNERS_PROGRAM_OUTRO, "Партнерська програма — заключний текст"),
        (PARTNERS_BECOME_CONTRACT, "Стати партнером — вступ перед посиланням на договір"),
        (PARTNERS_BECOME_CONTRACT_FOLLOWUP, "Стати партнером — текст після посилання на договір"),
        (PARTNERS_BECOME_CAREERS, "Стати партнером — блок про вакансії"),
        (PARTNERS_SERVICE_INTRO, "Сервіс і гарантія — вступний текст"),
        (PARTNERS_SERVICE_TERMS, "Сервіс і гарантія — умови гарантійного ремонту"),
        (PARTNERS_SERVICE_KIT, "Сервіс і гарантія — комплект поставки"),
    ]

    page = models.CharField(
        "Сторінка/блок",
        max_length=50,
        choices=PAGE_CHOICES,
        unique=True,
    )
    body = models.TextField("Текст (HTML)", blank=True)

    class Meta:
        verbose_name = "Текст сторінки"
        verbose_name_plural = "Тексти сторінок"
        ordering = ["page"]

    def __str__(self):
        return self.get_page_display()
