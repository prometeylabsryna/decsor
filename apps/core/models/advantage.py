"""Advantage — bullets in the 'Why work with us' section."""
from django.db import models


class Advantage(models.Model):
    icon = models.CharField(
        "Іконка",
        max_length=60,
        blank=True,
        help_text="CSS клас або ідентифікатор SVG",
    )
    title = models.CharField("Перевага", max_length=120)
    order = models.PositiveSmallIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Активний", default=True)

    class Meta:
        verbose_name = "Перевага"
        verbose_name_plural = "Переваги"
        ordering = ["order"]

    def __str__(self):
        return self.title
