# Описание использования проекта.

	Тестовое задание для организации.

## Инсталяция и запуск
```text
	Необходимо сбилдить композ-файл и запустить проект, для этого необходимо 
	выполнить следующие комманды:
```
	
```bash
	docker-compose build
	docker-compose up
```
	Дождаться запуска проекта и перейти на страницу http://localhost:8000

## Описание функционала.

### Партнеры.
```text
	Партнеры имеют доступ к API партнеров.
	Могут создавать анкеты (http://localhost:8000/api/partners_create_anketa/),
	а также просматривать существующие анкеты (http://localhost:8000/api/partners_view/)
	для партнера который делает запрос.
	Создавать заявки на основании анкет (http://localhost:8000/api/partners_create_zayavka/).
		Тип кредита может быть нескольких типов:
            'P' = 'Потребительский'
            'I' = 'Ипотека'
            'A' = 'Автокредит'
        
        Пример запроса по созданию заявки:
            {
                "type_of":"P",
                "start_rotate":"2018-03-23 20:20:20",
                "end_rotate":"2018-03-24 20:20:20",
                "min_scoring":"1.0",
                "max_scoring":"5.0",
                "credit_org":"Кредитная организация2",
                "passport_num":"234sd345435sdfdsf24"
            }
    	Для формирования(создания) заявки необходимо указать тип кредита (type_of),
	начало и конец ротации заявки(дату в формате как указано в примере.), минимальный,
	максимальный скорринговый бал(min_scoring, max_scoring),наименование кредитной 
	организации (credit_org), номер и серию паспорта лица подающего заявку (credit_org) 
	
	Отправка заявки в кредитную организацию происходит происходит через 
	(http://localhost:8000/api/partners_send_anketa/):
	 	
```

## Запуск тестирования проекта.
Перейти внутрь контейнера app коммандой:
```bash
   docker exec -ti unittest_app_1 bash
```
запустить внутри контейнера консольную команду для запуска тестов.
```bash
    python manage.py test
```

## Роли 

```text

	суперпользователь:
 	login: root
 	password: Qwerty123

 	Пользователь для Flower:
 	login: FLOWER_LOGIN
 	password: FLOWER_PASS

 	Пользователь для RabbitMQ:
 	login: rabbitmq
 	password: rabbitmq

 	Учетная запись для партнера:
 	login: partner_user
 	password: Qwerty123

 	Учетная запись для партнера:
 	login: partner_user2
 	password: Qwerty123


 	Учетная запись для кредитной организации:
 	login: credit_user
 	password: Qwerty123

 	Учетная запись для кредитной организации:
 	login: credit_user2
 	password: Qwerty123

``` 

## Ссылки необходимые для работы алгоритма:

```text
	http://localhost:8000/api-token-auth/ - Выдача токена на основании
	логина и пароля (POST - запрос), пример:
	
		{"username":"root", "password": "Qwerty123"}

    http://localhost:8000/api/partners_view/ - просмотр существуюших
    анкет с сортировкой и фильтрами (POST запрос). Пример:

        {
            "name": "Владимир",
            "surname": "Владимирович",
            "lastname": "Путин",
            "birthday": "2018-03-21",
            "telephone": "89201271212",
            "passport_num": "passport_num",
            "score_bal": 34.0
        }

    Просмотр анкет по id. Пример:

    { "id": 1 }


    http://localhost:8000/api/partners_create_anketa/ - создание анкет
    (POST запрос). Пример:

        {
            "name": "Владимир",
            "surname": "Владимирович",
            "lastname": "Путин",
            "birthday": "2018-03-21",
            "telephone": "89201271212",
            "passport_num": "passport_num",
            "score_bal": 34.0
        }
    
    http://localhost:8000/api/partners_view_creditorgs/ - возможность для
    партнеров просмотреть список кредитных организаций. С фильтрами и сортировкой. 
    (POST запрос). Пример:
    {"name":"Кредитная организация1"} или напрмиер:
    {"id":"1"}
    
    
    http://localhost:8000/api/partners_send_anketa/ - Отправка партнером
    анкеты в кредитную организацию (POST - запрос). Пример:

    { "id": 1 }

	Вспомогательная консольная комманда позовляющая проверить работу механизма
	по отправки заявки в кредитную организацию.
	
	python manage.py send_zayavka -id <id заявки>

```

## Основные компоненты используемые в проекте.
```text

	Django - http://localhost:8000
	Django admin panel - http://localhost:8000/admin/
	Flower - панель мониторинга выполнения асинхронных задач http://localhost:5555
	RabbitMQ - брокер очередей, http://localhost:15672

```

#### Примечания.
```text

     Файл .env через который прокидываем в проект основные переменные не
     закинул в gitignore специально, так вам не придется писать свой.

     Формат обмена информацией во всех запросах json.
     Заголовки для всех запросов:
     Content-type: application/json

     Выгрузка фикстур:
     python manage.py dumpdata --settings=unit_test.settings > fixtures/fixtures.json

     Загрузка фикстур (Просходит в автоматическом режиме):
     python manage.py loaddata fixtures/fixtures.json

 ```