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
 	login: partner
 	password: Qwerty123

 	Учетная запись для кредитной организации:
 	login: credit_org
 	password: Qwerty123

``` 

## Ссылки необходимые для работы алгоритма:

```text

    http://localhost:8000/api/partners_view/ - просмотр существуюших
    анкет с сортировкой и фильтрами. Пример:

        {
            "name": "Владимир",
            "surname": "Владимирович",
            "lastname": "Путин",
            "birthday": "2018-03-21T13:35:54Z",
            "telephone": "89201271212",
            "passport_num": "passport_num",
            "score_bal": 34.0
        }

    Просмотр анкет по id. Пример:

    { "id": 1 }

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

 ```