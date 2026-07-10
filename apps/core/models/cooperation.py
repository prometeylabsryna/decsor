"""CooperationBanner — the in-page wholesale CTA banner."""
from django.db import models


class CooperationBanner(models.Model):
    heading = models.CharField("Заголовок", max_length=160)
    body = models.TextField("Текст")
    cta_email = models.EmailField("Email для CTA", blank=True)
    is_active = models.BooleanField("Активний", default=True)

    class Meta:
        verbose_name = "Банер Співпраця"
        verbose_name_plural = "Банери Співпраця"

    def __str__(self):
        return self.heading
