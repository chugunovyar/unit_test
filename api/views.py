from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.parsers import JSONParser
from api.models import ClientAnketa, CreditOrg
from django.core import serializers
from django.core.exceptions import FieldError
import json
from asynctasks.tasks import send_request_credit_org


class PartnerView(APIView):
    """
        Получение списка анкет, с сортировкой и фильтрами.
        Просмотр анкеты по id
    """
    def post(self, request):
        _filter = request.data
        try:
            qs = ClientAnketa.objects.filter(**_filter).order_by('id')
            response_data = serializers.serialize('json', qs)
        except FieldError:
            response_data = json.dumps({"status": "не корректный запрос"})
        return HttpResponse(response_data, content_type='application/json')


class PartnerCreateAnketa(APIView):
    """
        создание анкеты
    """
    def post(self, request):

        _filter = request.data
        try:
            ClientAnketa(**_filter).save()
        except Exception as err:
            print(err)
        return JsonResponse({"status":"1"})


class PartnerSendAnketa(APIView):
    """
        Отправка партнерами анкеты в кредитные организации.
    """
    def post(self, request):

        if request.data.get('id'):

            try:

                ClientAnketa.objects.get(id=request.data['id'])
                send_request_credit_org.delay(anketa=json.dumps({"id": request.data['id']}))

            except ClientAnketa.DoesNotExist:

                response_data = json.dumps({"status": "нет анкеты по указанному фильтру"})

            return HttpResponse(response_data, content_type='application/json')

        else:

            response_data = json.dumps({"status": "не указан id анкеты"})
            return HttpResponse(response_data, content_type='application/json')


class CreditOrgView(APIView):
    """
        Просмотр кредитных заявок для кредитных организаций.
    """
    def post(self, request):
        _filter = request.data
        try:
            qs = CreditOrg.objects.filter(**_filter).order_by('id')
            response_data = serializers.serialize('json', qs)
        except FieldError:
            response_data = json.dumps({"status": "не корректный запрос"})
        return HttpResponse(response_data, content_type='application/json')