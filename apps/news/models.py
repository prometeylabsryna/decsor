"""NewsArticle — blog/news posts for the site."""
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class NewsArticle(models.Model):
    CATEGORY_MARKET = "market"
    CATEGORY_COMPANY = "company"
    CATEGORY_CHOICES = [
        (CATEGORY_MARKET, _("Новини ринку")),
        (CATEGORY_COMPANY, _("Новини компанії")),
    ]

    title = models.CharField("Заголовок", max_length=200)
    category = models.CharField(
        "Категорія",
        max_length=20,
        choices=CATEGORY_CHOICES,
        default=CATEGORY_MARKET,
    )
    slug = models.SlugField(
        "Slug",
        max_length=220,
        unique=True,
        blank=True,
        help_text="Заповнюється автоматично з заголовку",
    )
    excerpt = models.TextField(
        "Короткий опис",
        max_length=400,
        blank=True,
        help_text="Відображається у картці новини",
    )
    content = models.TextField("Повний текст")
    image = models.ImageField(
        "Обкладинка",
        upload_to="news/%Y/%m/",
        blank=True,
        null=True,
    )

    source_url = models.URLField(
        "Джерело (URL оригіналу)",
        max_length=500,
        blank=True,
        default="",
        help_text="Заповнюється автоматично при імпорті з RSS",
    )

    # SEO
    seo_title = models.CharField("SEO title", max_length=70, blank=True)
    seo_description = models.CharField("SEO description", max_length=160, blank=True)

    published_at = models.DateTimeField("Дата публікації", default=timezone.now)
    is_published = models.BooleanField("Опублікована", default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Новина"
        verbose_name_plural = "Новини"
        ordering = ["-published_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)
