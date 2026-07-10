"""Дані (uk/en) для FaqItem, ServiceCenter, PartnerRegion — використовується
командою `seed_editable_content`. Файл не є management-командою (починається
з «_», Django його не підхоплює як окрему команду).
"""


def get_faq_items(delivery_order_url, delivery_url, partners_service_url):
    return [
        {
            "question_uk": "А що таке FAQ?",
            "question_en": "What is FAQ?",
            "answer_uk": "<p>Тут ви можете знайти відповіді на свої запитання.</p>",
            "answer_en": "<p>Here you can find answers to your questions.</p>",
        },
        {
            "question_uk": "Як часто ви оновлюєте ціну?",
            "question_en": "How often do you update prices?",
            "answer_uk": "<p>Ціна оновлюється в міру надходження товару (1–2 рази на день).</p>",
            "answer_en": "<p>Prices are updated as stock arrives (1–2 times per day).</p>",
        },
        {
            "question_uk": "Як мені оформити замовлення?",
            "question_en": "How do I place an order?",
            "answer_uk": (
                f'<p>Замовлення описано в розділі '
                f'<a href="{delivery_order_url}">замовлення та оплата</a>.</p>'
            ),
            "answer_en": (
                f'<p>The ordering process is described in the '
                f'<a href="{delivery_order_url}">orders &amp; payment</a> section.</p>'
            ),
        },
        {
            "question_uk": "Я живу далеко від Києва, чи можете ви доставити товар в інше місто?",
            "question_en": "I live far from Kyiv, can you deliver to another city?",
            "answer_uk": (
                f'<p>Без жодних проблем, за умови повної оплати товару та вартості доставки '
                f'(<a href="{delivery_url}">доставка</a>).</p>'
            ),
            "answer_en": (
                f'<p>No problem at all, provided full payment for the goods and delivery costs '
                f'(<a href="{delivery_url}">delivery</a>).</p>'
            ),
        },
        {
            "question_uk": "Як мені здійснити оплату за товар?",
            "question_en": "How do I pay for goods?",
            "answer_uk": (
                "<p>Готівкою в нашому офісі. Банківським переказом в офісах на рахунок ТМ «Led "
                "leader». Також грошові перекази за системою VISA або MasterCard, у будь-якому "
                "відділенні банків Приватбанк, ПУМБ, ОТП банк, Монобанк.</p>"
            ),
            "answer_en": (
                "<p>Cash at our office. Bank transfer to the TM «Led leader» account. Also VISA "
                "or MasterCard transfers at any branch of Privatbank, FUIB, OTP Bank, Monobank.</p>"
            ),
        },
        {
            "question_uk": "Ваш прайс-лист містить лише роздрібні ціни, але я хочу замовити товар оптом?",
            "question_en": "Your price list only shows retail prices, but I want to order wholesale?",
            "answer_uk": (
                "<p>Щоб отримати доступ до оптових цін, вам необхідно зареєструватися на сайті "
                "або зв'язатися з менеджером по телефону або електронною поштою.</p>"
            ),
            "answer_en": (
                "<p>To access wholesale prices, you need to register on the website or contact "
                "a manager by phone or email.</p>"
            ),
        },
        {
            "question_uk": "Чи надаєте ви гарантію на мобільні телефони?",
            "question_en": "Do you provide warranty on mobile phones?",
            "answer_uk": (
                f'<p>Ми надаємо гарантію на мобільні телефони 1–12 та 36 місяців з дати продажу, '
                f'залежно від сертифікації телефону '
                f'(<a href="{partners_service_url}">Сервіс та гарантія</a>).</p>'
            ),
            "answer_en": (
                f"<p>We provide a warranty on mobile phones of 1–12 and 36 months from the date "
                f"of sale, depending on the phone's certification "
                f'(<a href="{partners_service_url}">Service &amp; Warranty</a>).</p>'
            ),
        },
        {
            "question_uk": "Техніка, яка продається на вашому сайті, справжня?",
            "question_en": "Is the equipment sold on your website genuine?",
            "answer_uk": "<p>Техніка справжня українська та європейського зразка, сертифікована.</p>",
            "answer_en": "<p>The equipment is genuine Ukrainian and European standard, certified.</p>",
        },
        {
            "question_uk": "У вашому прайс-листі немає товарів, які б хотів замовити. Що мені робити?",
            "question_en": "Your price list doesn't have the items I want to order. What should I do?",
            "answer_uk": (
                "<p>Будь ласка, зв'яжіться з менеджером та обговоріть час та можливість "
                "постачання того, що вам потрібно.</p>"
            ),
            "answer_en": (
                "<p>Please contact a manager to discuss the timing and availability of "
                "supplying what you need.</p>"
            ),
        },
        {
            "question_uk": "Чи є у вас якісь спеціальні пропозиції або знижки для постійних клієнтів?",
            "question_en": "Do you have any special offers or discounts for regular clients?",
            "answer_uk": (
                "<p>Для постійних клієнтів у нас діє гнучка система знижок. Для отримання "
                "додаткової інформації звертайтесь до менеджера.</p>"
            ),
            "answer_en": (
                "<p>We have a flexible discount system for regular clients. Contact your "
                "manager for more information.</p>"
            ),
        },
        {
            "question_uk": "У мене є ідеї та пропозиції щодо співпраці, як я можу їх реалізувати?",
            "question_en": "I have ideas and proposals for cooperation, how can I put them into practice?",
            "answer_uk": "<p>Обговоріть свої ідеї з нами.</p>",
            "answer_en": "<p>Discuss your ideas with us.</p>",
        },
    ]


def get_service_centers():
    return [
        {
            "name_uk": "ERC",
            "name_en": "ERC",
            "url": "https://www.erc.ua",
            "address_uk": "м. Київ, вул. Марка Вовчка, 18а (Вхід з боку вул. Вербової)",
            "address_en": "Kyiv, Marka Vovchka St., 18a (entrance from Verbova St.)",
            "phone": "+38 044 230 34 84",
            "order": 0,
        },
        {
            "name_uk": "«Крок СК»",
            "name_en": "«Krok SK»",
            "url": "https://www.krok-ttc.com",
            "address_uk": "м. Київ, пр-т Маяковського 26",
            "address_en": "Kyiv, Mayakovskoho Ave., 26",
            "phone": "+38 0800 50-45-04",
            "order": 1,
        },
        {
            "name_uk": "MTI",
            "name_en": "MTI",
            "url": "https://mti-service.com.ua/",
            "address_uk": "бул. Лесі Українки, 4, Київ, 01133",
            "address_en": "Lesi Ukrainky Blvd., 4, Kyiv, 01133",
            "phone": "0800332947",
            "order": 2,
        },
    ]


def get_partner_regions():
    return [
        ("Закарпатська область:", "Zakarpattia Region:", ["Ужгород", "Виноградово", "Мукачево"], ["Uzhhorod", "Vynohradiv", "Mukachevo"]),
        ("Житомирська область:", "Zhytomyr Region:", ["Житомир", "Малин", "Радомишль"], ["Zhytomyr", "Malyn", "Radomyshl"]),
        ("Чернігівська область:", "Chernihiv Region:", ["Чернігів", "Бахмач", "Ніжин", "Прилуки", "Глибока"], ["Chernihiv", "Bakhmach", "Nizhyn", "Pryluky", "Hlyboka"]),
        ("Сумська область:", "Sumy Region:", ["Суми", "Ромни", "Шостка"], ["Sumy", "Romny", "Shostka"]),
        ("Рівненська область:", "Rivne Region:", ["Рівне"], ["Rivne"]),
        ("Львівська область:", "Lviv Region:", ["Львів"], ["Lviv"]),
        ("Київська область:", "Kyiv Region:", ["Київ", "Біла Церква", "Бровари", "Ірпінь", "Іванків", "Обухів"], ["Kyiv", "Bila Tserkva", "Brovary", "Irpin", "Ivankiv", "Obukhiv"]),
        ("Полтавська область:", "Poltava Region:", ["Полтава", "Кременчук"], ["Poltava", "Kremenchuk"]),
        ("Івано-Франківська область:", "Ivano-Frankivsk Region:", ["Івано-Франківськ", "Калуш"], ["Ivano-Frankivsk", "Kalush"]),
        ("Кіровоградська область:", "Kirovohrad Region:", ["Кіровоград", "Олександрія", "Світловодськ"], ["Kropyvnytskyi", "Oleksandriia", "Svitlovodsk"]),
        ("Дніпропетровська область:", "Dnipropetrovsk Region:", ["Дніпро", "Кам'янське", "Жовті Води", "Кривий Ріг", "Нікополь"], ["Dnipro", "Kamianske", "Zhovti Vody", "Kryvyi Rih", "Nikopol"]),
        ("Вінницька область:", "Vinnytsia Region:", ["Вінниця", "Могилів"], ["Vinnytsia", "Mohyliv"]),
        ("Волинська область:", "Volyn Region:", ["Луцьк", "Нововолинськ"], ["Lutsk", "Novovolynsk"]),
        ("Миколаївська область:", "Mykolaiv Region:", ["Миколаїв", "Вознесенськ", "Південноукраїнськ"], ["Mykolaiv", "Voznesensk", "Pivdennoukrainsk"]),
        ("Запорізька область:", "Zaporizhzhia Region:", ["Мелітополь", "Токмак"], ["Melitopol", "Tokmak"]),
        ("Тернопільська область:", "Ternopil Region:", ["Тернопіль"], ["Ternopil"]),
        ("Черкаська область:", "Cherkasy Region:", ["Черкаси"], ["Cherkasy"]),
        ("Хмельницька область:", "Khmelnytskyi Region:", ["Хмельницький", "Шепетівка", "Славута"], ["Khmelnytskyi", "Shepetivka", "Slavuta"]),
        ("Одеська область:", "Odesa Region:", ["Одеса", "Ізмаїл", "Рені"], ["Odesa", "Izmail", "Reni"]),
        ("Херсонська область:", "Kherson Region:", ["Херсон"], ["Kherson"]),
        ("Харківська область:", "Kharkiv Region:", ["Харків"], ["Kharkiv"]),
        ("Чернівецька область:", "Chernivtsi Region:", ["Чернівці"], ["Chernivtsi"]),
        ("Латвія:", "Latvia:", ["Рига"], ["Riga"]),
    ]
