from __future__ import unicode_literals
from django.db import models
from django.utils import timezone


class Client(models.Model):
    CIVILITES = (
        ('M.', 'M.'),
        ('Mme', 'Mme'),
        ('SARL', 'SARL')
    )
    civilite  = models.CharField(max_length=10,choices=CIVILITES, default='M.')
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255, blank=True)
    adresse = models.CharField(max_length=255, blank=True)
    ville = models.CharField(max_length=255)
    cp = models.IntegerField(blank=True)

    def __unicode__(self):
        return unicode(self.civilite + ' ' + self.nom + ' ' + self.prenom )


class Tva(models.Model):
    value = models.DecimalField(max_digits=4, decimal_places=2)

    def __unicode__(self):
      return str(self.value)


class Facture(models.Model):
    date = models.DateField(default=timezone.now)
    id_client = models.ForeignKey('Client')
    add_description = models.TextField(max_length=400, null=True, blank=True)
    acompteht = models.DecimalField(max_digits=8, decimal_places=2)
    acomptettc = models.DecimalField(max_digits=8, decimal_places=2)
    tva = models.ForeignKey('Tva')
    prixht = models.DecimalField(max_digits=8, decimal_places=2)
    prixttc = models.DecimalField(max_digits=8, decimal_places=2)
    dejaregle = models.DecimalField(max_digits=8, decimal_places=2)
    parttva = models.DecimalField(max_digits=8, decimal_places=2)
    netapayer = models.DecimalField(max_digits=8, decimal_places=2)

    def __unicode__(self):
        return str(self.titre)

    def get_client(self):
        return unicode(self.id_client)


class FactureStep(models.Model):
    facture = models.ForeignKey(Facture)
    step_title = models.CharField(max_length=255)
    step_description = models.TextField(max_length=500)