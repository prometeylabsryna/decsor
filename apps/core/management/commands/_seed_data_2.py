"""Дані (uk/en) для PageContent — частина 1: «Про компанію», «Співпраця»,
«Партнери» (вступ), «Доставка». Використовується командою
`seed_editable_content`. Не є management-командою (починається з «_»).
"""


def get_page_content_part1(email, email_sales, delivery_transport_url):
    from apps.core.models import PageContent

    return {
        PageContent.ABOUT_INTRO: {
            "uk": (
                "<p>Компанія <strong>Led leader — DIGITAL EQUIPMENT</strong> існує на ринку "
                "мобільного зв'язку з 2006 року. За роки наполегливої праці наша компанія "
                "встановила для себе чіткі пріоритети, які на даний момент є невід'ємною "
                "частиною:</p>"
                "<ul>"
                "<li>Тільки якісна продукція.</li>"
                "<li>Розумна цінова політика.</li>"
                "<li>Співпраця з всесвітньо відомими брендами.</li>"
                "<li>Клієнт завжди правий!</li>"
                "</ul>"
                "<p>Компанія здійснює підтримку клієнтів на всіх етапах роботи, а саме: "
                "надання інформаційної допомоги; індивідуально підібраних для кожного "
                "зручних взаєморозрахунків; гарантійне обслуговування.</p>"
                "<p>Завдяки нашим можливостям на всій території України та Європи, ви "
                "можете здійснити оптову закупівлю цікавих для вас мобільних телефонів, "
                "смартфонів, планшетів у великому ціновому діапазоні — від недорогих, "
                "доступних кожному, до ексклюзивних, обмежених у випуску. Також ми "
                "працюємо не лише за фактом наявності продукції, а й за попереднім "
                "замовленням, оскільки нашою головною метою є не сама суть угоди, а "
                "забезпечення максимально зручних та приємних умов для покупця, "
                "дотримання його прав та потреб — і з матеріальної, і з етичної сторони.</p>"
                "<p>Наша компанія є учасником преміум-класу платформи <strong>GSMexchange</strong> "
                "— міжнародного торгового майданчика, створеного для допомоги оптовим "
                "торговцям GSM-гаджетами, заснованого в Дубліні; як відомо, всі її учасники "
                "перевіряються на відповідність вимогам безпеки торгівлі — а це вже "
                "говорить про багато!</p>"
                "<p>Отже, якщо вам потрібна якісна техніка за приємною ціною в будь-яких "
                "обсягах — вам саме до нас!</p>"
            ),
            "en": (
                "<p>Company <strong>Led leader — DIGITAL EQUIPMENT</strong> has been operating "
                "in the mobile communications market since 2006. Over years of dedicated "
                "work, we have established clear priorities that form an integral part of "
                "everything we do:</p>"
                "<ul>"
                "<li>Quality products only.</li>"
                "<li>Reasonable pricing policy.</li>"
                "<li>Cooperation with world-renowned brands.</li>"
                "<li>The customer is always right!</li>"
                "</ul>"
                "<p>The company supports clients at every stage of cooperation: providing "
                "informational assistance, individually tailored payment terms, and "
                "warranty service.</p>"
                "<p>Thanks to our reach across Ukraine and Europe, you can make wholesale "
                "purchases of mobile phones, smartphones and tablets across a wide price "
                "range — from affordable everyday models to exclusive limited editions. We "
                "also work on pre-order basis, because our primary goal is not just the "
                "transaction itself, but providing the most comfortable and pleasant "
                "conditions for every buyer, respecting their rights and needs — both "
                "financially and ethically.</p>"
                "<p>Our company is a premium member of the <strong>GSMexchange</strong> "
                "platform — an international marketplace founded in Dublin to assist "
                "wholesale GSM gadget traders; as all members are vetted against strict "
                "trade security requirements, this membership speaks for itself!</p>"
                "<p>So, if you need quality equipment at a great price in any quantity — "
                "we are the right choice!</p>"
            ),
        },
        PageContent.COOPERATION_INTRO: {
            "uk": (
                "<p>Компанія «Led leader» готова до взаємовигідної співпраці з точки зору "
                "просування нових брендів на ринок мобільних телефонів і активного "
                "висвітлення в ЗМІ технічних особливостей і переваг перспективних розробок, "
                "розрахованих на широке коло споживачів. Паралельно ми готові співпрацювати "
                "з виробниками та постачальниками будь-яких цифрових продуктів. Запрошуємо "
                "до діалогу регіональних представників, які зацікавлені у всебічному "
                "просуванні нових продуктів на ринок мобільних телефонів і різноманітної "
                "цифрової техніки.</p>"
            ),
            "en": (
                "<p>Led leader is open to mutually beneficial cooperation in promoting new "
                "brands to the mobile phone market and actively highlighting the technical "
                "features of promising products in the media. We are also ready to work "
                "with manufacturers and suppliers of any digital products. We invite "
                "regional representatives interested in comprehensive promotion of new "
                "products to the mobile phone and digital equipment market to get in "
                "touch.</p>"
            ),
        },
        PageContent.COOPERATION_NOTE: {
            "uk": "<p>Усіх, хто зацікавлений у цій пропозиції, просимо зв'язатися з нами телефоном або електронною поштою</p>",
            "en": "<p>All interested parties are welcome to contact us by phone or email</p>",
        },
        PageContent.PARTNERS_INTRO: {
            "uk": "<p>Завжди відкриті до діалогу, щоб представляти нашу компанію у вашому місті.</p>",
            "en": "<p>Always open to dialogue to represent our company in your city.</p>",
        },
        PageContent.DELIVERY_INTRO: {
            "uk": (
                "<p>Стати клієнтом компанії Led leader може будь-яка юридична особа або "
                "підприємець, який бажає здійснювати регулярні покупки мобільних телефонів "
                "у певному обсязі.</p>"
            ),
            "en": (
                "<p>Any legal entity or entrepreneur who wishes to make regular purchases of "
                "mobile phones in a certain volume can become a Led leader client.</p>"
            ),
        },
        PageContent.DELIVERY_CONDITIONS: {
            "uk": (
                "<ul>"
                "<li>Клієнтам компанії надаються пільгові умови співпраці, укладається "
                "дистриб'юторський договір.</li>"
                "<li>Клієнтам пропонується відстрочка платежу, торговий кредит.</li>"
                "<li>Гнучка система знижок, що базується на індивідуальному підході до "
                "кожного клієнта.</li>"
                "<li>У кожного клієнта є свій менеджер, який своєчасно попереджає про "
                "потік вашого товару.</li>"
                f'<li>Доставку товарів клієнтам по Україні здійснюють транспортні та '
                f'кур\'єрські організації (<a href="{delivery_transport_url}">Транспортні '
                f'послуги</a>). Відправлення вантажу здійснюється того ж дня після '
                f'бронювання.</li>'
                "<li>Рахунок на витрати на забезпечення позбавить вас від зайвих проблем.</li>"
                f'<li>Можливість оформлення замовлень телефоном або електронною поштою: '
                f'<a href="mailto:{email_sales}">{email_sales}</a></li>'
                "<li>Ми пропонуємо кожному клієнту індивідуальну схему співпраці.</li>"
                "</ul>"
            ),
            "en": (
                "<ul>"
                "<li>Clients are provided with preferential cooperation terms and a "
                "distribution agreement is concluded.</li>"
                "<li>Clients are offered deferred payment and trade credit.</li>"
                "<li>A flexible discount system based on an individual approach to each "
                "client.</li>"
                "<li>Each client has a dedicated manager who keeps them informed about "
                "their shipment.</li>"
                f'<li>Delivery of goods to clients across Ukraine is carried out by '
                f'transport and courier companies (<a href="{delivery_transport_url}">'
                f'Transport Services</a>). Shipments are dispatched on the same day as '
                f'booking.</li>'
                "<li>An expense account will save you from unnecessary hassle.</li>"
                f'<li>Orders can be placed by phone or email: '
                f'<a href="mailto:{email_sales}">{email_sales}</a></li>'
                "<li>We offer every client an individual cooperation scheme.</li>"
                "</ul>"
            ),
        },
        PageContent.DELIVERY_DISCOUNTS: {
            "uk": (
                "<p>Знижки та додаткові умови обговорюються з вашим персональним менеджером. "
                "На додаткові знижки також може розраховувати будь-який клієнт фірми Led "
                "leader, який бажає здійснити разову, оптову покупку на суму понад 2000 "
                "доларів США. Знижка в цьому випадку встановлюється за індивідуальною "
                "домовленістю. Оплата здійснюється в національній валюті за поточним "
                "курсом на дату оплати товару.</p>"
            ),
            "en": (
                "<p>Discounts and additional terms are discussed with your personal manager. "
                "Additional discounts are also available to any Led leader client wishing "
                "to make a one-time wholesale purchase exceeding $2,000. The discount in "
                "this case is determined by individual agreement. Payment is made in "
                "national currency at the current exchange rate on the date of payment.</p>"
            ),
        },
        PageContent.DELIVERY_ORDER_STEPS: {
            "uk": (
                "<h3>Крок 1 — Обрати товар</h3>"
                "<p>Ознайомтеся з нашим асортиментом та зв'яжіться з менеджером для "
                "отримання актуального прайс-листа та інформації про наявність товару на "
                "складі.</p>"
                "<h3>Крок 2 — Оформити заявку</h3>"
                f'<p>Надішліть заявку на email <a href="mailto:{email}">{email}</a> із '
                f'зазначенням:</p>'
                "<ul>"
                "<li>Назви та артикулу товару</li>"
                "<li>Необхідної кількості</li>"
                "<li>Ваших контактних даних</li>"
                "<li>Адреси доставки</li>"
                "</ul>"
                "<h3>Крок 3 — Підтвердження та оплата</h3>"
                "<p>Після отримання заявки менеджер сформує рахунок і надішле його вам. "
                "Замовлення відправляється після підтвердження оплати.</p>"
            ),
            "en": (
                "<h3>Step 1 — Choose a Product</h3>"
                "<p>Browse our assortment and contact a manager to get the latest price "
                "list and stock availability information.</p>"
                "<h3>Step 2 — Submit a Request</h3>"
                f'<p>Send your request to <a href="mailto:{email}">{email}</a> with the '
                f'following details:</p>'
                "<ul>"
                "<li>Product name and SKU</li>"
                "<li>Required quantity</li>"
                "<li>Your contact details</li>"
                "<li>Delivery address</li>"
                "</ul>"
                "<h3>Step 3 — Confirmation &amp; Payment</h3>"
                "<p>After receiving your request, the manager will issue an invoice and "
                "send it to you. The order is dispatched after payment confirmation.</p>"
            ),
        },
        PageContent.DELIVERY_ORDER_PAYMENT: {
            "uk": (
                "<h3>Безготівковий розрахунок</h3>"
                "<p>Для юридичних осіб та ФОП — оплата за виставленим рахунком на поточний "
                "рахунок компанії. Усі необхідні документи (рахунок, видаткова накладна, "
                "ТТН) надаються в електронному вигляді.</p>"
                "<h3>Оплата на картку</h3>"
                "<p>Для фізичних осіб та невеликих замовлень — оплата на картку "
                "VISA/MasterCard (Приватбанк або Monobank).</p>"
                "<h3>Відстрочка платежу</h3>"
                "<p>Для постійних клієнтів можлива відстрочка платежу від 7 до 30 днів. "
                "Умови визначаються індивідуально.</p>"
            ),
            "en": (
                "<h3>Bank Transfer</h3>"
                "<p>For legal entities and sole proprietors — payment by invoice to the "
                "company's current account. All required documents (invoice, delivery "
                "note, waybill) are provided electronically.</p>"
                "<h3>Card Payment</h3>"
                "<p>For individuals and small orders — payment by VISA/MasterCard "
                "(Privatbank or Monobank).</p>"
                "<h3>Deferred Payment</h3>"
                "<p>Regular clients may be offered deferred payment terms of 7 to 30 days. "
                "Conditions are determined individually.</p>"
            ),
        },
        PageContent.DELIVERY_TRANSPORT_INTRO: {
            "uk": (
                "<p>Ми співпрацюємо з надійними транспортними компаніями для забезпечення "
                "своєчасної та безпечної доставки замовлень по всій Україні та Європі.</p>"
            ),
            "en": (
                "<p>We partner with reliable transport companies to ensure timely and safe "
                "delivery of orders across Ukraine and Europe.</p>"
            ),
        },
        PageContent.DELIVERY_TRANSPORT_NOTE: {
            "uk": (
                "<p>Клієнт оплачує доставку за тарифами обраного перевізника. При "
                "замовленнях від визначеної суми — доставка за рахунок компанії "
                "(уточнюйте у менеджера).</p>"
            ),
            "en": (
                "<p>The client pays for delivery at the rates of the chosen carrier. For "
                "orders above a specified amount, delivery is covered by the company "
                "(please confirm with your manager).</p>"
            ),
        },
    }
