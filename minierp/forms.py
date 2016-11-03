# -*- coding: utf-8 -*-
from crispy_forms.bootstrap import FormActions, AppendedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Button, HTML, Layout, Field, Fieldset, Div
from dal import autocomplete
from django.forms import ModelForm, inlineformset_factory
from django import forms
from minierp.models import Client, Tva, Facture, FactureStep


class TvaForm(ModelForm):
    """Model Foo form"""
    class Meta:
        model = Tva
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TvaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout.append(
            FormActions(
                Submit('save', 'Ajouter'),
            )),


class ClientForm(ModelForm):
    """Model Foo form"""
    class Meta:
        model = Client
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout.append(
            FormActions(
                Submit('save', 'Ajouter'),
                HTML('<a class="btn btn-default" href={% url "client-list" %}>Annuler</a>'),
            ))


DescriptionFormSet = inlineformset_factory(Facture, FactureStep, extra=1, fields='__all__')


class FactureForm(ModelForm):
    client_address = forms.CharField(required=False, label='Adresse')
    client_cp = forms.CharField(required=False, label='Code Postal')
    client_city = forms.CharField(required=False, label='Ville')

    def __init__(self, *args, **kwargs):
        super(FactureForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(form=self)
        self.helper.form_method = 'POST'
        self.form_tag = False
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-8'
        self.helper.layout = Layout(
            Fieldset(
                'Client',
                Field('id_client'),
                Field('client_address'),
                Field('client_cp'),
                Field('client_city')),
            Fieldset(
                'Facture',
                Field('date'),
                # Field('titre', placeholder='Titre de la facture'),
                Field('add_description')),
            Fieldset(
                'Tarification',
                    Field('tva'),
                    AppendedText('netapayer', '€'),
                    AppendedText('prixht', '€', wrapper_class='prixht'),
                    AppendedText('prixttc', '€', wrapper_class='prixttc'),
                    AppendedText('dejaregle', '€'),
                    AppendedText('parttva', '€'),
                    AppendedText('acompteht', '€'),
                    AppendedText('acomptettc', '€'),
            ),
            FormActions(
                Submit('create', u'Créer',css_class='btn-primary'),
                Button('cancel', u'Annuler', css_class='btn-danger')
            )
        )
        # Wrapping the fields "housenumber and addition". Assign extra class to the fields
        # self.helper[12:14].wrap_together(Div, css_class="price-wrapper")
        # self.helper['house_number'].wrap(Field, wrapper_class="housenumber")
        # self.helper['addition'].wrap(Field, wrapper_class="addition")
        # self.helper[0:1].wrap_together(self.helper.layout, css_class="client_address-wrapper")
        # self.helper['client_address'].wrap(self.helper.layout.Field, wrapper_class="client_address")
        # self.helper['client_cp'].wrap(self.helper.layout.Field, wrapper_class="client_cp")

    class Meta:
        model = Facture
        # fields = ['date', 'id_client', 'titre', 'description', 'acompteht', 'acomptettc', 'tva', 'prixht', 'prixttc', 'dejaregle', 'parttva', 'netapayer']
        fields = '__all__'
        widgets = {
            'id_client': autocomplete.ModelSelect2(url='client-autocomplete')
        }