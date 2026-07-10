"""Carrier — transport/delivery companies shown on the 'Delivery' page."""
from django.db import models


class Carrier(models.Model):
    name = models.CharField("Назва компанії", max_length=100)
    logo = models.ImageField(
        "Логотип",
        upload_to="carriers/",
        blank=True,
        null=True,
        help_text=(
            "Рекомендований розмір: 160×56 px (співвідношення сторін ≈ 2.85:1). "
            "Формат SVG або PNG з прозорим фоном. Якщо логотип не завантажено — "
            "буде показано стандартну іконку."
        ),
    )
    description = models.TextField(
        "Опис",
        help_text="Короткий опис служби доставки та орієнтовні терміни доставки.",
    )
    order = models.PositiveSmallIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Активний", default=True)

    class Meta:
        verbose_name = "Транспортна компанія"
        verbose_name_plural = "Транспортні компанії"
        ordering = ["order"]

    def __str__(self):
        return self.name
