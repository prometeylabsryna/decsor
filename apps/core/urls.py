"""URL patterns for the core app."""
from django.urls import path

from apps.core.views import (
    HomeView,
    AboutView,
    CooperationView,
    FaqView,
    DeliveryView,
    DeliveryOrderView,
    DeliveryTransportView,
    PartnersView,
    PartnersProgramView,
    PartnersBecomeView,
    PartnersServiceView,
    ContactsView,
)

app_name = "core"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("pro-kompaniyu/", AboutView.as_view(), name="about"),
    path("pro-kompaniyu/spivpratsia/", CooperationView.as_view(), name="cooperation"),
    path("pro-kompaniyu/faq/", FaqView.as_view(), name="faq"),
    path("dostavka/", DeliveryView.as_view(), name="delivery"),
    path("dostavka/zamovlennia-ta-oplata/", DeliveryOrderView.as_view(), name="delivery-order"),
    path("dostavka/transportni-kompanii/", DeliveryTransportView.as_view(), name="delivery-transport"),
    path("partnery/", PartnersView.as_view(), name="partners"),
    path("partnery/prohrama/", PartnersProgramView.as_view(), name="partners-program"),
    path("partnery/staty-partnerom/", PartnersBecomeView.as_view(), name="partners-become"),
    path("partnery/servis-ta-harantiia/", PartnersServiceView.as_view(), name="partners-service"),
    path("kontakty/", ContactsView.as_view(), name="contacts"),
]
