"""Management command to populate the database with initial seed data."""
from django.core.management.base import BaseCommand
from django.utils import timezone


class Command(BaseCommand):
    help = "Заповнює базу даних початковими даними (seed) на основі ltm.com.ua"

    def add_arguments(self, parser):
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Видалити всі наявні дані перед заповненням",
        )
        parser.add_argument(
            "--with-market-news",
            action="store_true",
            help="Після seed імпортувати новини ринку з RSS",
        )

    def handle(self, *args, **options):
        if options["flush"]:
            self._flush()

        self._seed_site_settings()
        self._seed_hero()
        self._seed_services()
        self._seed_advantages()
        self._seed_cooperation_banner()
        self._seed_news()
        self._seed_brands()
        self._seed_carriers()

        if options["with_market_news"]:
            self._fetch_market_news()

        self.stdout.write(self.style.SUCCESS("✓ Seed завершено успішно"))

    # ------------------------------------------------------------------
    def _flush(self):
        from apps.core.models import SiteSettings, HeroSection, Service, Advantage, CooperationBanner
        from apps.news.models import NewsArticle
        from apps.brands.models import Brand
        from apps.core.models import Carrier

        HeroSection.objects.all().delete()
        Service.objects.all().delete()
        Advantage.objects.all().delete()
        CooperationBanner.objects.all().delete()
        NewsArticle.objects.all().delete()
        Brand.objects.all().delete()
        Carrier.objects.all().delete()
        self.stdout.write(self.style.WARNING("  Дані очищено"))

    # ------------------------------------------------------------------
    def _seed_site_settings(self):
        from apps.core.models import SiteSettings

        settings = SiteSettings.get_solo()
        settings.site_name = "Led leader"
        settings.site_name_en = "Led leader"
        settings.tagline = "Digital Equipment"
        settings.description = (
            "Led leader — Digital Equipment існує на ринку мобільних комунікацій "
            "з 2006 року. Оптовий продаж цифрових товарів від перевірених виробників."
        )
        settings.description_en = (
            "Led leader — Digital Equipment has been on the mobile communications market "
            "since 2006. Wholesale sales of digital goods from verified manufacturers."
        )
        settings.founded_year = 2006
        settings.email = "info@ltm.com.ua"
        settings.phone = "+38 044 303-92-20"
        settings.address = "Україна, Київ"
        settings.email_partner = "partner@ltm.com.ua"
        settings.email_advertising = "reklama@ltm.com.ua"
        settings.email_sales = "sales@ltm.com.ua"
        settings.email_manager_1 = "manager5@ltm.com.ua"
        settings.email_manager_2 = "manager6@ltm.com.ua"
        settings.email_hr = "hr-manager@ltm.com.ua"
        settings.seo_title = "Led leader Digital Equipment — оптовий продаж цифрової техніки"
        settings.seo_title_en = "Led leader Digital Equipment — wholesale digital equipment"
        settings.seo_description = (
            "Led leader — оптовий дистриб'ютор цифрового обладнання з 2006 року. "
            "Доставка по всій Україні. Гарантія якості."
        )
        settings.seo_description_en = (
            "Led leader — wholesale distributor of digital equipment since 2006. "
            "Delivery across Ukraine. Quality guarantee."
        )
        settings.save()
        self.stdout.write("  ✓ SiteSettings")

    # ------------------------------------------------------------------
    def _seed_hero(self):
        from apps.core.models import HeroSection

        heroes = [
            {
                "order": 0,
                "is_active": True,
                "cta_url": "#cooperation",
                "title_uk": "LED LEADER — DIGITAL EQUIPMENT",
                "title_en": "LED LEADER — DIGITAL EQUIPMENT",
                "subtitle_uk": "На ринку мобільних комунікацій з 2006 року",
                "subtitle_en": "On the mobile communications market since 2006",
                "body_uk": (
                    "За роки напруженої роботи компанія сформувала чіткі пріоритети, "
                    "які є невід'ємною частиною її діяльності."
                ),
                "body_en": (
                    "Through years of dedicated work the company has set clear priorities "
                    "that are an integral part of its operations."
                ),
                "cta_text_uk": "Зв'язатися з нами",
                "cta_text_en": "Get in touch",
            }
        ]

        for data in heroes:
            obj, _ = HeroSection.objects.update_or_create(
                order=data["order"],
                defaults=data,
            )
            obj.title = obj.title_uk
            obj.subtitle = obj.subtitle_uk
            obj.body = obj.body_uk
            obj.cta_text = obj.cta_text_uk
            obj.save(update_fields=["title", "subtitle", "body", "cta_text"])
        self.stdout.write("  ✓ HeroSection")

    # ------------------------------------------------------------------
    def _seed_services(self):
        from apps.core.models import Service

        services = [
            {
                "icon": "handshake",
                "order": 0,
                "is_active": True,
                "title_uk": "Співпраця",
                "title_en": "Cooperation",
                "description_uk": (
                    "Led leader готовий до взаємовигідного співробітництва як зі "
                    "споживачами, так і з постачальниками будь-якого цифрового обладнання."
                ),
                "description_en": (
                    "Led leader is open to mutually beneficial cooperation with both "
                    "customers and suppliers of any digital equipment."
                ),
            },
            {
                "icon": "truck",
                "order": 1,
                "is_active": True,
                "title_uk": "Доставка продукції",
                "title_en": "Product delivery",
                "description_uk": (
                    "Led leader здійснює доставку замовлення зручним для клієнта "
                    "перевізником або службою доставки по всій Україні."
                ),
                "description_en": (
                    "Led leader delivers orders via the carrier or courier service "
                    "of the customer's choice across Ukraine."
                ),
            },
            {
                "icon": "shield-check",
                "order": 2,
                "is_active": True,
                "title_uk": "Гарантія якості",
                "title_en": "Quality guarantee",
                "description_uk": (
                    "Якість продукції, що постачається Led leader, підтверджена "
                    "всіма необхідними сертифікатами від виробника."
                ),
                "description_en": (
                    "The quality of products supplied by Led leader is confirmed by "
                    "all required manufacturer certificates."
                ),
            },
            {
                "icon": "wrench",
                "order": 3,
                "is_active": True,
                "title_uk": "Якісний сервіс",
                "title_en": "Reliable service",
                "description_uk": (
                    "Сервісний центр Led leader надає гарантію на весь перелік "
                    "цифрового обладнання, що постачається клієнту."
                ),
                "description_en": (
                    "Led leader service centre provides warranty for the full range "
                    "of digital equipment supplied to the customer."
                ),
            },
        ]

        for data in services:
            obj, _ = Service.objects.update_or_create(
                icon=data["icon"],
                defaults=data,
            )
            obj.title = obj.title_uk
            obj.description = obj.description_uk
            obj.save(update_fields=["title", "description"])
        self.stdout.write(f"  ✓ Services ({len(services)})")

    # ------------------------------------------------------------------
    def _seed_advantages(self):
        from apps.core.models import Advantage

        advantages = [
            {
                "icon": "star",
                "order": 0,
                "is_active": True,
                "title_uk": "Тільки якісні продукти",
                "title_en": "Only quality products",
            },
            {
                "icon": "tag",
                "order": 1,
                "is_active": True,
                "title_uk": "Розумна цінова політика",
                "title_en": "Reasonable pricing policy",
            },
            {
                "icon": "globe",
                "order": 2,
                "is_active": True,
                "title_uk": "Робота з глобальними брендами",
                "title_en": "Work with global brands",
            },
            {
                "icon": "heart",
                "order": 3,
                "is_active": True,
                "title_uk": "Ми цінуємо наших клієнтів",
                "title_en": "We value our customers",
            },
        ]

        for data in advantages:
            obj, _ = Advantage.objects.update_or_create(
                icon=data["icon"],
                defaults=data,
            )
            obj.title = obj.title_uk
            obj.save(update_fields=["title"])
        self.stdout.write(f"  ✓ Advantages ({len(advantages)})")

    # ------------------------------------------------------------------
    def _seed_cooperation_banner(self):
        from apps.core.models import CooperationBanner

        data = {
            "is_active": True,
            "heading_uk": "В рамках оптових закупівель та співпраці",
            "heading_en": "Within wholesale purchasing and cooperation",
            "body_uk": (
                "Якщо у вас є пропозиція про співпрацю з нашою компанією — "
                "напишіть нам на пошту, і менеджер зв'яжеться з вами найближчим часом."
            ),
            "body_en": (
                "If you have a cooperation proposal for our company — drop us an "
                "email, and our manager will get back to you shortly."
            ),
        }
        obj, _ = CooperationBanner.objects.update_or_create(
            cta_email="info@ltm.com.ua",
            defaults=data,
        )
        obj.heading = obj.heading_uk
        obj.body = obj.body_uk
        obj.save(update_fields=["heading", "body"])
        self.stdout.write("  ✓ CooperationBanner")

    def _fetch_market_news(self):
        from django.core.management import call_command

        self.stdout.write("  Імпорт новин ринку з RSS...")
        try:
            call_command("fetch_market_news")
        except SystemExit as exc:
            if exc.code:
                self.stdout.write(
                    self.style.WARNING(
                        "  ⚠ Не вдалося імпортувати новини ринку (перевірте мережу або RSS)."
                    )
                )
            return
        self.stdout.write("  ✓ Новини ринку")

    # ------------------------------------------------------------------
    def _seed_news(self):
        from apps.news.models import NewsArticle

        tz = timezone.get_current_timezone()
        # Новини ринку імпортуються з RSS (manage.py fetch_market_news).
        articles = [
            {
                "slug": "led-leader-assortment-2019",
                "title_uk": "Led leader розширює асортимент продукції на 2019 рік",
                "category": NewsArticle.CATEGORY_COMPANY,
                "excerpt_uk": (
                    "Компанія Led leader оголошує про розширення асортименту цифрової техніки "
                    "у 2019 році. До переліку додаються нові категорії товарів від "
                    "провідних світових виробників."
                ),
                "content_uk": (
                    "Компанія Led leader оголошує про розширення асортименту цифрової техніки "
                    "у 2019 році. До переліку додаються нові категорії товарів від "
                    "провідних світових виробників: смарт-аксесуари, TWS-навушники, "
                    "портативні акумулятори та пристрої для розумного дому. "
                    "Ми продовжуємо зміцнювати партнерські стосунки з Samsung, Apple, Xiaomi."
                ),
                "published_at": timezone.datetime(2018, 7, 1, 9, 0, tzinfo=tz),
                "is_published": True,
            },
            {
                "slug": "led-leader-gsmexchange",
                "title_uk": "Led leader став учасником платформи GSMexchange",
                "category": NewsArticle.CATEGORY_COMPANY,
                "excerpt_uk": (
                    "Наша компанія є учасником преміум-класу платформи GSMexchange — "
                    "міжнародного торгового майданчика для оптових торговців GSM-гаджетами, "
                    "заснованого в Дубліні."
                ),
                "content_uk": (
                    "Наша компанія є учасником преміум-класу платформи GSMexchange — "
                    "міжнародного торгового майданчика для оптових торговців GSM-гаджетами, "
                    "заснованого в Дубліні. Участь у GSMexchange підтверджує надійність та "
                    "прозорість Led leader як оптового дистриб'ютора цифрового обладнання."
                ),
                "published_at": timezone.datetime(2018, 6, 15, 10, 0, tzinfo=tz),
                "is_published": True,
            },
        ]

        for data in articles:
            slug = data.pop("slug")
            obj, created = NewsArticle.objects.get_or_create(slug=slug, defaults=data)
            if not created and not obj.title_uk:
                for field, value in data.items():
                    setattr(obj, field, value)
                obj.save()
        self.stdout.write(f"  ✓ NewsArticles ({len(articles)})")

    # ------------------------------------------------------------------
    def _seed_brands(self):
        from apps.brands.models import Brand

        brand_names = [
            "Apple", "Samsung", "Xiaomi", "Huawei", "Sony",
            "LG", "ZTE", "Nokia", "OnePlus", "OPPO", "Blackview",
        ]

        for i, name in enumerate(brand_names):
            Brand.objects.get_or_create(
                name=name,
                defaults={"order": i, "is_active": True},
            )
        self.stdout.write(f"  ✓ Brands ({len(brand_names)})")

    # ------------------------------------------------------------------
    def _seed_carriers(self):
        from apps.core.models import Carrier

        carriers = [
            {
                "order": 0,
                "is_active": True,
                "name_uk": "Нова Пошта",
                "name_en": "Nova Poshta",
                "description_uk": (
                    "Найбільша приватна служба доставки в Україні. Доставка до "
                    "відділення або кур'єром за адресою. Широка мережа — понад "
                    "6 000 відділень по всій Україні. Терміни: 1–3 робочих дні."
                ),
                "description_en": (
                    "The largest private delivery service in Ukraine. Delivery "
                    "to a branch or by courier to the address. A wide network — "
                    "over 6,000 branches across Ukraine. Timeframe: 1–3 business days."
                ),
            },
            {
                "order": 1,
                "is_active": True,
                "name_uk": "Укрпошта",
                "name_en": "Ukrposhta",
                "description_uk": (
                    "Національний оператор поштового зв'язку. Доставка в усі "
                    "куточки України, включаючи невеликі населені пункти. "
                    "Терміни: 3–7 робочих днів."
                ),
                "description_en": (
                    "The national postal operator. Delivery to every corner of "
                    "Ukraine, including small towns and villages. "
                    "Timeframe: 3–7 business days."
                ),
            },
            {
                "order": 2,
                "is_active": True,
                "name_uk": "SAT (Служба авто-транспорту)",
                "name_en": "SAT (Auto Transport Service)",
                "description_uk": (
                    "Спеціалізується на доставці вантажів для бізнесу. "
                    "Оптимальний вибір для великих оптових замовлень. "
                    "Терміни: 1–4 робочих дні."
                ),
                "description_en": (
                    "Specializes in cargo delivery for businesses. The optimal "
                    "choice for large wholesale orders. Timeframe: 1–4 business days."
                ),
            },
            {
                "order": 3,
                "is_active": True,
                "name_uk": "Meest Express",
                "name_en": "Meest Express",
                "description_uk": (
                    "Міжнародна логістична компанія з широкою мережею в Україні "
                    "та Європі. Надійна доставка у великих містах та регіонах. "
                    "Терміни: 1–3 робочих дні."
                ),
                "description_en": (
                    "An international logistics company with a wide network in "
                    "Ukraine and Europe. Reliable delivery to major cities and "
                    "regions. Timeframe: 1–3 business days."
                ),
            },
            {
                "order": 4,
                "is_active": True,
                "name_uk": "Delivery",
                "name_en": "Delivery",
                "description_uk": (
                    "Кур'єрська служба доставки по всій Україні. Швидка "
                    "доставка в день оформлення або наступного дня. Покриття "
                    "всіх обласних центрів та великих міст. "
                    "Терміни: 1–2 робочих дні."
                ),
                "description_en": (
                    "A courier delivery service across Ukraine. Fast delivery "
                    "on the day of the order or the next day. Coverage of all "
                    "regional centers and major cities. Timeframe: 1–2 business days."
                ),
            },
            {
                "order": 5,
                "is_active": True,
                "name_uk": "Самовивіз",
                "name_en": "Self-pickup",
                "description_uk": (
                    "Ви можете забрати замовлення самостійно з нашого складу. "
                    "Адреса та час роботи — уточнюйте у менеджера."
                ),
                "description_en": (
                    "You can pick up your order yourself from our warehouse. "
                    "Please check the address and working hours with our manager."
                ),
            },
        ]

        for data in carriers:
            Carrier.objects.get_or_create(
                name_uk=data["name_uk"],
                defaults=data,
            )
        self.stdout.write(f"  ✓ Carriers ({len(carriers)})")
