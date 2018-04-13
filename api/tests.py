from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from api.views import Obtain_auth_token, PartnerCreateAnketa, PartnerView, \
    PartnerCreateZayavka, PartnerSendZayavka,\
    CreditOrgView, CreditOrgUpdateStatus
from api.models import Partner, CreditOrg, ClientAnketa, Predlogenie,\
    ZayavkiCreditOrg
import json
import time
from celery.result import AsyncResult


class Test_Partner_Api(TestCase):
    """
        Тестирование API для партнеров.
    """
    def setUp(self):
        """
            Наполняем базу данных фикстурами для тестирования:
                1. Создаем партнеров.
                2. Создаем кредитные организации.
                3. Создаем группы и добавляем туда пользователей.

        :return:
        """
        # Создаем пользователей и группы
        self.create_users_and_groups()
        self.factory = APIRequestFactory()
        # Запускаем метод из setUp метода потому что хотим чтобы токены
        #  для пользователей были
        # доступны по всему классу. Одновременно проверяем работы
        #  API по авторизации и
        # выдаче токенов.
        self.test_get_token()

    def test_get_token(self):
        """
            Тестирование функционала выдачи токенов для пользователей.
        :return:
        """

        # Проверка получения для первого партнера
        request = self.factory.post('/api-token-auth/',
                                    json.dumps(self.partner_auth),
                                    content_type='application/json')
        view = Obtain_auth_token.as_view()
        force_authenticate(request, user=self.partner_user)
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.partner_user_token = json.loads(response.content)['token']
        self.assertGreater(len(self.partner_user_token), 1)

        # Проверка получения токена для второго партнера
        request = self.factory.post('/api-token-auth/',
                                    json.dumps(self.partner_auth2),
                                    content_type='application/json')
        view = Obtain_auth_token.as_view()
        force_authenticate(request, user=self.partner_user2)
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.partner_user_token2 = json.loads(response.content)['token']
        self.assertGreater(len(self.partner_user_token2), 1)

        # Проверка получения токена для кредитной организации 1
        request = self.factory.post('/api-token-auth/',
                                    json.dumps(self.credit_auth),
                                    content_type='application/json')
        view = Obtain_auth_token.as_view()
        force_authenticate(request, user=self.credit_user)
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.credit_user_token = json.loads(response.content)['token']
        self.assertGreater(len(self.credit_user_token), 1)

        # Проверка получения токена для кредитной организации 2
        request = self.factory.post('/api-token-auth/',
                                    json.dumps(self.credit_auth2),
                                    content_type='application/json')
        view = Obtain_auth_token.as_view()
        force_authenticate(request, user=self.credit_user2)
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.credit_user_token2 = json.loads(response.content)['token']
        self.assertGreater(len(self.credit_user_token2), 1)

    def test_partner_api(self):
        """
            Тестирование API для партнеров.
            1. Создание анкет.
            2. Просмотр анкет с фильтрами.
            3. Тестирование того, что пользователи не входящие
            в группу партнеров не могут получить доступ
            к API предназначенного для партнеров.
        :return:
        """
        _anketa1 = {
            "name": "Сидор",
            "surname": "Петрович",
            "lastname": "Иванов",
            "birthday": "2018-03-21",
            "telephone": "111111111111",
            "passport_num": "kjahsd2384y32894",
            "score_bal": 34.0
        }
        request = self.factory.post('/api/partners_create_anketa/',
                                    json.dumps(_anketa1),
                                    content_type='application/json')
        force_authenticate(request, user=self.partner_user,
                           token=self.partner_user_token)
        view = PartnerCreateAnketa.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 201)
        status = json.loads(response.content)['status']
        self.assertEqual(status, 'created')

        _anketa2 = {
            "name": "Иван",
            "surname": "Иванович",
            "lastname": "Иванов",
            "birthday": "2018-04-21",
            "telephone": "222222222222",
            "passport_num": "kjahsd23834534",
            "score_bal": 3.0
        }
        request = self.factory.post('/api/partners_create_anketa/',
                                    json.dumps(_anketa2),
                                    content_type='application/json')
        force_authenticate(request,
                           user=self.partner_user,
                           token=self.partner_user_token)
        view = PartnerCreateAnketa.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 201)
        status = json.loads(response.content)['status']
        self.assertEqual(status, 'created')
        # Проверяем что созданы две анкеты для этого партнера.
        _partner = Partner.objects.get(username=self.partner_user)
        ankets = ClientAnketa.objects.filter(partner=_partner)
        self.assertEqual(len(ankets), 2)
        self.assertEqual(ankets[0].name, 'Сидор')
        self.assertEqual(ankets[0].partner.name, self.partner_auth['username'])
        self.assertEqual(ankets[1].name, 'Иван')
        self.assertEqual(ankets[1].partner.name, self.partner_auth['username'])
        ############################################################
        # Создаем анкеты для второго партнера.
        ############################################################
        _anketa1 = {
            "name": "Николай",
            "surname": "Петрович",
            "lastname": "Петров",
            "birthday": "2018-03-21",
            "telephone": "111111111111",
            "passport_num": "kj234ahs23484y32894",
            "score_bal": 5.0
        }
        request = self.factory.post('/api/partners_create_anketa/',
                                    json.dumps(_anketa1),
                                    content_type='application/json')
        force_authenticate(request,
                           user=self.partner_user2,
                           token=self.partner_user_token2)
        view = PartnerCreateAnketa.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 201)
        status = json.loads(response.content)['status']
        self.assertEqual(status, 'created')

        _anketa2 = {
            "name": "Вася",
            "surname": "Иванович",
            "lastname": "Иванов",
            "birthday": "2018-04-21",
            "telephone": "222222222222",
            "passport_num": "kjahsd2383333",
            "score_bal": 3.0
        }
        request = self.factory.post('/api/partners_create_anketa/',
                                    json.dumps(_anketa2),
                                    content_type='application/json')
        force_authenticate(request,
                           user=self.partner_user2,
                           token=self.partner_user_token2)
        view = PartnerCreateAnketa.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 201)
        status = json.loads(response.content)['status']
        self.assertEqual(status, 'created')

        # Проверяем что созданы две анкеты для этого партнера.
        _partner = Partner.objects.get(username=self.partner_user2)
        ankets = ClientAnketa.objects.filter(partner=_partner)
        self.assertEqual(len(ankets), 2)
        self.assertEqual(ankets[0].name, 'Николай')
        self.assertEqual(ankets[0].partner.name,
                         self.partner_auth2['username'])
        self.assertEqual(ankets[1].name, 'Вася')
        self.assertEqual(ankets[1].partner.name,
                         self.partner_auth2['username'])

        # Проверка API партнеров для просмотра анкет клиентов пользователей,
        # с фильтрами.
        request = self.factory.post('/api/partners_view/',
                                    json.dumps({}),
                                    content_type='application/json')
        force_authenticate(request,
                           user=self.partner_user,
                           token=self.partner_user_token)
        view = PartnerView.as_view()
        response = view(request)
        _partner_answer = json.loads(response.content)
        # Убеждаемся в том что партнер видит только свои анкеты.
        self.assertEqual(len(_partner_answer), 2)
        self.assertEqual(_partner_answer[0]['fields']['name'], 'Сидор')
        self.assertEqual(_partner_answer[1]['fields']['name'], 'Иван')

        # Проверяем что фильтры для партнера 1, отрабатывают корректно
        request = self.factory.post('/api/partners_view/',
                                    json.dumps({"name": "Сидор"}),
                                    content_type='application/json')
        force_authenticate(request,
                           user=self.partner_user,
                           token=self.partner_user_token)
        view = PartnerView.as_view()
        response = view(request)
        _partner_answer = json.loads(response.content)
        # Убеждаемся в том что партнер видит только
        # одну анкету которую он выбрал
        # при помощи фильтра.
        self.assertEqual(len(_partner_answer), 1)
        self.assertEqual(_partner_answer[0]['fields']['name'], 'Сидор')

        # Проверка API партнеров для просмотра анкет
        # клиентов пользователей, с фильтрами.
        request = self.factory.post('/api/partners_view/',
                                    json.dumps({}),
                                    content_type='application/json')
        force_authenticate(request,
                           user=self.partner_user2,
                           token=self.partner_user_token2)
        view = PartnerView.as_view()
        response = view(request)
        _partner_answer = json.loads(response.content)
        # Убеждаемся в том что партнер видит только свои анкеты.
        self.assertEqual(len(_partner_answer), 2)
        self.assertEqual(_partner_answer[0]['fields']['name'], 'Николай')
        self.assertEqual(_partner_answer[1]['fields']['name'], 'Вася')

        # Проверяем что фильтры для партнера 2, отрабатывают корректно
        request = self.factory.post('/api/partners_view/',
                                    json.dumps({"name": "Николай"}),
                                    content_type='application/json')
        force_authenticate(request,
                           user=self.partner_user2,
                           token=self.partner_user_token2)
        view = PartnerView.as_view()
        response = view(request)
        _partner_answer = json.loads(response.content)
        # Убеждаемся в том что партнер видит только
        #  одну анкету которую он выбрал при помощи фильтра.
        self.assertEqual(len(_partner_answer), 1)
        self.assertEqual(_partner_answer[0]['fields']['name'], 'Николай')

        # Проверяем что пользователи не входящие
        #  в группу партнеров не могут получить
        # Доступ к API предназначенной для партнеров.
        # Проверка API для просмотра анкет.
        request = self.factory.post('/api/partners_view/',
                                    json.dumps({}),
                                    content_type='application/json')
        force_authenticate(request,
                           user=self.credit_user,
                           token=self.credit_user_token)
        view = PartnerView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 403)
        # Проверка API для создания анкет.
        request = self.factory.post('/api/partners_create_anketa/',
                                    json.dumps({}),
                                    content_type='application/json')
        force_authenticate(request,
                           user=self.credit_user,
                           token=self.credit_user_token)
        view = PartnerView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 403)

    def create_users_and_groups(self):
        """
            Создание групп и пользователей.
        :return:
        """
        # Создаем партнеров
        self.partner_auth = {"username": "partner_user",
                             "password": "Qwerty123"}
        User.objects.create_user(**self.partner_auth)
        self.partner_user = User.objects.get(
            username=self.partner_auth['username']
        )
        Partner(username=self.partner_user,
                name=self.partner_auth['username']).save()

        self.partner_auth2 = {"username": "partner_user2",
                              "password": "Qwerty123"}
        User.objects.create_user(**self.partner_auth2)
        self.partner_user2 = User.objects.get(
            username=self.partner_auth2['username']
        )
        Partner(
            username=self.partner_user2,
            name=self.partner_auth2['username']
        ).save()

        # Создаем кредитные организации.
        self.credit_auth = {
            "username": "credit_user",
            "password": "Qwerty123"
        }
        User.objects.create_user(**self.credit_auth)
        self.credit_user = User.objects.get(
            username=self.credit_auth['username']
        )
        CreditOrg(
            username=self.credit_user,
            name=self.credit_auth['username']
        ).save()

        self.credit_auth2 = {
            "username": "credit_user2",
            "password": "Qwerty123"
        }
        User.objects.create_user(**self.credit_auth2)
        self.credit_user2 = User.objects.get(
            username=self.credit_auth2['username']
        )
        CreditOrg(
            username=self.credit_user2,
            name=self.credit_auth2['username']
        ).save()

        # Добавляем партнеров в группу партнеров.
        partner_group, created = Group.objects.get_or_create(
            name='partner_group'
        )
        self.assertTrue(created)
        partner_group.user_set.add(self.partner_user)
        partner_group.user_set.add(self.partner_user2)

        # Добавляем кредитные организации в группу кредитных организаций.
        credit_group, created = Group.objects.get_or_create(
            name='credit_group'
        )
        self.assertTrue(created)
        credit_group.user_set.add(self.credit_user)
        credit_group.user_set.add(self.credit_user2)


class TestPartnersZayavkaAPI(TestCase):
    """
        Тестирование создания предложения и заявки партнером.
    """

    def setUp(self):
        """
            Создание фикстур
        :return:
        """
        TestPartnersZayavkaAPI.factory = APIRequestFactory()
        self.create_users_and_groups()
        self.get_token()
        self.partner_api_create_ankets()

    def test_partners_create_zayavka(self):
        """
            Тестирование создания заявки и предложения.
            Тестирование отправки заявки в кредитную организацию
            на рассмотрение заявки.
        :return:
        """
        _zayavka_send = {
                "type_of": "P",
                "start_rotate": "2018-03-23 20:20:20",
                "end_rotate": "2018-03-24 20:20:20",
                "min_scoring": "1.0",
                "max_scoring": "5.0",
                "credit_org": self.credit_auth2['username'],
                "passport_num": "kj234ahs23484y32894"
            }

        request = self.factory.post('/api/partners_create_zayavka/'
                                    '', json.dumps(_zayavka_send),
                                    content_type='application/json')
        force_authenticate(request,
                           user=self.partner_user2,
                           token=self.partner_user_token2
                           )
        view = PartnerCreateZayavka.as_view()
        response = view(request)
        _partner_answer = json.loads(response.content)
        # Убеждаемся что заявка и предложение созданы.
        self.assertEqual(response.status_code, 201)
        self.assertEqual(_partner_answer['status'], 'created')
        creditorg = CreditOrg.objects.get(name=self.credit_auth2['username'])
        self.assertEqual(
            len(Predlogenie.objects.filter(credit_org=creditorg)),
            1
        )
        client_anketa = ClientAnketa.objects.get(
            passport_num=_zayavka_send['passport_num']
        )
        zayavka = ZayavkiCreditOrg.objects.filter(
            client_anketa=client_anketa
        )
        self.assertEqual(len(zayavka), 1)
        ###############################################
        #       Отправляем заявку на рассмотрение
        #  в кредитную организацию
        ###############################################
        _zayavka_send = {"id": zayavka[0].id}
        request = self.factory.post(
            '/api/partners_send_zayavka/',
            json.dumps(_zayavka_send),
            content_type='application/json'
        )
        force_authenticate(
            request,
            user=self.partner_user2,
            token=self.partner_user_token2
        )
        view = PartnerSendZayavka.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        _zayvka_status = json.loads(response.content)
        self.assertEqual(_zayvka_status['status'],
                         'Zayavka sended')

    def create_users_and_groups(self):
        """
            Создание групп и пользователей.
        :return:
        """
        # Создаем партнеров
        self.partner_auth = {
            "username": "partner_user",
            "password": "Qwerty123"
        }
        User.objects.create_user(**self.partner_auth)
        self.partner_user = User.objects.get(
            username=self.partner_auth['username']
        )
        Partner(
            username=self.partner_user,
            name=self.partner_auth['username']
        ).save()

        self.partner_auth2 = {
            "username": "partner_user2",
            "password": "Qwerty123"
        }
        User.objects.create_user(**self.partner_auth2)
        self.partner_user2 = User.objects.get(
            username=self.partner_auth2['username']
        )
        Partner(
            username=self.partner_user2,
            name=self.partner_auth2['username']
        ).save()

        # Создаем кредитные организации.
        self.credit_auth = {"username": "credit_user", "password": "Qwerty123"}
        User.objects.create_user(**self.credit_auth)
        self.credit_user = User.objects.get(
            username=self.credit_auth['username']
        )
        CreditOrg(
            username=self.credit_user,
            name=self.credit_auth['username']
        ).save()

        self.credit_auth2 = {
            "username": "credit_user2",
            "password": "Qwerty123"
        }
        User.objects.create_user(**self.credit_auth2)
        self.credit_user2 = User.objects.get(
            username=self.credit_auth2['username']
        )
        CreditOrg(
            username=self.credit_user2,
            name=self.credit_auth2['username']
        ).save()

        # Добавляем партнеров в группу партнеров.
        partner_group, created = Group.objects.get_or_create(
            name='partner_group'
        )
        self.assertTrue(created)
        partner_group.user_set.add(self.partner_user)
        partner_group.user_set.add(self.partner_user2)

        # Добавляем кредитные организации в группу кредитных организаций.
        credit_group, created = Group.objects.get_or_create(
            name='credit_group'
        )
        self.assertTrue(created)
        credit_group.user_set.add(self.credit_user)
        credit_group.user_set.add(self.credit_user2)

    def get_token(self):
        """
            Тестирование функционала выдачи токенов для пользователей.
        :return:
        """

        # Проверка получения для первого партнера
        request = self.factory.post(
            '/api-token-auth/',
            json.dumps(self.partner_auth),
            content_type='application/json'
        )
        view = Obtain_auth_token.as_view()
        force_authenticate(request, user=self.partner_user)
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.partner_user_token = json.loads(response.content)['token']
        self.assertGreater(len(self.partner_user_token), 1)

        # Проверка получения токена для второго партнера
        request = self.factory.post(
            '/api-token-auth/',
            json.dumps(self.partner_auth2),
            content_type='application/json'
        )
        view = Obtain_auth_token.as_view()
        force_authenticate(request, user=self.partner_user2)
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.partner_user_token2 = json.loads(response.content)['token']
        self.assertGreater(len(self.partner_user_token2), 1)

        # Проверка получения токена для кредитной организации 1
        request = self.factory.post(
            '/api-token-auth/',
            json.dumps(self.credit_auth),
            content_type='application/json'
        )
        view = Obtain_auth_token.as_view()
        force_authenticate(request, user=self.credit_user)
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.credit_user_token = json.loads(response.content)['token']
        self.assertGreater(len(self.credit_user_token), 1)

        # Проверка получения токена для кредитной организации 2
        request = self.factory.post(
            '/api-token-auth/',
            json.dumps(self.credit_auth2),
            content_type='application/json'
        )
        view = Obtain_auth_token.as_view()
        force_authenticate(request, user=self.credit_user2)
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.credit_user_token2 = json.loads(response.content)['token']
        self.assertGreater(len(self.credit_user_token2), 1)

    def partner_api_create_ankets(self):
        """
            Тестирование API для партнеров.
            1. Создание анкет.
            2. Просмотр анкет с фильтрами.
            3. Тестирование того, что пользователи
            не входящие в группу партнеров
                не могут получить доступ к API предназначенного для партнеров.
        :return:
        """
        _anketa1 = {
            "name": "Сидор",
            "surname": "Петрович",
            "lastname": "Иванов",
            "birthday": "2018-03-21",
            "telephone": "111111111111",
            "passport_num": "kjahsd2384y32894",
            "score_bal": 34.0
        }
        request = self.factory.post(
            '/api/partners_create_anketa/',
            json.dumps(_anketa1),
            content_type='application/json'
        )
        force_authenticate(
            request,
            user=self.partner_user,
            token=self.partner_user_token
        )
        view = PartnerCreateAnketa.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 201)
        status = json.loads(response.content)['status']
        self.assertEqual(status, 'created')

        _anketa2 = {
            "name": "Иван",
            "surname": "Иванович",
            "lastname": "Иванов",
            "birthday": "2018-04-21",
            "telephone": "222222222222",
            "passport_num": "kjahsd23834534",
            "score_bal": 3.0
        }
        request = self.factory.post(
            '/api/partners_create_anketa/',
            json.dumps(_anketa2),
            content_type='application/json'
        )
        force_authenticate(
            request,
            user=self.partner_user,
            token=self.partner_user_token
        )
        view = PartnerCreateAnketa.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 201)
        status = json.loads(response.content)['status']
        self.assertEqual(status, 'created')

        # Проверяем что созданы две анкеты для этого партнера.
        _partner = Partner.objects.get(username=self.partner_user)
        ankets = ClientAnketa.objects.filter(partner=_partner)
        self.assertEqual(len(ankets), 2)
        self.assertEqual(ankets[0].name, 'Сидор')
        self.assertEqual(ankets[0].partner.name, self.partner_auth['username'])
        self.assertEqual(ankets[1].name, 'Иван')
        self.assertEqual(ankets[1].partner.name, self.partner_auth['username'])
        ############################################################
        # Создаем анкеты для второго партнера.
        ############################################################
        _anketa1 = {
            "name": "Николай",
            "surname": "Петрович",
            "lastname": "Петров",
            "birthday": "2018-03-21",
            "telephone": "111111111111",
            "passport_num": "kj234ahs23484y32894",
            "score_bal": 5.0
        }
        request = self.factory.post(
            '/api/partners_create_anketa/',
            json.dumps(_anketa1),
            content_type='application/json'
        )
        force_authenticate(
            request,
            user=self.partner_user2,
            token=self.partner_user_token2
        )
        view = PartnerCreateAnketa.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 201)
        status = json.loads(response.content)['status']
        self.assertEqual(status, 'created')
        _anketa2 = {
            "name": "Вася",
            "surname": "Иванович",
            "lastname": "Иванов",
            "birthday": "2018-04-21",
            "telephone": "222222222222",
            "passport_num": "kjahsd2383333",
            "score_bal": 3.0
        }
        request = self.factory.post(
            '/api/partners_create_anketa/',
            json.dumps(_anketa2),
            content_type='application/json'
        )
        force_authenticate(
            request,
            user=self.partner_user2,
            token=self.partner_user_token2
        )
        view = PartnerCreateAnketa.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 201)
        status = json.loads(response.content)['status']
        self.assertEqual(status, 'created')

        # Проверяем что созданы две анкеты для этого партнера.
        _partner = Partner.objects.get(username=self.partner_user2)
        ankets = ClientAnketa.objects.filter(partner=_partner)
        self.assertEqual(len(ankets), 2)
        self.assertEqual(ankets[0].name, 'Николай')
        self.assertEqual(
            ankets[0].partner.name,
            self.partner_auth2['username']
        )
        self.assertEqual(ankets[1].name, 'Вася')
        self.assertEqual(
            ankets[1].partner.name,
            self.partner_auth2['username']
        )

        # Проверка API партнеров для просмотра анкет клиентов пользователей,
        # с фильтрами.
        request = self.factory.post(
            '/api/partners_view/',
            json.dumps({}),
            content_type='application/json'
        )
        force_authenticate(
            request,
            user=self.partner_user,
            token=self.partner_user_token
        )
        view = PartnerView.as_view()
        response = view(request)
        _partner_answer = json.loads(response.content)
        # Убеждаемся в том что партнер видит только свои анкеты.
        self.assertEqual(len(_partner_answer), 2)
        self.assertEqual(_partner_answer[0]['fields']['name'], 'Сидор')
        self.assertEqual(_partner_answer[1]['fields']['name'], 'Иван')

        # Проверяем что фильтры для партнера 1, отрабатывают корректно
        request = self.factory.post(
            '/api/partners_view/',
            json.dumps({"name": "Сидор"}),
            content_type='application/json'
        )
        force_authenticate(
            request,
            user=self.partner_user,
            token=self.partner_user_token
        )
        view = PartnerView.as_view()
        response = view(request)
        _partner_answer = json.loads(response.content)
        # Убеждаемся в том что партнер видит только
        #  одну анкету которую он выбрал при помощи фильтра.
        self.assertEqual(len(_partner_answer), 1)
        self.assertEqual(_partner_answer[0]['fields']['name'], 'Сидор')

        # Проверка API партнеров для просмотра анкет клиентов пользователей,
        # с фильтрами.
        request = self.factory.post(
            '/api/partners_view/',
            json.dumps({}),
            content_type='application/json'
        )
        force_authenticate(
            request,
            user=self.partner_user2,
            token=self.partner_user_token2
        )
        view = PartnerView.as_view()
        response = view(request)
        _partner_answer = json.loads(response.content)
        # Убеждаемся в том что партнер видит только свои анкеты.
        self.assertEqual(len(_partner_answer), 2)
        self.assertEqual(_partner_answer[0]['fields']['name'], 'Николай')
        self.assertEqual(_partner_answer[1]['fields']['name'], 'Вася')

        # Проверяем что фильтры для партнера 2, отрабатывают корректно
        request = self.factory.post(
            '/api/partners_view/',
            json.dumps({"name": "Николай"}),
            content_type='application/json'
        )
        force_authenticate(
            request,
            user=self.partner_user2,
            token=self.partner_user_token2
        )
        view = PartnerView.as_view()
        response = view(request)
        _partner_answer = json.loads(response.content)
        # Убеждаемся в том что партнер видит только одну
        #  анкету которую он выбрал при помощи фильтра.
        self.assertEqual(len(_partner_answer), 1)
        self.assertEqual(_partner_answer[0]['fields']['name'], 'Николай')

        # Проверяем что пользователи не входящие в группу
        #  партнеров не могут получить Доступ к API
        # предназначенной для партнеров.
        # Проверка API для просмотра анкет.
        request = self.factory.post(
            '/api/partners_view/',
            json.dumps({}),
            content_type='application/json'
        )
        force_authenticate(
            request,
            user=self.credit_user,
            token=self.credit_user_token
        )
        view = PartnerView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 403)
        # Проверка API для создания анкет.
        request = self.factory.post(
            '/api/partners_create_anketa/',
            json.dumps({}),
            content_type='application/json'
        )
        force_authenticate(
            request,
            user=self.credit_user,
            token=self.credit_user_token
        )
        view = PartnerView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 403)


class TestCreditOrgAPI(TestCase):
    """
        Тестирование API для кредитных организаций.
    """
    def setUp(self):
        """
            Наполняем фикстурами базу данных.
        :return:
        """
        self.factory = APIRequestFactory()
        self.create_users_and_groups()
        self.get_token()
        self.partner_api_create_ankets()
        self.partners_create_zayavka()

    def create_users_and_groups(self):
        """
            Создание групп и пользователей.
        :return:
        """
        # Создаем партнеров
        self.partner_auth = {
            "username": "partner_user",
            "password": "Qwerty123"
        }
        User.objects.create_user(**self.partner_auth)
        self.partner_user = User.objects.get(
            username=self.partner_auth['username']
        )
        Partner(
            username=self.partner_user,
            name=self.partner_auth['username']
        ).save()

        self.partner_auth2 = {
            "username": "partner_user2",
            "password": "Qwerty123"
        }
        User.objects.create_user(**self.partner_auth2)
        self.partner_user2 = User.objects.get(
            username=self.partner_auth2['username']
        )
        Partner(
            username=self.partner_user2,
            name=self.partner_auth2['username']
        ).save()

        # Создаем кредитные организации.
        self.credit_auth = {
            "username": "credit_user",
            "password": "Qwerty123"
        }
        User.objects.create_user(**self.credit_auth)
        self.credit_user = User.objects.get(
            username=self.credit_auth['username']
        )
        CreditOrg(
            username=self.credit_user,
            name=self.credit_auth['username']
        ).save()

        self.credit_auth2 = {
            "username": "credit_user2",
            "password": "Qwerty123"
        }
        User.objects.create_user(**self.credit_auth2)
        self.credit_user2 = User.objects.get(
            username=self.credit_auth2['username']
        )
        CreditOrg(
            username=self.credit_user2,
            name=self.credit_auth2['username']
        ).save()

        # Добавляем партнеров в группу партнеров.
        partner_group, created = Group.objects.get_or_create(
            name='partner_group'
        )
        self.assertTrue(created)
        partner_group.user_set.add(self.partner_user)
        partner_group.user_set.add(self.partner_user2)

        # Добавляем кредитные организации в группу кредитных организаций.
        credit_group, created = Group.objects.get_or_create(
            name='credit_group'
        )
        self.assertTrue(created)
        credit_group.user_set.add(self.credit_user)
        credit_group.user_set.add(self.credit_user2)

    def get_token(self):
        """
            Тестирование функционала выдачи токенов для пользователей.
        :return:
        """

        # Проверка получения для первого партнера
        request = self.factory.post(
            '/api-token-auth/',
            json.dumps(self.partner_auth),
            content_type='application/json'
        )
        view = Obtain_auth_token.as_view()
        force_authenticate(request, user=self.partner_user)
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.partner_user_token = json.loads(response.content)['token']
        self.assertGreater(len(self.partner_user_token), 1)

        # Проверка получения токена для второго партнера
        request = self.factory.post(
            '/api-token-auth/',
            json.dumps(self.partner_auth2),
            content_type='application/json'
        )
        view = Obtain_auth_token.as_view()
        force_authenticate(request, user=self.partner_user2)
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.partner_user_token2 = json.loads(response.content)['token']
        self.assertGreater(len(self.partner_user_token2), 1)

        # Проверка получения токена для кредитной организации 1
        request = self.factory.post(
            '/api-token-auth/',
            json.dumps(self.credit_auth),
            content_type='application/json'
        )
        view = Obtain_auth_token.as_view()
        force_authenticate(request, user=self.credit_user)
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.credit_user_token = json.loads(response.content)['token']
        self.assertGreater(len(self.credit_user_token), 1)

        # Проверка получения токена для кредитной организации 2
        request = self.factory.post(
            '/api-token-auth/',
            json.dumps(self.credit_auth2),
            content_type='application/json'
        )
        view = Obtain_auth_token.as_view()
        force_authenticate(request, user=self.credit_user2)
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.credit_user_token2 = json.loads(response.content)['token']
        self.assertGreater(len(self.credit_user_token2), 1)

    def partner_api_create_ankets(self):
        """
            Тестирование API для партнеров.
            1. Создание анкет.
            2. Просмотр анкет с фильтрами.
            3. Тестирование того, что пользователи
             не входящие в группу партнеров
            не могут получить доступ к API предназначенного для партнеров.
        :return:
        """
        _anketa1 = {
            "name": "Сидор",
            "surname": "Петрович",
            "lastname": "Иванов",
            "birthday": "2018-03-21",
            "telephone": "111111111111",
            "passport_num": "kjahsd2384y32894",
            "score_bal": 34.0
        }
        request = self.factory.post(
            '/api/partners_create_anketa/',
            json.dumps(_anketa1),
            content_type='application/json'
        )
        force_authenticate(
            request,
            user=self.partner_user,
            token=self.partner_user_token
        )
        view = PartnerCreateAnketa.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 201)
        status = json.loads(response.content)['status']
        self.assertEqual(status, 'created')

        _anketa2 = {
            "name": "Иван",
            "surname": "Иванович",
            "lastname": "Иванов",
            "birthday": "2018-04-21",
            "telephone": "222222222222",
            "passport_num": "kjahsd23834534",
            "score_bal": 3.0
        }
        request = self.factory.post(
            '/api/partners_create_anketa/',
            json.dumps(_anketa2),
            content_type='application/json'
        )
        force_authenticate(
            request,
            user=self.partner_user,
            token=self.partner_user_token
        )
        view = PartnerCreateAnketa.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 201)
        status = json.loads(response.content)['status']
        self.assertEqual(status, 'created')

        # Проверяем что созданы две анкеты для этого партнера.
        _partner = Partner.objects.get(username=self.partner_user)
        ankets = ClientAnketa.objects.filter(partner=_partner)
        self.assertEqual(len(ankets), 2)
        self.assertEqual(ankets[0].name, 'Сидор')
        self.assertEqual(ankets[0].partner.name, self.partner_auth['username'])
        self.assertEqual(ankets[1].name, 'Иван')
        self.assertEqual(ankets[1].partner.name, self.partner_auth['username'])
        ############################################################
        # Создаем анкеты для второго партнера.
        ############################################################
        _anketa1 = {
            "name": "Николай",
            "surname": "Петрович",
            "lastname": "Петров",
            "birthday": "2018-03-21",
            "telephone": "111111111111",
            "passport_num": "kj234ahs23484y32894",
            "score_bal": 5.0
        }
        request = self.factory.post(
            '/api/partners_create_anketa/',
            json.dumps(_anketa1),
            content_type='application/json'
        )
        force_authenticate(
            request,
            user=self.partner_user2,
            token=self.partner_user_token2
        )
        view = PartnerCreateAnketa.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 201)
        status = json.loads(response.content)['status']
        self.assertEqual(status, 'created')

        _anketa2 = {
            "name": "Вася",
            "surname": "Иванович",
            "lastname": "Иванов",
            "birthday": "2018-04-21",
            "telephone": "222222222222",
            "passport_num": "kjahsd2383333",
            "score_bal": 3.0
        }
        request = self.factory.post(
            '/api/partners_create_anketa/',
            json.dumps(_anketa2),
            content_type='application/json'
        )
        force_authenticate(
            request,
            user=self.partner_user2,
            token=self.partner_user_token2
        )
        view = PartnerCreateAnketa.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 201)
        status = json.loads(response.content)['status']
        self.assertEqual(status, 'created')

        # Проверяем что созданы две анкеты для этого партнера.
        _partner = Partner.objects.get(username=self.partner_user2)
        ankets = ClientAnketa.objects.filter(partner=_partner)
        self.assertEqual(len(ankets), 2)
        self.assertEqual(ankets[0].name, 'Николай')
        self.assertEqual(
            ankets[0].partner.name,
            self.partner_auth2['username']
        )
        self.assertEqual(ankets[1].name, 'Вася')
        self.assertEqual(
            ankets[1].partner.name,
            self.partner_auth2['username']
        )

        # Проверка API партнеров для просмотра анкет клиентов пользователей,
        # с фильтрами.
        request = self.factory.post(
            '/api/partners_view/',
            json.dumps({}),
            content_type='application/json'
        )
        force_authenticate(
            request,
            user=self.partner_user,
            token=self.partner_user_token
        )
        view = PartnerView.as_view()
        response = view(request)
        _partner_answer = json.loads(response.content)
        # Убеждаемся в том что партнер видит только свои анкеты.
        self.assertEqual(len(_partner_answer), 2)
        self.assertEqual(_partner_answer[0]['fields']['name'], 'Сидор')
        self.assertEqual(_partner_answer[1]['fields']['name'], 'Иван')

        # Проверяем что фильтры для партнера 1, отрабатывают корректно
        request = self.factory.post(
            '/api/partners_view/',
            json.dumps({"name": "Сидор"}),
            content_type='application/json'
        )
        force_authenticate(
            request,
            user=self.partner_user,
            token=self.partner_user_token
        )
        view = PartnerView.as_view()
        response = view(request)
        _partner_answer = json.loads(response.content)
        # Убеждаемся в том что партнер видит только одну
        #  анкету которую он выбрал при помощи фильтра.
        self.assertEqual(len(_partner_answer), 1)
        self.assertEqual(_partner_answer[0]['fields']['name'], 'Сидор')

        # Проверка API партнеров для просмотра анкет клиентов пользователей,
        # с фильтрами.
        request = self.factory.post(
            '/api/partners_view/',
            json.dumps({}),
            content_type='application/json'
        )
        force_authenticate(
            request,
            user=self.partner_user2,
            token=self.partner_user_token2
        )
        view = PartnerView.as_view()
        response = view(request)
        _partner_answer = json.loads(response.content)
        # Убеждаемся в том что партнер видит только свои анкеты.
        self.assertEqual(len(_partner_answer), 2)
        self.assertEqual(_partner_answer[0]['fields']['name'], 'Николай')
        self.assertEqual(_partner_answer[1]['fields']['name'], 'Вася')

        # Проверяем что фильтры для партнера 2, отрабатывают корректно
        request = self.factory.post(
            '/api/partners_view/',
            json.dumps({"name": "Николай"}),
            content_type='application/json'
        )
        force_authenticate(
            request,
            user=self.partner_user2,
            token=self.partner_user_token2
        )
        view = PartnerView.as_view()
        response = view(request)
        _partner_answer = json.loads(response.content)
        # Убеждаемся в том что партнер видит только одну
        # анкету которую он выбрал при помощи фильтра.
        self.assertEqual(len(_partner_answer), 1)
        self.assertEqual(_partner_answer[0]['fields']['name'], 'Николай')

        # Проверяем что пользователи не входящие в группу
        #  партнеров не могут получить Доступ к API предназначенной
        #  для партнеров. Проверка API для просмотра анкет.
        request = self.factory.post(
            '/api/partners_view/',
            json.dumps({}),
            content_type='application/json'
        )
        force_authenticate(
            request,
            user=self.credit_user,
            token=self.credit_user_token
        )
        view = PartnerView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 403)
        # Проверка API для создания анкет.
        request = self.factory.post(
            '/api/partners_create_anketa/',
            json.dumps({}),
            content_type='application/json'
        )
        force_authenticate(
            request,
            user=self.credit_user,
            token=self.credit_user_token
        )
        view = PartnerView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 403)

    def partners_create_zayavka(self):
        """
            Тестирование создания заявки и предложения.
            Тестирование интефейса отправки заявки.
            Тестирование интерфейса просмотра заявок для кредитной оргаизации.
            Тестирование интейфейса обновления статусов
             для кредитных организаций по заявкам.
        :return:
        """
        _zayavka_send = {
                "type_of": "P",
                "start_rotate": "2018-03-23 20:20:20",
                "end_rotate": "2018-03-24 20:20:20",
                "min_scoring": "1.0",
                "max_scoring": "5.0",
                "credit_org": self.credit_auth2['username'],
                "passport_num": "kj234ahs23484y32894"
            }
        request = self.factory.post(
            '/api/partners_create_zayavka/',
            json.dumps(_zayavka_send),
            content_type='application/json'
        )
        force_authenticate(
            request,
            user=self.partner_user2,
            token=self.partner_user_token2
        )
        view = PartnerCreateZayavka.as_view()
        response = view(request)
        _partner_answer = json.loads(response.content)
        # Убеждаемся что заявка и предложение созданы.
        self.assertEqual(response.status_code, 201)
        self.assertEqual(_partner_answer['status'], 'created')
        creditorg = CreditOrg.objects.get(
            name=self.credit_auth2['username']
        )
        self.assertEqual(
            len(Predlogenie.objects.filter(
                credit_org=creditorg)), 1
        )
        client_anketa = ClientAnketa.objects.get(
            passport_num=_zayavka_send['passport_num']
        )
        zayavka = ZayavkiCreditOrg.objects.filter(
            client_anketa=client_anketa
        )
        self.assertEqual(len(zayavka), 1)
        self.assertEqual(zayavka[0].status, 'NEW')
        # Изменяем статус заявки на отправлено.
        z = ZayavkiCreditOrg.objects.get(**{"id": zayavka[0].id})
        z.status = 'SENDED'
        z.save()

        # Тестирование работы интерфейса для кредитных организаций.
        request = self.factory.post('/api/credit_org/',
                                    json.dumps(_zayavka_send),
                                    content_type='application/json'
                                    )
        force_authenticate(
            request,
            user=self.credit_user2,
            token=self.credit_user_token2
        )
        view = CreditOrgView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        _creditorg_view = json.loads(response.content)
        self.assertEqual(len(_creditorg_view), 1)
        self.assertEqual(_creditorg_view[0]['fields']['status'], 'SENDED')
        # Проверяем что каждая кредитная организация видит только свои заявки.
        request = self.factory.post(
            '/api/credit_org/',
            json.dumps(_zayavka_send),
            content_type='application/json'
        )
        force_authenticate(
            request,
            user=self.credit_user,
            token=self.credit_user_token
        )
        view = CreditOrgView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        _creditorg_view = json.loads(response.content)
        self.assertEqual(len(_creditorg_view), 0)
        ###############################################
        # Тестирование интерфейса обновления статуса для заявки
        # в кредитную организацию.
        ###############################################
        _update_status = {
            "id": "1",
            "status": "ACCEPT"
        }
        request = self.factory.post(
            '/api/creditorg_update_status/',
            json.dumps(_update_status),
            content_type='application/json'
        )
        force_authenticate(
            request,
            user=self.credit_user2,
            token=self.credit_user_token2
        )
        view = CreditOrgUpdateStatus.as_view()
        response = view(request)
        _credit_answer = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            _credit_answer['status'],
            'status updated'
        )
        # Проверяем что кредитная организация может обвнолять статусы
        #  только у заявок которые направлены именно ей.
        _update_status = {
            "id": "1",
            "status": "ACCEPT"
        }
        request = self.factory.post(
            '/api/creditorg_update_status/',
            json.dumps(_update_status),
            content_type='application/json'
        )
        force_authenticate(
            request,
            user=self.credit_user,
            token=self.credit_user_token
        )
        view = CreditOrgUpdateStatus.as_view()
        response = view(request)
        _credit_answer = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            _credit_answer['status'],
            "ZayavkiCreditOrg matching query does not exist."
        )
