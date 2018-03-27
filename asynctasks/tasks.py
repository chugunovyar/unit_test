# -- coding: utf-8 -*-
from celery.result import AsyncResult
from asynctasks.celeryconf import app
from api.send_zayavka import SendZayavkaToCreditOrg

@app.task
def test(n):
    return n ** 2

@app.task
def send_request_credit_org(zayavka_id=None):
    """
        Отправка запроса в кредитную организацию.
    :param anketa:
    :return:
    """
    if zayavka_id != None:
        try:
            SendZayavkaToCreditOrg(zayavka_id=zayavka_id)
        except Exception as err:
            return err
    else:
        return 'There is no id presented'
    return 'Ok'
