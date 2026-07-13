"""Data migration: оновлює map_embed_code в SiteSettings на карту Європи з піном на Києві."""
from django.db import migrations

NEW_EMBED = (
    '<iframe src="https://maps.google.com/maps?q=Kyiv,+Ukraine&z=5&output=embed"'
    ' width="600" height="450" style="border:0;"'
    ' allowfullscreen="" loading="lazy"'
    ' referrerpolicy="strict-origin-when-cross-origin"></iframe>'
)


def update_map_embed(apps, schema_editor):
    SiteSettings = apps.get_model("core", "SiteSettings")
    SiteSettings.objects.update(map_embed_code=NEW_EMBED)


def reverse_map_embed(apps, schema_editor):
    OLD_EMBED = (
        '<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d20328.566181121325'
        '!2d30.5007107!3d50.4397824!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2'
        '!1s0x40d4ce88e35e395f%3A0xc63774cf5da5a434!2z0KHQvtGE0LjQudGB0LrQuNC5INGB0L7QsdC-0YA'
        '!5e0!3m2!1sru!2sua!4v1783689698284!5m2!1sru!2sua" width="600" height="450" style="border:0;" '
        'allowfullscreen="" loading="lazy" referrerpolicy="strict-origin-when-cross-origin"></iframe>'
    )
    SiteSettings = apps.get_model("core", "SiteSettings")
    SiteSettings.objects.update(map_embed_code=OLD_EMBED)


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0007_faqitem_internalextension_pagecontent_partnerregion_and_more"),
    ]

    operations = [
        migrations.RunPython(update_map_embed, reverse_code=reverse_map_embed),
    ]
