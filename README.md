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

## Роли 

```text
	суперпользователь:
 	login: root
 	password: Qwerty123

``` 
 
## Основные компоненты используемые в проекте.
```text
	Django - http://localhost:8000
	Django admin panel - http://localhost:8000/admin/
	Flower - панель мониторинга выполнения асинхронных задач http://localhost:5555
	RabbitMQ - брокер очередей, http://localhost:15672
```