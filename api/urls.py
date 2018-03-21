from django.conf.urls import url, include
from api import views

urlpatterns = [
    url(r'^parners/', views.PartnerView.as_view()),
    url(r'^credit_org/', views.CreditOrgView.as_view())
]