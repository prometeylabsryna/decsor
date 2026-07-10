"""Service — cards in the 'Cooperation / Delivery / Quality' section."""
from django.db import models


class Service(models.Model):
    icon = models.CharField(
        "Іконка (CSS клас або SVG назва)",
        max_length=60,
        blank=True,
        help_text="Наприклад: icon-cooperation або handshake",
    )
    title = models.CharField("Назва", max_length=100)
    description = models.TextField("Опис")
    order = models.PositiveSmallIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Активний", default=True)

    class Meta:
        verbose_name = "Послуга"
        verbose_name_plural = "Послуги"
        ordering = ["order"]

    def __str__(self):
        return self.title
