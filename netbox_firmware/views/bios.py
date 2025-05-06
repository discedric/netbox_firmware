import logging
from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import redirect
from django.template import Template
from netbox.views import generic
from utilities.query import count_related
from utilities.views import register_model_view, ViewTab
from ..utils import get_countdevice

from netbox_firmware import tables
from netbox_firmware import forms
from netbox_firmware import models
from netbox_firmware import filtersets

__all__ = (
    'BiosView',
    'BiosListView',
    'BiosChangeLogView',
    'BiosJournalView',
)

@register_model_view(models.Bios)
class BiosView(generic.ObjectView):
    queryset = models.Bios.objects.all()

    def get_extra_context(self, request, instance):
        context = super().get_extra_context(request, instance)
        return context

class BiosChangeLogView(generic.ObjectChangeLogView):
    """View for displaying the changelog of a Bios object"""
    queryset = models.Bios.objects.all()
    model = models.Bios
    
    def get(self, request, pk):
        return super().get(request, pk=pk, model=self.model)

class BiosJournalView(generic.ObjectJournalView):
    """View for displaying the journal of a Bios object"""
    queryset = models.Bios.objects.all()
    model = models.Bios
    
    def get(self, request, pk):
        return super().get(request, pk=pk, model=self.model)

@register_model_view(models.Bios, 'list', path='', detail=False)
class BiosListView(generic.ObjectListView):
    queryset = models.Bios.objects.prefetch_related(
        'device_type',
        'module_type'
    ).annotate(
        instance_count=count_related(models.BiosAssignment,'bios'),
    )
    filterset = filtersets.BiosFilterSet
    filterset_form = forms.BiosFilterForm
    table = tables.BiosTable

@register_model_view(models.Bios, 'edit')
@register_model_view(models.Bios, 'add', detail=False)
class BiosEditView(generic.ObjectEditView):
    queryset = models.Bios.objects.all()
    form = forms.BiosForm
    default_return_url = 'plugins:netbox_firmware:bios_list'

@register_model_view(models.Bios,'delete')
class BiosDeleteView(generic.ObjectDeleteView):
    queryset = models.Bios.objects.all()

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


# ----------------- Bulk Import, Edit, Delete -----------------

@register_model_view(models.Bios, 'bulk_import', detail=False)
class BiosBulkImportView(generic.BulkImportView):
    queryset = models.Bios.objects.all()
    model_form = forms.BiosImportForm

    def save_object(self, object_form, request):
        obj = object_form.save()
        return obj
    
@register_model_view(models.Bios, 'bulk_edit', detail=False)
class BiosBulkEditView(generic.BulkEditView):
    queryset = models.Bios.objects.all()
    filterset = filtersets.BiosFilterSet
    table = tables.BiosTable
    form = forms.BiosBulkEditForm
    default_return_url = 'plugins:netbox_firmware:bios_list'
    
    def post (self, request, **kwargs):
        return super().post(request, **kwargs)

@register_model_view(models.Bios, 'bulk_delete', detail=False)
class BiosBulkDeleteView(generic.BulkDeleteView):
    queryset = models.Bios.objects.all()
    table = tables.BiosTable

    def post(self, request):
        return super().post(request)