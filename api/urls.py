from django.conf.urls import url, include
from api import views

urlpatterns = [
    url(r'^partners_view/', views.PartnerView.as_view()),
    url(r'^partners_create_anketa/', views.PartnerCreateAnketa.as_view()),
    url(r'^partners_send_zayavka/', views.PartnerSendZayavka.as_view()),
    url(r'^partners_view_creditorgs/', views.PartnerViewCreditOrgs.as_view()),
    url(r'^partners_create_zayavka/', views.PartnerCreateZayavka.as_view()),
    url(r'^partners_view_zayavka/', views.PartnerViewZayavka.as_view()),
    url(r'^credit_org/', views.CreditOrgView.as_view()),
    url(r'^creditorg_update_status/', views.CreditOrgUpdateStatus.as_view())
]
