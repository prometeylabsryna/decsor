"""Brand — partner/manufacturer brands displayed on the homepage."""
from django.db import models


class Brand(models.Model):
    name = models.CharField("Назва бренду", max_length=100)
    logo = models.ImageField(
        "Логотип",
        upload_to="brands/",
        blank=True,
        null=True,
    )
    url = models.URLField("Сайт бренду", blank=True)
    order = models.PositiveSmallIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Активний", default=True)

    class Meta:
        verbose_name = "Бренд"
        verbose_name_plural = "Бренди"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name
