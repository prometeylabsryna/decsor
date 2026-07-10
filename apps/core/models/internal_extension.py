"""InternalExtension — internal phone extension numbers of the sales/partner line."""
from django.db import models


class InternalExtension(models.Model):
    extension = models.CharField("Внутрішній номер", max_length=20)
    order = models.PositiveSmallIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Активний", default=True)

    class Meta:
        verbose_name = "Внутрішній номер телефону"
        verbose_name_plural = "Внутрішні номери телефону"
        ordering = ["order"]

    def __str__(self):
        return self.extension
