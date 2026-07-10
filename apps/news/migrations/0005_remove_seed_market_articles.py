from django.db import migrations

SEED_MARKET_SLUGS = [
    "powerbank-wireless-charging",
    "zte-axon-9-pro",
    "apple-presentation-2018",
    "edison-transatlantic-call",
    "samsung-galaxy-note-9",
    "5g-real-speeds",
    "google-duplex-calls",
    "microsoft-surface-phone-foldable",
]


def remove_seed_market_articles(apps, schema_editor):
    NewsArticle = apps.get_model("news", "NewsArticle")
    NewsArticle.objects.filter(
        category="market",
        slug__in=SEED_MARKET_SLUGS,
        source_url="",
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("news", "0004_newsarticle_source_url"),
    ]

    operations = [
        migrations.RunPython(remove_seed_market_articles, migrations.RunPython.noop),
    ]
