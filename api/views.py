from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.parsers import JSONParser



class PartnerView(APIView):
    """
        Возможность просматривать анкеты и заявки.
    """
    def get(self, request):
        pass
        return JsonResponse({"status":"ok"})


class CreditOrgView(APIView):
    """
        Просмотр кредитных заявок для кредитных организаций.
    """
    def get(self, request):
        pass
        return JsonResponse({"status":"ok"})