from django.db import migrations


class Migration(migrations.Migration):
    """No-op: source_url already added in 0003."""

    dependencies = [
        ("news", "0003_newsarticle_content_en_newsarticle_content_uk_and_more"),
    ]

    operations = []
