"""SiteSettings — singleton model for global site configuration."""
from django.db import models
from solo.models import SingletonModel


class SiteSettings(SingletonModel):
    site_name = models.CharField("Назва сайту", max_length=120, default="Led leader")
    tagline = models.CharField("Слоган", max_length=255, default="Digital Equipment")
    description = models.TextField(
        "Короткий опис компанії",
        default="",
        blank=True,
    )
    founded_year = models.PositiveSmallIntegerField("Рік заснування", default=2006)

    # Contacts
    email = models.EmailField("Основний email (info@)", blank=True)
    phone = models.CharField("Телефон (багатоканальний)", max_length=30, blank=True)
    address = models.CharField("Адреса", max_length=255, blank=True)
    email_partner = models.EmailField("Email партнерства (partner@)", blank=True)
    email_advertising = models.EmailField("Email реклами (reklama@)", blank=True)
    email_sales = models.EmailField("Email відділу продажів (sales@)", blank=True)
    email_manager_1 = models.EmailField("Email менеджера 1", blank=True)
    email_manager_2 = models.EmailField("Email менеджера 2", blank=True)
    email_hr = models.EmailField("Email HR (hr-manager@)", blank=True)

    # Working hours
    hours_weekdays = models.CharField(
        "Робочі години (Пн–Пт)", max_length=50, default="09:00 – 18:00", blank=True
    )
    hours_saturday = models.CharField(
        "Робочі години (Сб)", max_length=50, default="10:00 – 16:00", blank=True
    )
    hours_sunday = models.CharField(
        "Неділя", max_length=50, default="вихідний", blank=True
    )

    # Social
    facebook_url = models.URLField("Facebook", blank=True)
    instagram_url = models.URLField("Instagram", blank=True)
    telegram_url = models.URLField("Telegram", blank=True)

    # SEO
    seo_title = models.CharField("SEO title", max_length=70, blank=True)
    seo_description = models.CharField("SEO description", max_length=160, blank=True)
    og_image = models.ImageField("OG Image", upload_to="seo/", blank=True, null=True)

    # Branding
    favicon = models.ImageField("Favicon", upload_to="branding/", blank=True, null=True)
    logo = models.ImageField("Логотип", upload_to="branding/", blank=True, null=True)

    # Документи (сторінки «Партнери»)
    partner_contract_file = models.FileField(
        "Договір купівлі-продажу (файл)",
        upload_to="docs/",
        blank=True,
        null=True,
        help_text="Файл, який завантажується на сторінці «Стати партнером» (.doc, .docx, .pdf).",
    )
    warranty_act_file = models.FileField(
        "Акт приймання на гарантійний ремонт (файл)",
        upload_to="docs/",
        blank=True,
        null=True,
        help_text="Файл, який завантажується на сторінці «Сервіс і гарантія» (.xlsx, .pdf, .doc).",
    )

    # Map (сторінки «Партнери» та «Співпраця»)
    map_embed_code = models.TextField(
        "Код карти (iframe з Google Maps або OpenStreetMap)",
        blank=True,
        default=(
            '<iframe src="https://maps.google.com/maps?q=Kyiv,+Ukraine&z=4&output=embed"'
            ' width="600" height="450" style="border:0;"'
            ' allowfullscreen="" loading="lazy"'
            ' referrerpolicy="strict-origin-when-cross-origin"></iframe>'
        ),
        help_text=(
            "Вставте повний код &lt;iframe&gt;...&lt;/iframe&gt;, отриманий "
            "у Google Maps через «Поділитися → Вставити карту». "
            "Якщо поле порожнє — показується карта Європи за замовчуванням."
        ),
    )

    class Meta:
        verbose_name = "Налаштування сайту"

    def __str__(self):
        return self.site_name
