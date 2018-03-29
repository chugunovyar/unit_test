# -- coding: utf-8 -*-
from celery.result import AsyncResult
from asynctasks.celeryconf import app
from api.send_zayavka import SendZayavkaToCreditOrg
from api.models import ZayavkiCreditOrg
import json

@app.task
def test(n):
    return n ** 2

@app.task
def send_request_credit_org(zayavka_id):
    """
        Отправка запроса в кредитную организацию.
    :param anketa:
    :return:
    """
    if zayavka_id != None:

        zayavka_id = json.loads(zayavka_id)
        try:
            zayavka = ZayavkiCreditOrg.objects.get(
                **zayavka_id
            )
            # Проставляем статус что заявка отправлена.
            zayavka.status = 'SENDED'
            zayavka.save()

            z = ZayavkiCreditOrg.objects.get(
                **zayavka_id
            )

            print (z.status)

        except ZayavkiCreditOrg.DoesNotExist as err:
                raise  err

        except Exception as err:
            raise err

    else:
        return 'There is no id presented'
    return 'Ok'
