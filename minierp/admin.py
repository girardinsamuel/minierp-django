from django.contrib import admin
from minierp.models import Facture, FactureStep, Client, Tva
from minierp.forms import DescriptionFormSet


class FactureStepInline(admin.TabularInline):
    model = FactureStep
    formset = DescriptionFormSet


class FactureAdmin(admin.ModelAdmin):
    list_display = ('id_client', 'date', 'netapayer')
    inlines = [
        FactureStepInline,
    ]


class ClientAdmin(admin.ModelAdmin):
    list_display = ('civilite', 'nom', 'prenom', 'ville')


admin.site.register(Facture, FactureAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Tva)