# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.forms import formset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView, View
from django.db.models import Q
from minierp.models import Client, Tva, Facture, FactureStep
from minierp.forms import ClientForm, TvaForm, FactureForm, DescriptionFormSet, FactureStepForm
from minierp.pdf import generate_invoice

from dal import autocomplete


def test(request):

    return render(request, 'minierp/test.html')


def home(request):
    context_dict = {}
    # recuperer les derniers clients, devis, factures
    context_dict['client_list'] = Client.objects.order_by('-pk')[:3]
    # context_dict['devis_list'] = Devis.objects.order_by('-pk')[:3]
    context_dict['facture_list'] = Facture.objects.order_by('-pk')[:3]

    return render(request, 'base-minierp.html', context_dict)


class ClientList(ListView):
    model = Client


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
    # paginate_by = 10


class ClientAutocomplete(autocomplete.Select2QuerySetView):
    """view for auto-completion of client name in facture form."""
    def get_queryset(self):

        qs = Client.objects.all()
        if self.q:
            qs = qs.filter(Q(nom__istartswith=self.q) |
                           Q(civilite__istartswith=self.q) |
                           Q(prenom__istartswith=self.q))

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


# class FactureCreate(CreateView):
#     model = Facture
#     form_class = FactureForm
#     success_url = reverse_lazy('facture-list')
#     success_message = u'La facture a bien été créée.'
#
#     def get_context_data(self, **kwargs):
#         data = super(FactureCreate, self).get_context_data(**kwargs)
#         if self.request.POST:
#             data['descriptions'] = DescriptionFormSet(self.request.POST)
#         else:
#             data['descriptions'] = DescriptionFormSet()
#         return data
#
#     def form_valid(self, form):
#
# def facture_create(request):
#
#         # Get our existing formset data for this facture.  This is used as initial data.
#         # facture_steps = FactureStep.objects.filter(facture=facture.pk)
#         # facture_data = [{'step_title': fs.step_title, 'step_description': l.step_description} for fs in facture_steps]
#         #
#         if request.method == 'POST':
#             facture_form = FactureForm(request.POST)
#             des_formset = DescriptionFormSet(request.POST)
#
#             if facture_form.is_valid() and des_formset.is_valid():
#                 # Save facture info
#                 obj = facture_form.save()
#                 # description_form.instance = self.object
#
#
#             new_des = []
#             # id = facture_form.cleaned_data.get('pk')
#             # id = facture_form.pk
#             for des_form in des_formset:
#                 d = des_form.cleaned_data.get('step_description')
#                 t = des_form.cleaned_data.get('step_title')
#                 # id = des_form.cleaned_data.get('id')
#                 des_form.instance = obj
#                 new_des.append(FactureStep(facture=obj, step_description=d, step_title=t))
#
#             with transaction.atomic():
#                 FactureStep.objects.filter(facture=obj.pk).delete()
#                 x = new_des[0].facture_id
#
#                 FactureStep.objects.bulk_create(new_des)
#
#             messages.success(request, 'You have updated your profile.')
#             return HttpResponseRedirect(reverse_lazy('facture-list'))
#         else:
#             facture_form = FactureForm()
#             des_formset = DescriptionFormSet()
#
#         context = {
#             'form': facture_form,
#             'descriptions': des_formset,
#         }
#
#         return render(request, 'minierp/facture_form.html', context)

def facture_create(request):

    FactureStepFormSet = formset_factory(FactureStepForm, formset=DescriptionFormSet )

    # get existing in case of edition (nothing here in creation)

    if request.method == 'POST':
        facture_form = FactureForm(request.POST)
        facturestep_formset = FactureStepFormSet(request.POST)

        if facture_form.is_valid() and facturestep_formset.is_valid():

            # Save facture info
            f = facture_form.save()
            # description_form.instance = self.object

            new_steps = []
            for facturestep in facturestep_formset:
                d = facturestep.cleaned_data.get('step_description')
                t = facturestep.cleaned_data.get('step_title')

                if d and t:
                    new_steps.append(FactureStep(facture=f, step_description=d, step_title=t))

            with transaction.atomic():
                # Replace the old with the new
                FactureStep.objects.filter(facture=f).delete()
                FactureStep.objects.bulk_create(new_steps)

            messages.success(request, 'La facture n° %d a bien été créée.' % f.pk)
            return HttpResponseRedirect(reverse_lazy('facture-list'))
    else:
        facture_form = FactureForm()
        facturestep_formset = DescriptionFormSet()# put initial data in edition

    context = {
        'form': facture_form,
        'facturestep_formset': facturestep_formset,
        'is_edition': False
    }

    return render(request, 'minierp/facture_form.html', context)



def facture_edit(request, pk):

    FactureStepFormSet = formset_factory(FactureStepForm, formset=DescriptionFormSet )

    # get existing in case of edition (nothing here in creation)
    facture = get_object_or_404(Facture, pk=pk)
    facture_steps = FactureStep.objects.filter(facture=facture)
    fs_data = [{'step_title': fs.step_title, 'step_description': fs.step_description} for fs in facture_steps]

    if request.method == 'POST':
        facture_form = FactureForm(request.POST, instance=facture)
        facturestep_formset = FactureStepFormSet(request.POST)

        if facture_form.is_valid() and facturestep_formset.is_valid():

            # Save facture info
            f = facture_form.save()
            # description_form.instance = self.object

            new_steps = []
            for facturestep in facturestep_formset:
                d = facturestep.cleaned_data.get('step_description')
                t = facturestep.cleaned_data.get('step_title')

                if d and t:
                    new_steps.append(FactureStep(facture=f, step_description=d, step_title=t))

            with transaction.atomic():
                # Replace the old with the new
                FactureStep.objects.filter(facture=f).delete()
                FactureStep.objects.bulk_create(new_steps)

            messages.success(request, 'La facture n° %d a bien été modifiée.' % f.pk)
            return HttpResponseRedirect(reverse_lazy('facture-list'))
    else:
        facture_form = FactureForm(instance=facture)
        facturestep_formset = DescriptionFormSet(initial=fs_data)# put initial data in edition

    context = {
        'form': facture_form,
        'facturestep_formset': facturestep_formset,
        'is_edition': True
    }

    return render(request, 'minierp/facture_form.html', context)


def FactureDetail(request, pk):

    # get facture
    facture = Facture.objects.get(pk=pk)

    # get related description steps
    # Car.objects.filter(id__in=(1, 2))
    formset = FactureStep.objects.filter(facture=facture)

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
