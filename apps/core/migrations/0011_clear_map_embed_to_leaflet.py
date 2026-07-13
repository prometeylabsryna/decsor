"""Data migration: очищає map_embed_code щоб сторінки використовували Leaflet-карту."""
from django.db import migrations


def clear_map_embed(apps, schema_editor):
    SiteSettings = apps.get_model("core", "SiteSettings")
    SiteSettings.objects.update(map_embed_code="")


def restore_map_embed(apps, schema_editor):
    EMBED = (
        '<iframe src="https://maps.google.com/maps?q=Kyiv,+Ukraine&z=5&output=embed"'
        ' width="600" height="450" style="border:0;"'
        ' allowfullscreen="" loading="lazy"'
        ' referrerpolicy="strict-origin-when-cross-origin"></iframe>'
    )
    SiteSettings = apps.get_model("core", "SiteSettings")
    SiteSettings.objects.update(map_embed_code=EMBED)


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0010_alter_sitesettings_map_embed_code"),
    ]

    operations = [
        migrations.RunPython(clear_map_embed, reverse_code=restore_map_embed),
    ]
