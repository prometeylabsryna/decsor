"""PartnerRegion — regions/cities where the company has partners (Партнерська програма)."""
from django.db import models


class PartnerRegion(models.Model):
    name = models.CharField("Назва області/регіону", max_length=120)
    cities = models.TextField(
        "Міста",
        blank=True,
        help_text="Кожне місто — з нового рядка.",
    )
    order = models.PositiveSmallIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Активний", default=True)

    class Meta:
        verbose_name = "Регіон партнерів"
        verbose_name_plural = "Регіони партнерів"
        ordering = ["order"]

    def __str__(self):
        return self.name
