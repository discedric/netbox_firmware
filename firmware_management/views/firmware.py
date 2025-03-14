import logging
from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import redirect
from django.template import Template
from netbox.views import generic
from utilities.views import register_model_view

from .. import tables
from .. import forms
from .. import models
from ..template_content import WARRANTY_PROGRESSBAR

__all__ = (
    'FirmwareView',
    'FirmwareListView',
    'FirmwareChangeLogView'
)

@register_model_view(models.Firmware)
class FirmwareView(generic.ObjectView):
    queryset = models.Firmware.objects.all()

    def get_extra_context(self, request, instance):
        context = super().get_extra_context(request, instance)
        return context

class FirmwareChangeLogView(generic.ObjectChangeLogView):
    """View for displaying the changelog of a Firmware object"""
    queryset = models.Firmware.objects.all()
    model = models.Firmware
    
    def get(self, request, pk):
        return super().get(request, pk=pk, model=self.model)

@register_model_view(models.Firmware, 'list', path='', detail=False)
class FirmwareListView(generic.ObjectListView):
    queryset = models.Firmware.objects.prefetch_related(
        'manufacturer',
        'device_type',
        'module_type',
        'inventory_item_type'
    )
    table = tables.FirmwareTable
    
@register_model_view(models.Firmware, 'edit')
@register_model_view(models.Firmware, 'add', detail=False)
class FirmwareEditView(generic.ObjectEditView):
    queryset = models.Firmware.objects.all()
    form = forms.FirmwareForm
    

@register_model_view(models.Firmware,'delete')
class FirmwareDeleteView(generic.ObjectDeleteView):
    queryset = models.Firmware.objects.all()

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

@register_model_view(models.Firmware, 'bulk_import', detail=False)
class FirmwareBulkImportView(generic.BulkImportView):
    queryset = models.Firmware.objects.all()
    model_form = forms.FirmwareImportForm

    def save_object(self, object_form, request):
        obj = object_form.save()
        return obj