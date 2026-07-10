"""Template tags for contact links."""
from django import template

register = template.Library()


@register.filter
def tel_href(phone: str) -> str:
    """Convert display phone to tel: href (digits and leading + only)."""
    if not phone:
        return ""
    cleaned = "".join(ch for ch in phone if ch.isdigit() or ch == "+")
    return cleaned or phone
