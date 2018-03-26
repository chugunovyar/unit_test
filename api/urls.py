from django.conf.urls import url, include
from api import views

urlpatterns = [
    url(r'^partners_view/', views.PartnerView.as_view()),
    url(r'^partners_create_anketa/', views.PartnerCreateAnketa.as_view()),
    url(r'^partners_send_anketa/', views.PartnerSendAnketa.as_view()),
    url(r'^partners_view_creditorgs/', views.PartnerViewCreditOrgs.as_view()),
    url(r'^credit_org/', views.CreditOrgView.as_view())
]