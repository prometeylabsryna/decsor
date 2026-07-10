from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="newsarticle",
            name="category",
            field=models.CharField(
                choices=[("market", "Новини ринку"), ("company", "Новини Led leader")],
                default="market",
                max_length=20,
                verbose_name="Категорія",
            ),
        ),
    ]
