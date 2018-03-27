from django.http import JsonResponse
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from django.contrib.auth import authenticate, login
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.parsers import JSONParser
from api.models import ClientAnketa, CreditOrg, Partner, ZayavkiCreditOrg, Predlogenie
from django.core import serializers
from django.contrib.auth.models import User
from django.core.exceptions import FieldError, ObjectDoesNotExist
import json
import datetime
import uuid
from asynctasks.tasks import send_request_credit_org


class GroupPartnerPermisions(permissions.BasePermission):
    """
        Проверяем находится ли пользователь в группе partner_group
    """
    def has_permission(self, request, view):
        
        if request.user.is_authenticated() and request.user.is_superuser:
            return True
        
        elif request.user.is_authenticated():
            # Проверяем если пользователь в группе partner_group
            try:
                request.user.groups.get(name="partner_group")
                return True
            except ObjectDoesNotExist:
                return False
            
        else:
            return False


class GroupCreditPermisions(permissions.BasePermission):
    """
        Проверяем находится ли пользователь в группе credit_group
    """

    def has_permission(self, request, view):

        if request.user.is_authenticated() and request.user.is_superuser:
            return True

        elif request.user.is_authenticated():
            # Проверяем если пользователь в группе credit_group
            try:
                request.user.groups.get(name="credit_group")
                return True
            except ObjectDoesNotExist:
                return False

        else:
            return False


class PartnerView(APIView):
    """
        Получение списка анкет, с сортировкой и фильтрами.Фильрация может происходить по любому из полей. Пример фильтра:
           {
            "name": "test",
            "surname": "test",
            "lastname": "test",
            "birthday": "2018-03-21",
            "telephone": "89168094164",
            "passport_num": "kjahsd2384y32894",
            "score_bal": 34.0
          }
        Просмотр анкеты по id
    """

    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated,GroupPartnerPermisions)

    def post(self, request):
        _filter = request.data
        try:
            partner = Partner.objects.get(username=request.user)
            qs = ClientAnketa.objects.filter(
                partner=partner,
                **_filter
            ).order_by('id')
            response_data = serializers.serialize('json', qs)
        except FieldError as err:
            response_data = json.dumps({"status": str(err)})
            return HttpResponse(response_data, content_type='application/json', status=status.HTTP_400_BAD_REQUEST)
        return HttpResponse(response_data, content_type='application/json', status=status.HTTP_200_OK)


class PartnerCreateAnketa(APIView):
    """
        Создание анкеты происходит при помощи отправки POST запроса в формате json.
        Пример запроса:
        {
            "name": "Сидор",
            "surname": "Петрович",
            "lastname": "Иванов",
            "birthday": "2018-03-21",
            "telephone": "89168094164",
            "passport_num": "kjahsd2384y32894",
            "score_bal": 34.0
        }
    """

    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, GroupPartnerPermisions)

    def post(self, request):

        _filter = request.data
        try:
            partner = Partner.objects.get(username=request.user)
            ClientAnketa(
                partner=partner,
                **_filter
            ).save()
        except Exception as err:
            response_data = json.dumps({"status": str(err)})
            return HttpResponse(response_data, content_type='application/json', status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({"status":"created"}, status=status.HTTP_201_CREATED)


class PartnerViewCreditOrgs(APIView):
    """
        Возможность для партнеров просмотра кредитных организаций, 
        чтобы партнеры знали о перечне организаций, которым можно отправить
        заявку на рассмотрение.
        С сортировкой и фильтрацией.
    """
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, GroupPartnerPermisions)

    def post(self, request):
        """

        :param request:
        :return:
        """
        _filter = request.data
        try:
            qs = CreditOrg.objects.filter(
                **_filter
            ).order_by('id')
            response_data = serializers.serialize('json', qs)
        except FieldError as err:
            response_data = json.dumps({"status": str(err)})
            return HttpResponse(response_data, content_type='application/json', status=status.HTTP_400_BAD_REQUEST)
        return HttpResponse(response_data, content_type='application/json', status=status.HTTP_200_OK)


class PartnerCreateZayavka(APIView):
    """
        Предоставление API интерфейса для партнеров по созданию заявки 
        в кредитную организацию.
        Для создания заявки партнер должен знать id анкеты,  name кредитной организации и
        тип кредита type_of в которую собирается отправить заявку на рассмотрение.
        Тип кредита может быть нескольких типов:
            'P' = 'Потребительский'
            'I' = 'Ипотека'
            'A' = 'Автокредит'
        
        Формат запроса по созданию заявки:
            {
                "type_of":"P",
                "start_rotate":"2018-03-23 20:20:20",
                "end_rotate":"2018-03-24 20:20:20",
                "min_scoring":"1.0",
                "max_scoring":"5.0",
                "credit_org":"Кредитная организация2",
                "passport_num":"234sd345435sdfdsf24"
            }
    """
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, GroupPartnerPermisions) 
    
    def post(self, request):
        
        _data = request.data
        partner = Partner.objects.get(username=request.user)
        # Определяем тип кредита.
        try:
            type_of = _data['type_of']
        except Exception as err:
            response_data = json.dumps({"status": str(err) + ' not correct'})
            return HttpResponse(response_data, content_type='application/json', status=status.HTTP_400_BAD_REQUEST)
        
        # По номеру паспорта находим анкету тк он уникален.
        try:
            passport_num = _data['passport_num']
            
            _client_anketa = ClientAnketa.objects.get(
                partner=partner,
                passport_num=passport_num
            )
        except ClientAnketa.DoesNotExist:
            response_data = json.dumps({"status":'There is no Client Ankent with this passport num for this partner'})
            return HttpResponse(response_data, content_type='application/json', status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as err:
            response_data = json.dumps({"status": str(err) + ' not correct'})
            return HttpResponse(response_data, content_type='application/json', status=status.HTTP_400_BAD_REQUEST)

        # Находим кредитную организацию для которой формируется заявка.
        try:
            credit_org = CreditOrg.objects.get(name=_data['credit_org'])
        except CreditOrg.DoesNotExist:    
            response_data = json.dumps({"status":'There is no Credit org with this name'})
            return HttpResponse(response_data, content_type='application/json', status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as err:
            response_data = json.dumps({"status": str(err) + ' not correct'})
            return HttpResponse(response_data, content_type='application/json', status=status.HTTP_400_BAD_REQUEST)
            
        # Определяем дату начала ротации
        try:
            start_rotate = datetime.datetime.strptime(_data['start_rotate'], "%Y-%m-%d %H:%M:%S")
        except Exception as err:
            response_data = json.dumps({"status": str(err) + ' not correct'})
            return HttpResponse(response_data, content_type='application/json', status=status.HTTP_400_BAD_REQUEST)

        # Определяем дату конца ротации
        try:
            end_rotate = datetime.datetime.strptime(_data['end_rotate'], "%Y-%m-%d %H:%M:%S")
        except Exception as err:
            response_data = json.dumps({"status": str(err) + ' not correct'})
            return HttpResponse(response_data, content_type='application/json', status=status.HTTP_400_BAD_REQUEST)
        
        # Получаем минимальный скорринговый бал.
        try:
            min_scoring = _data['min_scoring']
        except Exception as err:
            response_data = json.dumps({"status": str(err) + ' not correct'})
            return HttpResponse(response_data, content_type='application/json', status=status.HTTP_400_BAD_REQUEST)
        
        # Получаем максимальный скоринговый бал.
        try:
            max_scoring = _data['max_scoring']
        except Exception as err:
            response_data = json.dumps({"status": str(err) + ' not correct'})
            return HttpResponse(response_data, content_type='application/json', status=status.HTTP_400_BAD_REQUEST)
        
        # Формируем предложение.
        try:
            name = str(uuid.uuid4())
            _predlogenie = Predlogenie.objects.create(
                start_rotate=start_rotate,
                end_rotate=end_rotate,
                name = name,
                type_of=type_of,
                min_scoring=min_scoring,
                max_scoring=max_scoring,
                credit_org=credit_org
            )
            
            # Формируем заявку на основании предложения.
            zayavka = ZayavkiCreditOrg.objects.create(
                client_anketa=_client_anketa,
                predlogenie=_predlogenie,
                status='NEW'
            )
            
            return JsonResponse({"status": "created"}, status=status.HTTP_201_CREATED)
        
        except Exception as err:
            response_data = json.dumps({"status": str(err)})
            return HttpResponse(response_data, content_type='application/json', status=status.HTTP_400_BAD_REQUEST)        


class PartnerViewZayavka(APIView):
    """
        Возможность просмотра заявок для партнера.
    """
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, GroupPartnerPermisions)
    def post(self, request):
        _filter = request.data
        qs = []
        try:
            partner = Partner.objects.get(username=request.user)
            clients_ankets = ClientAnketa.objects.filter(
                partner=partner,
            )
            
            print(clients_ankets)
            for client_anketa in clients_ankets:

                zayavki = ZayavkiCreditOrg.objects.filter(
                    client_anketa=client_anketa.id
                )
                for zayavka in zayavki:
                    qs.append(zayavka)
                
            response_data = serializers.serialize('json', qs)
            return HttpResponse(response_data, content_type='application/json', status=status.HTTP_200_OK)
        
        except Exception as err:
            response_data = json.dumps({"status": str(err)})
            return HttpResponse(response_data, content_type='application/json', status=status.HTTP_400_BAD_REQUEST)         
        
        


# class PartnerSendAnketa(APIView):
#     """
#         Отправка партнерами анкеты в кредитные организации.
#     """
# 
#     authentication_classes = (TokenAuthentication, )
#     permission_classes = (IsAuthenticated, GroupPartnerPermisions)
# 
#     def post(self, request):
# 
#         if request.data.get('id'):
# 
#             try:
#                 partner = Partner.objects.get(username=request.user)
#                 ClientAnketa.objects.get(partner=partner, id=request.data['id'])
#                 send_request_credit_org.delay(anketa=json.dumps({"id": request.data['id']}))
#                 response_data = json.dumps({"status": "Заявка отправлена на рассмотрение"})
#                 return HttpResponse(response_data, content_type='application/json', status=status.HTTP_200_OK)
# 
#             except ClientAnketa.DoesNotExist:
# 
#                 response_data = json.dumps({"status": "нет анкеты с указанным id"})
#                 return HttpResponse(response_data, content_type='application/json', status=status.HTTP_200_OK)
# 
#         else:
# 
#             response_data = json.dumps({"status": "не указан id анкеты"})
#             return HttpResponse(response_data, content_type='application/json', status=status.HTTP_400_BAD_REQUEST)


class CreditOrgView(APIView):
    """
        Просмотр кредитных заявок для кредитных организаций.
    """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, GroupCreditPermisions )

    def post(self, request):
        _filter = request.data
        try:
            credit_org = CreditOrg.objects.get(username = request.user)
            qs = CreditOrg.objects.filter(**_filter).order_by('id')
            response_data = serializers.serialize('json', qs)
        except FieldError:
            response_data = json.dumps({"status": "не корректный запрос"})
        return HttpResponse(response_data, content_type='application/json')


class Obtain_auth_token(APIView):

    permission_classes = (AllowAny,)
    authentication_classes = (BasicAuthentication,)

    def post(self, request):

        try:
            username = request.data['username']
            password = request.data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                u = User.objects.get(username=user)
                token = Token.objects.filter(user=u)
                if len(token) == 0:
                    token = Token.objects.create(user=u)
                else:
                    token = Token.objects.get(user=u)
                result = json.dumps({"token": token.key })
                return HttpResponse(result, content_type='application/json')
            else:
                return HttpResponse(status=status.HTTP_401_UNAUTHORIZED, content_type='application/json')

        except Exception as err:
            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED, content_type='application/json')