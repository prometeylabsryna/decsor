"""Template context processors for apps.core."""

from apps.core.models import PageContent, SiteSettings


def site_settings(request):
    page_content = {pc.page: pc.body for pc in PageContent.objects.all()}
    return {
        "site_settings": SiteSettings.get_solo(),
        "page_content": page_content,
    }
