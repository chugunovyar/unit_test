from django.core.management.base import BaseCommand, CommandError
from api.send_zayavka import SendZayavkaToCreditOrg
import json

class Command(BaseCommand):
    help = 'Вспомогательная консольная команда которая позволяет проверить отправку заявки в кредитную организацию'

    def add_arguments(self, parser):
        parser.add_argument('-id', type=str)

    def handle(self, *args, **options):
        zayavka_id = json.dumps({"id":options['id']})
        SendZayavkaToCreditOrg(zayavka_id=zayavka_id)#.query()


