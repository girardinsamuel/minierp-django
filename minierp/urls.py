from __future__ import unicode_literals
from django.conf.urls import url, include
from minierp.views import *


urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^tva/$', AddTva.as_view(), name='add-tva'),
    url(r'^tva/delete/(?P<pk>\d+)$', DeleteTva.as_view(), name='delete-tva'),
    url(r'^clients/$', ClientList.as_view(), name='client-list'),
    url(r'^clients/create/', ClientCreate.as_view(), name='client-create'),
    url(r'^clients/edit/(?P<pk>\d+)$', ClientEdit.as_view(), name='client-edit'),
    url(r'^clients/detail/(?P<pk>\d+)$', ClientDetail.as_view(), name='client-detail'),
    url(r'^clients/delete/(?P<pk>\d+)$', ClientDelete.as_view(), name='client-delete'),
    url(r'^client-autocomplete/$', ClientAutocomplete.as_view(), name='client-autocomplete'),
    url(r'^client-data/$', get_client_data, name='get_client_data'),

    url(r'^factures/$', FactureList.as_view(), name='facture-list'),
    url(r'^factures/create/$', facture_create, name='facture-create'),
    url(r'^factures/edit/(?P<pk>\d+)$', facture_edit, name='facture-edit'),
    url(r'^factures/detail/(?P<pk>\d+)$', FactureDetail, name='facture-detail'),
    url(r'^factures/delete/(?P<pk>\d+)$', FactureDelete.as_view(), name='facture-delete'),

    url(r'^devis/$', DevisList.as_view(), name='devis-list'),
    url(r'^devis/create/$', devis_create, name='devis-create'),
    # url(r'^devis/edit/(?P<pk>\d+)$', devis_edit, name='devis-edit'),
    url(r'^devis/detail/(?P<pk>\d+)$', DevisDetail, name='devis-detail'),
    # url(r'^devis/delete/(?P<pk>\d+)$', DevisDelete.as_view(), name='devis-delete'),
]