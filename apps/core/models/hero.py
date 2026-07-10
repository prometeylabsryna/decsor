"""HeroSection — banner model for the main page."""
from django.db import models


class HeroSection(models.Model):
    title = models.CharField("Заголовок", max_length=120)
    subtitle = models.CharField("Підзаголовок", max_length=255, blank=True)
    body = models.TextField("Текст", blank=True)
    cta_text = models.CharField("Текст кнопки CTA", max_length=60, blank=True)
    cta_url = models.CharField("URL кнопки CTA", max_length=255, blank=True)
    background_image = models.ImageField(
        "Фонове зображення",
        upload_to="hero/",
        blank=True,
        null=True,
    )
    is_active = models.BooleanField("Активний", default=True)
    order = models.PositiveSmallIntegerField("Порядок", default=0)

    class Meta:
        verbose_name = "Секція Hero"
        verbose_name_plural = "Секції Hero"
        ordering = ["order"]

    def __str__(self):
        return self.title
