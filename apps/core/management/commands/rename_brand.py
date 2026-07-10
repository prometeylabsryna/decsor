"""Replace legacy brand name (Дексор / Dexor / Deksor) with Led leader in the database."""
from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import models

# Order matters: longer / uppercase variants first.
_REPLACEMENTS = (
    ("DEKSOR", "LED LEADER"),
    ("ДЕКСОР", "LED LEADER"),
    ("Deksor", "Led leader"),
    ("Dexor", "Led leader"),
    ("Дексор", "Led leader"),
    ("deksor", "led-leader"),
)


def replace_brand(text: str) -> str:
    if not text:
        return text
    for old, new in _REPLACEMENTS:
        text = text.replace(old, new)
    return text


class Command(BaseCommand):
    help = "Replace Дексор/Dexor/Deksor with Led leader in all stored content."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show changes without saving.",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        updated_rows = 0
        updated_fields = 0

        for model in apps.get_models():
            if model._meta.app_label not in ("core", "news"):
                continue

            text_fields = [
                f
                for f in model._meta.get_fields()
                if isinstance(f, (models.CharField, models.TextField, models.SlugField))
                and not f.auto_created
            ]
            if not text_fields:
                continue

            for obj in model.objects.all():
                changed = {}
                for field in text_fields:
                    value = getattr(obj, field.name, None)
                    if not value or not isinstance(value, str):
                        continue
                    new_value = replace_brand(value)
                    if new_value != value:
                        changed[field.name] = new_value

                if not changed:
                    continue

                updated_rows += 1
                for name, new_value in changed.items():
                    updated_fields += 1
                    old_value = getattr(obj, name)
                    self.stdout.write(
                        f"  {model._meta.label}.{name} pk={obj.pk}: "
                        f"{old_value[:60]!r} → {new_value[:60]!r}"
                    )
                    if not dry_run:
                        setattr(obj, name, new_value)

                if not dry_run:
                    obj.save()

        slug_fixes = self._fix_news_slugs(dry_run)
        updated_fields += slug_fixes

        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    f"Dry run: {updated_rows} row(s), {updated_fields} field(s) would change."
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Updated {updated_rows} row(s), {updated_fields} field(s)."
                )
            )

    def _fix_news_slugs(self, dry_run: bool) -> int:
        """Ensure featured article slug matches views.py after rename."""
        from apps.news.models import NewsArticle

        slug_map = {
            "deksor-tsyfrove-obladnannia": "led-leader-tsyfrove-obladnannia",
            "deksor-assortment-2019": "led-leader-assortment-2019",
            "deksor-gsmexchange": "led-leader-gsmexchange",
        }
        count = 0
        for old, new in slug_map.items():
            article = NewsArticle.objects.filter(slug=old).first()
            if not article:
                continue
            if NewsArticle.objects.filter(slug=new).exclude(pk=article.pk).exists():
                self.stdout.write(
                    self.style.WARNING(f"  Skip slug {old!r}: {new!r} already taken.")
                )
                continue
            self.stdout.write(f"  NewsArticle.slug pk={article.pk}: {old!r} → {new!r}")
            count += 1
            if not dry_run:
                article.slug = new
                article.save(update_fields=["slug"])
        return count
