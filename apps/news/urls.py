"""URL patterns for the news app."""
from django.urls import re_path

from apps.news.views import NewsListView, NewsDetailView

app_name = "news"

urlpatterns = [
    re_path(r"^$", NewsListView.as_view(), name="list"),
    re_path(r"^(?P<slug>[-\w]+)/$", NewsDetailView.as_view(), name="detail"),
]
