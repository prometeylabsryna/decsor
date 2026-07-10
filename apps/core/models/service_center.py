"""ServiceCenter — authorized warranty service centres (Партнери → Сервіс і гарантія)."""
from django.db import models


class ServiceCenter(models.Model):
    name = models.CharField("Назва", max_length=100)
    url = models.URLField("Сайт", blank=True)
    address = models.CharField("Адреса", max_length=255, blank=True)
    phone = models.CharField("Телефон", max_length=30, blank=True)
    order = models.PositiveSmallIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Активний", default=True)

    class Meta:
        verbose_name = "Сервісний центр"
        verbose_name_plural = "Сервісні центри"
        ordering = ["order"]

    def __str__(self):
        return self.name
