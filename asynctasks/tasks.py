# -- coding: utf-8 -*-
from celery.result import AsyncResult
from asynctasks.celeryconf import app
import requests

@app.task
def test(n):
    return n ** 2

@app.task
def send_request_credit_org(anketa=None):
    """
        Отправка запроса в кредитную организацию.
    :param anketa:
    :return:
    """
    if anketa != None:
        pass
    else:
        pass
    return anketa
