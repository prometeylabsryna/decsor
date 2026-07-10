"""Дані (uk/en) для PageContent — частина 2: «Партнерська програма»,
«Стати партнером», «Сервіс і гарантія». Використовується командою
`seed_editable_content`. Не є management-командою (починається з «_»).
"""


def get_page_content_part2(email_partner, email_hr):
    from apps.core.models import PageContent

    return {
        PageContent.PARTNERS_PROGRAM_INTRO: {
            "uk": (
                "<p>Співпрацюючи з компанією Led leader Ви купуєте партнера з:</p>"
                "<ul>"
                "<li>довгостроковим досвідом роботи і стратегічним партнерством з "
                "виробниками</li>"
                "<li>регіональною інфраструктурою включаючи офіси, склади</li>"
                "<li>персональним менеджером, закріпленим за вашою компанією</li>"
                "<li>відкритістю та прозорістю співпраці з партнерами</li>"
                "<li>стабільними оптовими цінами</li>"
                "<li>наявністю сучасної інформаційної системи</li>"
                "<li>маркетинговою командою, готовою негайно приступити до співпраці з "
                "вашою компанією</li>"
                "<li>польовими силами та системою аналізу ринку</li>"
                "<li>інформаційною підтримкою та проведенням конференцій</li>"
                "</ul>"
                "<p>Компанія має дуже широкий спектр партнерів та покупців, вони розкидані "
                "в різних куточках Європи</p>"
            ),
            "en": (
                "<p>By partnering with Led leader, you gain a partner with:</p>"
                "<ul>"
                "<li>long-term experience and strategic partnerships with manufacturers</li>"
                "<li>regional infrastructure including offices and warehouses</li>"
                "<li>a dedicated personal manager assigned to your company</li>"
                "<li>openness and transparency in partner cooperation</li>"
                "<li>stable wholesale prices</li>"
                "<li>a modern information system</li>"
                "<li>a marketing team ready to immediately start working with your "
                "company</li>"
                "<li>field forces and a market analysis system</li>"
                "<li>information support and conference hosting</li>"
                "</ul>"
                "<p>The company has a very wide range of partners and buyers spread across "
                "various parts of Europe</p>"
            ),
        },
        PageContent.PARTNERS_PROGRAM_OUTRO: {
            "uk": "<p>Завжди відкриті до діалогу для представлення нашої компанії у Вашому місті.</p>",
            "en": "<p>Always open to dialogue to represent our company in your city.</p>",
        },
        PageContent.PARTNERS_BECOME_CONTRACT: {
            "uk": (
                "<p>Якщо ви хочете заощадити час і почати роботу з нашою компанією в самі "
                "короткі терміни просимо ознайомитися з:</p>"
            ),
            "en": (
                "<p>If you want to save time and start working with us as quickly as "
                "possible, please review:</p>"
            ),
        },
        PageContent.PARTNERS_BECOME_CONTRACT_FOLLOWUP: {
            "uk": (
                "<p>У разі якщо у Вас немає претензій і побажань для зміни типового "
                f'договору з компанією Led leader то підпишіть його зі свого боку і '
                f'відправте його нам на адресу <a href="mailto:{email_partner}">'
                f'{email_partner}</a></p>'
                "<p>Наші менеджери зв'яжуться з вами в самий найближчий час</p>"
            ),
            "en": (
                "<p>If you have no objections or requests to change the standard agreement "
                f'with Led leader, please sign it and send it to us at '
                f'<a href="mailto:{email_partner}">{email_partner}</a></p>'
                "<p>Our managers will contact you as soon as possible</p>"
            ),
        },
        PageContent.PARTNERS_BECOME_CAREERS: {
            "uk": (
                "<p>Вибачте, зараз немає відкритих вакансій в нашій компанії</p>"
                f'<p>Надсилайте своє резюме на електронну пошту, із зазначенням посади: '
                f'<a href="mailto:{email_hr}">{email_hr}</a></p>'
            ),
            "en": (
                "<p>Sorry, there are currently no open vacancies at our company</p>"
                f'<p>Send your CV to our email, indicating the desired position: '
                f'<a href="mailto:{email_hr}">{email_hr}</a></p>'
            ),
        },
        PageContent.PARTNERS_SERVICE_INTRO: {
            "uk": (
                "<p>Гарантійний термін на пропоновані телефони: 1 – 12 і 36 місяців.</p>"
                "<p>Гарантію на товар терміном 1 місяць надає Сервісний Центр Led leader.</p>"
            ),
            "en": (
                "<p>Warranty period for offered phones: 1 – 12 and 36 months.</p>"
                "<p>A 1-month product warranty is provided by the Led leader Service "
                "Centre.</p>"
            ),
        },
        PageContent.PARTNERS_SERVICE_TERMS: {
            "uk": (
                "<p>1. Сервісний Центр Led leader здійснює гарантійне обслуговування "
                "абонентського стільникового обладнання відповідно до умов договорів з "
                "фірмами-виробниками або постачальниками обладнання. Власник обладнання "
                "має право на гарантійне обслуговування обладнання в разі якщо:</p>"
                "<ul>"
                "<li>Термін гарантійних зобов'язань не закінчився.</li>"
                "<li>IMEI, модель, колір і комплектація відповідають даним бази проданих "
                "телефонів, що знаходяться на гарантії.</li>"
                "<li>Несправність у роботі обладнання виникла не через недбалість "
                "Власника.</li>"
                "<li>Чи не була наслідком використання обладнання не за призначенням або "
                "не у відповідності з правилами експлуатації.</li>"
                "<li>Чи не виникла при впливі на обладнання вологи або рідини.</li>"
                "<li>Не стала наслідком попадання всередину обладнання інших речовин і "
                "істот.</li>"
                "<li>Чи не була наслідком інших порушень правил експлуатації.</li>"
                "</ul>"
                "<p>2. Використання аксесуарів, не дозволених фірмою-виробником, може "
                "вивести обладнання з ладу, і є порушенням правил експлуатації, яке "
                "позбавляє законної сили будь-які гарантії на обладнання.</p>"
                "<p>3. Гарантія на обладнання втрачається при спробі його розтину або "
                "ремонту в іншому сервісному центрі.</p>"
                "<p>4. Максимальний термін гарантійного ремонту обладнання – 14 робочих "
                "днів з дня звернення до Сервісного центру Led leader.</p>"
                "<p>Гарантія 12 – 36 місяців надається на оригінальні, сертифіковані "
                "Укрчастотнаглядом UA UCRF; з гарантією 12 – 36 місяців від представництв "
                "фірм-виробників. Обслуговування проводиться у відповідних авторизованих "
                "цими фірмами сервіс-центрах.</p>"
            ),
            "en": (
                "<p>1. The Led leader Service Centre provides warranty service for "
                "subscriber mobile equipment in accordance with agreements with "
                "manufacturers or equipment suppliers. The equipment owner is entitled to "
                "warranty service if:</p>"
                "<ul>"
                "<li>The warranty period has not expired.</li>"
                "<li>The IMEI, model, colour and configuration match the records in the "
                "database of phones under warranty.</li>"
                "<li>The malfunction was not caused by the Owner's negligence.</li>"
                "<li>Was not the result of using the equipment for purposes other than "
                "intended or contrary to the operating rules.</li>"
                "<li>Did not arise from exposure to moisture or liquid.</li>"
                "<li>Was not caused by the entry of foreign substances or objects into the "
                "equipment.</li>"
                "<li>Was not the result of any other violations of the operating rules.</li>"
                "</ul>"
                "<p>2. The use of accessories not approved by the manufacturer may damage "
                "the equipment and constitutes a violation of operating rules that voids "
                "all warranties on the equipment.</p>"
                "<p>3. The warranty is void if the equipment is opened or repaired by any "
                "other service centre.</p>"
                "<p>4. The maximum warranty repair period is 14 business days from the date "
                "of contacting the Led leader Service Centre.</p>"
                "<p>A 12–36 month warranty is provided on original equipment certified by "
                "the Ukrainian State Centre of Radio Frequencies (UA UCRF), with a 12–36 "
                "month warranty from manufacturer representatives. Service is carried out "
                "at authorised service centres designated by the respective "
                "manufacturers.</p>"
            ),
        },
        PageContent.PARTNERS_SERVICE_KIT: {
            "uk": (
                "<ul>"
                "<li>мобільний телефон, батарейка, зарядний пристрій;</li>"
                "<li>оригінальна коробка;</li>"
                "<li>інструкція;</li>"
                "<li>гарантійний талон з адресами і телефонами сервіс-центрів, які "
                "виробляють безкоштовне гарантійне обслуговування.</li>"
                "</ul>"
            ),
            "en": (
                "<ul>"
                "<li>mobile phone, battery, charger;</li>"
                "<li>original box;</li>"
                "<li>instruction manual;</li>"
                "<li>warranty card with addresses and phone numbers of service centres "
                "providing free warranty service.</li>"
                "</ul>"
            ),
        },
    }
