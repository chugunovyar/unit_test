# -- coding: utf-8 -*-
from django.contrib import admin
from api.models import ZayavkiCreditOrg, Partner, Predlogenie, CreditOrg, ClientAnketa


class PartnerAdmin(admin.ModelAdmin):
    """

    """
    list_display = ('name',)
    readonly_fields = ()
    fields = ()
    raw_id_fields = ()
    list_filter = ()
    search_fields = ('name',)


class ZayavkiCreditOrgAdmin(admin.ModelAdmin):
    """
        create_dt = models.DateTimeField(auto_now=True)
        send_dt = models.DateTimeField(auto_now=True)
        client_anketa = models.ForeignKey(ClientAnketa)
        status = models.CharField(choices=STATUSES, max_length=10)
    """
    list_display = ('create_dt', 'send_dt', 'client_anketa', 'status')
    readonly_fields = ()
    fields = ()
    raw_id_fields = ()
    list_filter = ()
    search_fields = ()


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
    list_display = ('create_dt', 'update_dt', 'start_rotate', 'end_rotate', 'name', 'type_of', 'min_scoring', 'max_scoring', 'credit_org')
    readonly_fields = ()
    fields = ()
    raw_id_fields = ()
    list_filter = ()
    search_fields = ()


class CreditOrgAdmin(admin.ModelAdmin):
    """

    """
    list_display = ('name', )
    readonly_fields = ()
    fields = ()
    raw_id_fields = ()
    list_filter = ()
    search_fields = ()


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
    list_display = ('create_dt', 'update_dt', 'name', 'surname', 'lastname', 'birthday', 'telephone', 'passport_num', 'score_bal')
    readonly_fields = ()
    fields = ()
    raw_id_fields = ()
    list_filter = ()
    search_fields = ()


admin.site.register(Partner, PartnerAdmin)
admin.site.register(ZayavkiCreditOrg, ZayavkiCreditOrgAdmin)
admin.site.register(Predlogenie, PredlogenieAdmin)
admin.site.register(CreditOrg, CreditOrgAdmin)
admin.site.register(ClientAnketa, ClientAnketaAdmin)