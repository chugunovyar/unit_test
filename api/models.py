# -- coding: utf-8 -*-
from django.db import models

class CreditOrg(models.Model):
    """
        Кредитные организации.
    """
    name = models.CharField(max_length=254)
    
    class Meta:
        verbose_name='Кредитные организации'

    def __unicode__(self):
        return self.name
    
    
class Partner(models.Model):
    """
        Партнеры
    """
    name = models.CharField(max_length=254)

    class Meta:
        verbose_name='Партнеры'
    

class Predlogenie(models.Model):
    """
        Предложение.
    """
    
    TYPE_OF = (
        ('P','Потребительский'),
        ('I','Ипотека'),
        ('A','Автокредит'),
    )
    
    create_dt = models.DateTimeField(auto_now_add=True)
    update_dt = models.DateTimeField(auto_now=True)
    start_rotate = models.DateTimeField()
    end_rotate = models.DateTimeField()
    name = models.CharField(max_length=254)
    type_of = models.CharField(max_length=1, choices=TYPE_OF)
    min_scoring = models.FloatField()
    max_scoring = models.FloatField()
    credit_org = models.ForeignKey(CreditOrg)

    class Meta:
        verbose_name='Предложения'

    def __unicode__(self):
        return self.name

class ClientAnketa(models.Model):
    """
        Модель Анкета клиента.
    """
    create_dt = models.DateTimeField(auto_now_add=True)
    update_dt = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    birthday = models.DateField(null=False, blank=False)
    telephone = models.CharField(max_length=14)
    passport_num = models.CharField(max_length=20)
    score_bal = models.FloatField()

    class Meta:
        verbose_name='Анкета клиента'

    def __unicode__(self):
        self.passport_num
    

class ZayavkiCreditOrg(models.Model):
    """
        Модель заявки в кредитную организацию.
    """
    
    STATUSES = (
        ('NEW', 'Новая'),
        ('SENDED', 'Отправлена'),
        ('ACCEPT','Получена'),
        ('AGREE', 'Одобрена'),
        ('CANCELED', 'Отказано'),
        ('ISSUED','Выдано'),    
    )
    
    create_dt = models.DateTimeField(auto_now_add=True)
    send_dt = models.DateTimeField(auto_now=True)
    client_anketa = models.ForeignKey(ClientAnketa)
    status = models.CharField(choices=STATUSES, max_length=10)

    class Meta:
        verbose_name='Заявки в кредитную организацию'

