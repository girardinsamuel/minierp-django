# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView, View

from minierp.models import Client, Tva, Facture
from minierp.forms import ClientForm, TvaForm, FactureForm, DescriptionFormSet
from minierp.pdf import generate_invoice

from dal import autocomplete


def home(request):
    context_dict = {}
    # recuperer les derniers clients, devis, factures
    context_dict['client_list'] = Client.objects.order_by('-pk')[:3]
    # context_dict['devis_list'] = Devis.objects.order_by('-pk')[:3]
    context_dict['facture_list'] = Facture.objects.order_by('-pk')[:3]

    return render(request,'base.html', context_dict)


class ClientList(ListView):
    model = Client
    paginate_by = 10


class ClientCreate(SuccessMessageMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('client-list')
    success_message = u'%(civilite)s %(nom)s %(prenom)s a bien été ajouté.'


class ClientEdit(SuccessMessageMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('client-list')
    success_message = u'%(civilite)s %(nom)s %(prenom)s a bien été modifié.'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ClientEdit, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['is_edition'] = True
        return context


class ClientDetail(DetailView):
    model = Client


class ClientDelete(SuccessMessageMixin, DeleteView):
    model = Client
    context_object_name = 'obj'
    template_name = "minierp/obj_delete.html"
    success_url = reverse_lazy('client-list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        client = self.object.__dict__['civilite'] + " " + self.object.__dict__['nom'] + " " +self.object.__dict__['prenom']
        success_message = u'Le client %s a bien été supprimé.' % client
        messages.warning(self.request, success_message)
        return super(ClientDelete, self).delete(request, *args, **kwargs)


class AddTva(SuccessMessageMixin, CreateView):
    model = Tva
    form_class = TvaForm
    success_url = reverse_lazy('add-tva')
    success_message = u'La TVA à %(value)s %% a bien été ajoutée.'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(AddTva, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['tva_list'] = Tva.objects.all()
        return context


class DeleteTva(SuccessMessageMixin, DeleteView):
    model = Tva
    context_object_name = 'obj'
    template_name = "minierp/obj_delete.html"
    success_url = reverse_lazy('add-tva')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_message = u'La TVA %s a bien été supprimée.' % self.object
        messages.warning(self.request, success_message)
        return super(DeleteTva, self).delete(request, *args, **kwargs)


class FactureList(ListView):
    model = Facture
    paginate_by = 10


class ClientAutocomplete(autocomplete.Select2QuerySetView):
    """view for auto-completion of client name in facture form."""
    def get_queryset(self):

        qs = Client.objects.all()
        if self.q:
            qs = qs.filter(nom__istartswith=self.q)

        return qs


@csrf_exempt
def get_client_data(request):
    id_client = int(request.POST.get('id', ''))

    if id_client:
        client = Client.objects.get(pk=id_client)
        data = {'address': client.adresse, 'cp': client.cp, 'city': client.ville}
        return HttpResponse(json.dumps(data))

    response = {}
    return HttpResponse(json.dumps(response))


class FactureCreate(SuccessMessageMixin, CreateView):
    model = Facture
    form_class = FactureForm
    success_url = reverse_lazy('facture-list')
    success_message = u'La facture a bien été créée.'

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        description_form = DescriptionFormSet()
        return self.render_to_response(
            self.get_context_data(form=form,
                                  description_form=description_form))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        description_form = DescriptionFormSet(self.request.POST)
        if form.is_valid():
            if description_form.is_valid():
                return self.form_valid(form, description_form)
        else:
            return self.form_invalid(form, description_form)

    def form_valid(self, form, description_form):
        """
        Called if all forms are valid. Creates a Recipe instance along with
        associated Ingredients and Instructions and then redirects to a
        success page.
        """
        self.object = form.save()
        description_form.instance = self.object
        description_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, description_form):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(self.get_context_data(form=form, description_form=description_form))


class FactureEdit(SuccessMessageMixin, UpdateView):
    model = Facture
    form_class = FactureForm
    success_url = reverse_lazy('facture-list')
    success_message = u'La facture a bien été modifiée.'


def FactureDetail(request, pk):

    # get facture
    facture = Facture.objects.get(pk=pk)
    # get related description steps
    formset = DescriptionFormSet(instance=facture)

    # get facture number to create facture filename
    filename = 'F_' + str(pk)

    # create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=' + filename + '.pdf'

    # generate pdf with report lab library
    pdf = generate_invoice(response, facture, formset)

    # show page
    pdf.showPage()
    pdf.save()

    return response


class FactureDelete(SuccessMessageMixin, DeleteView):
    model = Facture
    context_object_name = 'obj'
    template_name = "minierp/obj_delete.html"
    success_url = reverse_lazy('facture-list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        facture = self.object.__dict__['tire']
        success_message = u'La facture "%s" a bien été supprimée.' % facture
        messages.warning(self.request, success_message)
        return super(FactureDelete, self).delete(request, *args, **kwargs)
