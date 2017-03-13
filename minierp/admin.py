from django.contrib import admin
from minierp.models import Facture, FactureStep, Client, Tva, Devis, DevisStep
from minierp.forms import DescriptionFormSet, DescriptionDevisFormSet


class FactureStepInline(admin.TabularInline):
    model = FactureStep
    formset = DescriptionFormSet


class DevisStepInline(admin.TabularInline):
    model = DevisStep
    formset = DescriptionDevisFormSet


class FactureAdmin(admin.ModelAdmin):
    list_display = ('id_client', 'date', 'netapayer')
    inlines = [
        FactureStepInline,
    ]


class DevisAdmin(admin.ModelAdmin):
    list_display = ('id_client', 'date')
    inlines = [
        DevisStepInline,
    ]


class ClientAdmin(admin.ModelAdmin):
    list_display = ('civilite', 'nom', 'prenom', 'ville')


admin.site.register(Facture, FactureAdmin)
admin.site.register(Devis, DevisAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Tva)
