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
 ```