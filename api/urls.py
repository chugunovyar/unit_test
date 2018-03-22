from django.conf.urls import url, include
from api import views

urlpatterns = [
    url(r'^partners_view/', views.PartnerView.as_view()),
    url(r'^partners_create_query/', views.PartnerCreateQuery.as_view()),
    url(r'^credit_org/', views.CreditOrgView.as_view())
]