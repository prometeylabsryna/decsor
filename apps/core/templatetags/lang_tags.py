"""Custom template tags for language URL switching."""
from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def lang_url(context, lang_code: str) -> str:
    """Return the current full path switched to the given language code.

    Assumes i18n_patterns with prefix_default_language=False:
      - 'uk' paths have no /en/ prefix  (e.g. /novyny/)
      - 'en' paths have /en/ prefix      (e.g. /en/novyny/)
    """
    request = context.get("request")
    if request is None:
        return "/"

    full_path = request.get_full_path()

    if lang_code == "uk":
        if full_path.startswith("/en/"):
            return full_path[3:]
        if full_path == "/en":
            return "/"
        return full_path

    if lang_code == "en":
        if full_path.startswith("/en"):
            return full_path
        return "/en" + full_path

    return full_path


@register.filter
def split_brand_title(title: str) -> list[str]:
    """Split hero title into [brand, tagline] on em dash, or [title] if no separator."""
    if " — " in title:
        return title.split(" — ", 1)
    return [title]
