# -- coding: utf-8 -*-
from django.contrib import admin
from api.models import ZayavkiCreditOrg, Partner, Predlogenie,\
    CreditOrg, ClientAnketa


class PartnerAdmin(admin.ModelAdmin):
    """

    """
    list_display = ('id', 'name', 'username')
    readonly_fields = ('id',)
    fields = ()
    raw_id_fields = ('username',)
    list_filter = ('name', 'username')
    search_fields = ('name',)


class ZayavkiCreditOrgAdmin(admin.ModelAdmin):
    """
        create_dt = models.DateTimeField(auto_now=True)
        send_dt = models.DateTimeField(auto_now=True)
        client_anketa = models.ForeignKey(ClientAnketa)
        status = models.CharField(choices=STATUSES, max_length=10)
    """
    model = ZayavkiCreditOrg
    list_display = ('id', 'create_dt', 'send_dt', 'client_anketa', 'status')
    readonly_fields = ('id',)
    fields = ()
    raw_id_fields = ('client_anketa', 'predlogenie',)
    list_filter = ('status',)
    search_fields = ('status',)


class PredlogenieAdmin(admin.ModelAdmin):
    """
        create_dt = models.DateTimeField(auto_created=True)
        update_dt = models.DateTimeField(auto_now=True)
        start_rotate = models.DateTimeField()
        end_rotate = models.DateTimeField()
        name = models.CharField(max_length=254)
        type_of = models.CharField(max_length=1, choices=TYPE_OF)
        min_scoring = models.FloatField()
        max_scoring = models.FloatField()
        credit_org = models.ForeignKey(CreditOrg)
    """
    model = Predlogenie
    list_display = ('id', 'create_dt', 'update_dt', 'start_rotate',
                    'end_rotate', 'name', 'type_of', 'min_scoring',
                    'max_scoring', 'credit_org')
    readonly_fields = ('id', 'create_dt', 'update_dt',)
    fields = ('id', 'name', 'type_of', 'min_scoring', 'max_scoring',
              'credit_org', 'start_rotate', 'end_rotate')
    raw_id_fields = ('credit_org', )
    list_filter = ('create_dt', 'update_dt', 'start_rotate',
                   'end_rotate', 'credit_org',)
    search_fields = ('name', 'type_of', 'min_scoring', 'max_scoring',)


class CreditOrgAdmin(admin.ModelAdmin):
    """
        Кастомизация представления в административной панели,
         модели кредитных организаций.
    """
    list_display = ('id', 'name', 'username')
    readonly_fields = ('id',)
    raw_id_fields = ('username',)
    list_filter = ('name', 'username')
    search_fields = ('id', 'name', 'username',)


class ClientAnketaAdmin(admin.ModelAdmin):
    """

    create_dt = models.DateTimeField(auto_created=True)
    update_dt = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    birthday = models.DateTimeField()
    telephone = models.CharField(max_length=14)
    passport_num = models.CharField(max_length=20)
    score_bal = models.FloatField()

    """
    list_display = (
        'id',
        'create_dt',
        'update_dt',
        'name',
        'surname',
        'lastname',
        'birthday',
        'telephone',
        'passport_num',
        'score_bal',
        'partner',
    )
    readonly_fields = ('id', 'create_dt', 'update_dt', )
    fields = ('id', 'name', 'surname', 'lastname', 'birthday',
              'telephone', 'passport_num', 'score_bal', 'partner',)
    raw_id_fields = ('partner',)
    list_filter = ('create_dt', 'update_dt', 'birthday',)
    search_fields = ('name', 'surname', 'lastname', 'birthday',
                     'telephone', 'passport_num', 'score_bal')


admin.site.register(Partner, PartnerAdmin)
admin.site.register(ZayavkiCreditOrg, ZayavkiCreditOrgAdmin)
admin.site.register(Predlogenie, PredlogenieAdmin)
admin.site.register(CreditOrg, CreditOrgAdmin)
admin.site.register(ClientAnketa, ClientAnketaAdmin)
