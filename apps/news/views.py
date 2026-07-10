"""Views for the news app."""
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, DetailView

from apps.news.models import NewsArticle


class NewsListView(ListView):
    model = NewsArticle
    template_name = "news/list.html"
    context_object_name = "articles"
    paginate_by = 9

    def get_queryset(self):
        qs = NewsArticle.objects.filter(is_published=True).order_by("-published_at")
        cat = self.request.GET.get("cat")
        if cat in (NewsArticle.CATEGORY_MARKET, NewsArticle.CATEGORY_COMPANY):
            qs = qs.filter(category=cat)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["active_cat"] = self.request.GET.get("cat", "")
        ctx["page_title"] = _("Новини")
        ctx["featured_article"] = None
        if ctx["active_cat"] == NewsArticle.CATEGORY_MARKET:
            ctx["page_title"] = _("Новини ринку")
        elif ctx["active_cat"] == NewsArticle.CATEGORY_COMPANY:
            ctx["page_title"] = _("Новини компанії")
            ctx["featured_article"] = (
                NewsArticle.objects.filter(
                    is_published=True,
                    category=NewsArticle.CATEGORY_COMPANY,
                    slug="led-leader-tsyfrove-obladnannia",
                ).first()
            )
        return ctx


class NewsDetailView(DetailView):
    model = NewsArticle
    template_name = "news/detail.html"
    context_object_name = "article"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return NewsArticle.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["related"] = (
            NewsArticle.objects.filter(is_published=True)
            .exclude(pk=self.object.pk)
            .order_by("-published_at")[:4]
        )
        return ctx
