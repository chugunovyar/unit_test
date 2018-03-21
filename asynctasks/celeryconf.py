import os
from kombu import Queue
from celery import Celery
from django.conf import settings

user = os.environ.get('RABBIT_USER', 'rabbitmq')
password = os.environ.get('RABBIT_PASSWORD', 'rabbitmq')
host = os.environ.get('RABBIT_HOST', 'rabbit')
port = os.environ.get('RABBIT_PORT','5672')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "unit_test.settings")

app = Celery('datanrm', backend='amqp', \
             broker='amqp://' + user + ':' + password + '@'+ host +':'+ port +'//')

app.conf.task_default_queues = 'default'

app.conf.task_queues = (
    Queue('default', routing_key='asynctasks.#'),
)

app.conf.task_routes = {
    'asynctasks.tasks.*':{'queue':'default'},
}

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)