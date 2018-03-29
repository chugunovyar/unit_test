# -- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class CreditOrg(models.Model):
    """
        Кредитные организации.
    """
    name = models.CharField(max_length=254)
    username = models.ForeignKey(User)
    
    class Meta:
        verbose_name='Кредитные организации'

    def __str__(self):
        return '%s' % (self.name)

    def __unicode__(self):
        return  '%s' % (self.name)
    
    
class Partner(models.Model):
    """
        Партнеры
    """
    name = models.CharField(max_length=254)
    username = models.ForeignKey(User)

    class Meta:
        verbose_name='Партнеры'

    def __str__(self):
        return '%s' % (self.name)

    def __unicode__(self):
        return  '%s' % (self.name)


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
    # предпологаю что номер паспорта уникален в стране :)
    passport_num = models.CharField(max_length=20, unique=True)
    score_bal = models.FloatField()
    partner = models.ForeignKey(Partner)

    class Meta:
        verbose_name='Анкета клиента'

    def __str__(self):
        return '%s' % (self.passport_num)

    def __unicode__(self):
        return  '%s' % (self.passport_num)


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

    def __str__(self):
        return '%s' % (self.name)

    def __unicode__(self):
        return  '%s' % (self.name)
    

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
    predlogenie = models.ForeignKey(Predlogenie)
    status = models.CharField(choices=STATUSES, max_length=10, default='NEW')

    class Meta:
        verbose_name='Заявки в кредитную организацию'

